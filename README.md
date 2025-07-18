# Guest-List-API
🎉 Guest List API

A simple Flask-based RESTful API to manage a guest list. This API allows you to add, view, update, and delete guests.

🚀 Features

GET /guests – Retrieve the full guest list.
POST /guests – Add a new guest.
PUT /guests/<guest_id> – Update an existing guest's information.
DELETE /guests/<guest_id> – Remove a guest from the list.
🛠️ Technologies

Python 3.x
Flask
JSON for data exchange
📦 Installation

Clone the repository:
   git clone https://github.com/your-username/guest-list-api.git

   cd guest-list-api

Create a virtual environment (optional but recommended):
   python -m venv venv

   source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
   pip install -r requirements.txt

Run the app:
   python app.py

📬 API Endpoints

GET /guests

Returns a list of all guests.

Response:

[

  {

    "id": 1,

    "name": "Alice",

    "email": "alice@example.com"

  }

]

POST /guests

Adds a new guest.

Request Body:

{

  "name": "Bob",

  "email": "bob@example.com"

}

Response:

{

  "message": "Guest added successfully",

  "guest": {

    "id": 2,

    "name": "Bob",

    "email": "bob@example.com"

  }

}

PUT /guests/<guest_id>

Updates an existing guest.

Request Body:

{

  "name": "Robert",

  "email": "robert@example.com"

}

Response:

{

  "message": "Guest updated successfully"

}

DELETE /guests/<guest_id>

Deletes a guest by ID.

Response:

{

  "message": "Guest deleted successfully"

}

📁 Project Structure

guest-list-api/

│

├── app.py               # Main Flask application

├── requirements.txt     # Python dependencies

└── README.md            # Project documentation

🧪 Testing

You can test the API using tools like:

Postman
curl
httpie
📄 License

This project is licensed under the MIT License.
