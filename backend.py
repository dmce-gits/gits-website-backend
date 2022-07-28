import firebase_admin
from firebase_admin import credentials, db
from flask import request
from flask import jsonify
from flask import Flask
from flask_cors import CORS, cross_origin
from pydantic import EmailError

app = Flask(__name__)
CORS(app, resources = {r"*": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type    '
app.config['Access_Control_Allow_Origin'] = '*'

config = {
  "apiKey": "AIzaSyCWX9vdYEtH0F8z_RdtYATy3AYY6IaKAdc",
  "authDomain": "git-website-490ba.firebaseapp.com",
  "projectId": "git-website-490ba",
  "storageBucket": "git-website-490ba.appspot.com",
  "messagingSenderId": "98278579912",
  "appId": "1:98278579912:web:41662294a35cb1054f0ffd",
  "measurementId": "G-5J8P9EDEZS",
}
cred = credentials.Certificate('./firebaseSDK.json')
firebase_app = firebase_admin.initialize_app(cred,{"databaseURL": "https://git-website-490ba-default-rtdb.firebaseio.com/"})

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin','*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.route('/insertData', methods=['POST', 'OPTIONS'], strict_slashes=False)
def insertData():
    data = request.json
    print(data)
    ref = db.reference('/certificates')
    ref.update(data)
    return jsonify({"success": True})

@app.route("/verify", methods=['POST', 'OPTIONS'], strict_slashes=False)
def verify():
    data = request.json
    print(data)
    ref = db.reference(f'/certificates/{data["crt_number"]}')
    cert_data = ref.get()   
    return jsonify(cert_data)

@app.route("/deleteCrt", methods=['POST', 'OPTIONS'], strict_slashes=False)
def deleteCrt():
    data = request.json
    print(data)
    ref = db.reference(f'/certificates/{data["crt_number"]}')
    ref.delete()
    return jsonify({"success": True})

@app.route("/eventRegistration", methods=['GET','PUT','POST','DELETE','OPTIONS'])
def eventRegistration():
    data = request.json

    
    event = data["event"]
    name = data["name"]
    email = data["email"]
    phone = data["phone"]
    div = data["div"]
    year = data["year"]
    stdid = data["grNum"]
    roll_no = data["rollnum"]
    input = {
            "name": name,
            "email": email,
            "division": div,
            "year": year,
            "stdid": stdid,
            "roll_no": roll_no,
        }
    
    print(data)
    ref = db.reference(f'/Registration/{event}/{phone}')
    ref.update(input) 
    return _corsify_actual_response(jsonify({"success": True}))

@app.route("/getRegistrations", methods=['POST', 'OPTIONS'], strict_slashes=False)
def getRegistrations():
    data = request.json
    event = data["event"]
    ref = db.reference(f'/Registration/{event}')
    registrations = ref.get()
    return jsonify(registrations)

def _corsify_actual_response(response):
    # response.headers.add("Access-Control-Allow-Origin", "*")
    response.status_code = 200
    return response

if __name__ == "__main__":
    app.run(debug=True)
