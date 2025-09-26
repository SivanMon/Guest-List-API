import uuid, logging, re, os
from flask import Flask, request, send_from_directory, jsonify

import boto3
from botocore.exceptions import ClientError

app = Flask("guestlistapp")
logging.basicConfig(level=logging.INFO)

# ---- DynamoDB setup ----
AWS_REGION       = os.getenv("AWS_REGION", "us-east-1")
DDB_TABLE        = os.getenv("DDB_TABLE", "guests-dev")
DDB_ENDPOINT_URL = os.getenv("DDB_ENDPOINT_URL")  # None in AWS

_ddb = boto3.resource("dynamodb", region_name=AWS_REGION, endpoint_url=DDB_ENDPOINT_URL)
_table = _ddb.Table(DDB_TABLE)

# simple validators
_ID_RE    = re.compile(r"^[0-9]{5,20}$")
_PHONE_RE = re.compile(r"^0\d{8,9}$")  # 9–10 digits starting with 0
def _bad(msg): return jsonify({"error": msg}), 400


@app.route("/")
def serve_frontend():
    return send_from_directory('.', 'index.html')

@app.route('/api')
def api_root():
    return {"name": "Guest List API", "storage": "dynamodb", "table": DDB_TABLE}


# ---- Guests ----

@app.route('/guests', methods=['GET'])
def get_all_guests():
    items, start = [], None
    while True:
        resp = _table.scan(ExclusiveStartKey=start) if start else _table.scan()
        items.extend(resp.get("Items", []))
        start = resp.get("LastEvaluatedKey")
        if not start:
            break
    # keep your existing shape: {seq_num: {...}}
    return {it["seq_num"]: it for it in items}

@app.route('/guests', methods=['POST'])
def add_new_guest():     # expects: id, firstname, surname, quantity, phone, email
    try:
        data = request.get_json(silent=True) or {}

        # backward-compat if someone still sends guest_id
        if "id" not in data and "guest_id" in data:
            data["id"] = data["guest_id"]

        required = ["id", "firstname", "surname", "quantity", "phone", "email"]
        for k in required:
            if k not in data:
                return _bad(f"Missing field: {k}")

        if not _ID_RE.match(str(data["id"])):
            return _bad("Invalid id format")

        q = str(data["quantity"])
        if not q.isdigit() or int(q) <= 0:
            return _bad("Invalid quantity")

        if not _PHONE_RE.match(str(data["phone"])):
            return _bad("Invalid phone")

        # prevent duplicate person id (simple scan; fine for your size)
        dup = _table.scan(
            ProjectionExpression="#i",
            ExpressionAttributeNames={"#i": "id"},
            FilterExpression="id = :pid",
            ExpressionAttributeValues={":pid": str(data["id"])},
        )
        if dup.get("Count", 0) > 0:
            return {"error": "Guest with this ID already exists"}, 409

        seq_num = str(uuid.uuid4())
        item = {
            "seq_num": seq_num,
            "id": str(data["id"]),
            "firstname": str(data["firstname"]),
            "surname": str(data["surname"]),
            "quantity": str(data["quantity"]),
            "phone": str(data["phone"]),
            "email": str(data["email"]),
        }

        try:
            _table.put_item(
                Item=item,
                ConditionExpression="attribute_not_exists(#s)",
                ExpressionAttributeNames={"#s": "seq_num"},
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return {"error": "Race on seq_num, try again"}, 409
            raise

        logging.info(f"New guest created: {item}")

        return {
            "message": "Guest created successfully",
            "guest": {
                "seq_num": seq_num,
                "firstname": item["firstname"],
                "surname": item["surname"],
                "quantity": item["quantity"],
                "phone": item["phone"],
                "email": item["email"],
                "id": item["id"]
            }
        }, 201

    except Exception as e:
        logging.exception("Error creating guest")
        return {"error": str(e)}, 500

@app.route('/guests/<id>', methods=['DELETE'])
def delete_guest(id):
    try:
        _table.delete_item(
            Key={"seq_num": id},
            ConditionExpression="attribute_exists(#s)",
            ExpressionAttributeNames={"#s": "seq_num"},
        )
        return {'msg': f'Guest {id} deleted successfully'}, 200
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return {'msg': f"Can't delete, guest seq_num '{id}' not found"}, 404
        raise

@app.route('/guests/<id>', methods=['GET'])
def get_specific_guest(id):
    resp = _table.get_item(Key={"seq_num": id})
    item = resp.get("Item")
    if not item:
        return {'error': f"Guest with seq_num '{id}' not found"}, 404
    return item, 200


# ---- Health ----

@app.route('/health')
def health_check():
    # fast approximate count; cheap for small tables
    resp = _table.scan(Select="COUNT")
    return {'status': 'healthy', 'guests_count': resp.get("Count", 0)}, 200

@app.route("/healthz", methods=["GET"])
def healthz():
    # process is up
    return jsonify(status="ok"), 200

@app.route("/readyz", methods=["GET"])
def readyz():
    # lightweight dependency check: DynamoDB describe table
    try:
        region = os.environ["AWS_DEFAULT_REGION"]
        table_name = os.environ["DDB_TABLE"]
        dynamodb = boto3.resource("dynamodb", region_name=region)
        table = dynamodb.Table(table_name)
        table.load()  # calls DescribeTable
        return jsonify(status="ready"), 200
    except Exception as e:
        # don't expose secrets; 503 tells k8s it's not ready yet
        return jsonify(status="not-ready", reason=str(e)[:200]), 503

if __name__ == "__main__":
    app.run('0.0.0.0', 1111, debug=False)