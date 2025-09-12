import uuid, logging
from flask import Flask, request, send_from_directory
import os

app = Flask("guestlistapp")

all_guests = {}
logging.basicConfig(level=logging.INFO)


@app.route("/")
def serve_frontend():
    """Serve the HTML frontend"""
    return send_from_directory('.', 'index.html')

@app.route('/api')
def main_error():
    """API root endpoint"""
    result = {'msg':"API root endpoint - use /guests for guest operations"}
    return result

@app.route('/guests', methods=['GET'])
def get_all_guests():
    return all_guests

@app.route('/guests', methods=['POST'])
def add_new_guest():     #  Details: 'firstname', 'surname', 'quantity', 'phone', 'email'
    try:
        guest_details = request.get_json()

        # validating that all fields are filled.
        required_fields = ['firstname', 'surname', 'quantity', 'phone', 'email', 'id']
        for field in required_fields:
            if field not in guest_details:
                return {"error": f"Missing field: {field}"}, 400

        # make sure that the quantity is a positive number.
        try:
            quantity = int(guest_details['quantity'])
            if quantity <= 0:
                return {"error": "Quantity must be positive"}, 400
        except ValueError:
            return {"error": "Quantity must be a number"}, 400

        # validating that the phone number is Israeli (10 digits, starts with 0, only numbers)
        try:
            phone = guest_details['phone']

            if not isinstance(phone, str):
                phone = str(phone)

            if not phone.isdigit():
                return {"error": "Phone must contain only digits"}, 400

            if not phone.startswith('0'):
                return {"error": "Phone must start with 0"}, 400

            if len(phone) != 10:
                return {"error": "Phone number must be exactly 10 digits long"}, 400
        except Exception as e:
            return {"error": "Invalid phone format"}, 400

        # checking if guest already exists (FIXED: was all_guests(id) instead of all_guests)
        existing_guest_id = None
        for seq_num, guest in all_guests.items():
            if guest.get('id') == guest_details['id']:
                existing_guest_id = seq_num
                break
        
        if existing_guest_id:
            return {"error": "Guest with this ID already exists"}, 409

        seq_num = str(uuid.uuid4())
        guest_details['seq_num'] = seq_num
        all_guests[seq_num] = guest_details

        logging.info(f"New guest created: {guest_details}")

        return {
            "message": "Guest created successfully",
            "guest": {
                "seq_num": seq_num,
                "id" : guest_details['id'],
                "firstname": guest_details['firstname'],
                "surname": guest_details['surname'],
                "phone": guest_details['phone'],
                "email": guest_details['email'],
                "quantity": quantity
            }
        }, 201

    except Exception as e:
        logging.exception("Error in /guests")
        return {"error": "Internal server error"}, 500

@app.route('/guests/<id>', methods=['DELETE'])
def delete_guest(id):
    """Delete guest by seq_num (FIXED: now works correctly)"""
    if id in all_guests:
       del all_guests[id]
       return {'msg': f'Guest {id} deleted successfully'}, 200
    else:
        return {'msg': f"Can't delete, guest seq_num '{id}' not found"}, 404

@app.route('/guests/<id>', methods=['GET'])
def get_specific_guest(id):
    """Get specific guest by seq_num (FIXED: was returning function instead of data)"""
    if id in all_guests:
        return all_guests[id], 200
    else:
        return {'error': f"Guest with seq_num '{id}' not found"}, 404

# Health check endpoint for Kubernetes
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'guests_count': len(all_guests)}, 200

if __name__ == "__main__":
    app.run('0.0.0.0', 1111, debug=False)
