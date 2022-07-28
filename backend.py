import flask
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, db
from flask_cors import CORS
import pyrebase
from flask_mail import Mail, Message

app = Flask(__name__)

mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'minipromail@gmail.com'
app.config['MAIL_PASSWORD'] = 'mrunal3996'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'minipromail@gmail.com'


config = {
    "apiKey": "AIzaSyAJppA-q39TMHVMGdb4Bo-VuQDVlEGxJv8",
    "authDomain": "pyminiproject.firebaseapp.com",
    "databaseURL": "https://pyminiproject-default-rtdb.firebaseio.com",
    "projectId": "pyminiproject",
    "storageBucket": "pyminiproject.appspot.com",
    "messagingSenderId": "650816371817",
    "appId": "1:650816371817:web:0b7cb04b80f4fa461ab6f8",
    "measurementId": "G-VWE27L6J03"
}

firebase_sdk = {
  "type": "service_account",
  "project_id": "pyminiproject",
  "private_key_id": "c6830cc827984ba6fd6037dd712fd6d8bb49e511",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC+/P+2m/+qQqFt\nMc9cCgxWYbUBJYMMGKSej2Yi2LA7mVPsnq87xL+1Vubia8Bd/LsxoOMkfomaX5GO\n6LzDuxmFydU2XfrSIn2jtH3az/p4H52gAxMiJvGc2lmBK9gQ1PfpbYpV4acl1RzC\ncbuVWKB3vIt4xh193MYgnHy8OAQfliRZGqddZJj8Y6uERzibDAp6DfObmN1jy38n\nxJRkiFSVbc8c7rW3tz6tjR9Ia1UYn2b2iuzTjktKCcX2zzKl3MErz4KxU/Yvud2z\nuL6eqhlwIjGe5T2P9TysqqdjErtcK4LvewQyyzG9wcoBHuWRlsWPHHxTgr/8fXYs\nbcSL1mwtAgMBAAECggEAF2vlXBqTZujW7RIvsMTWsH04+lQEVyZqgbtqNhnGuvhZ\nr2niaXz+WZm3pMq8A4qr1jE5yc7uxwyzSAhIpeQ7BAo1aH5r9Psf10SaLoxU1ghi\nhy35WbXW6XppgYrD64SChpDVZyTOH7ib10ilTXJZ83Ue0YfSNA4wCe3G6jogX1MP\nElcy1QCixjWBgGaMECODZiML6vnGdudvYJ0JyE6zlsyluPyjfpd5bMZr+WccI6JF\n/3zRHz4VElYsSidbfmBU5u2p3loygI82KcBTMOwtqKutFEIFTtVTxywcI4515Mzu\ntq1F4ReFzk5oy4DmHVUEUKk+4PU6jGZ1m2F3HZVMDQKBgQDg3hkPyA4wXx9MeEQa\n6pmgvNGXUfRAD8izcMvbcQXljw/ujK7RMjynnIWxKN2gn1eNzvf8LU7uQ7XmOsD0\nC4r9OFlye+ZWo/+qGAjGDNbCRFvjo7DhY2i3xDXaJf3QoF7FOo74XY0+3w5tuo77\npV0eYFXr2EoQ3TMkZR9rGNZCzwKBgQDZbiEOnEQ6VlqlQNKGnzpmHn/rFSCy1sT1\n8yjvUA7X9qfi3ldB16jnQ30R8nq0GYSy1+qURlUj/r0ostyIow125B89R50vFO0M\nHKzZ62IuZ4UDvBnngJaAXnlYw5OUqMoMjfd2r+XY8oGSTPFEiUleH3fvTN9SOEM3\nUGXPHIoQQwKBgQDgGHahY53AVwu6CaDVsjaoGYRGaUYhEZnSOfbvGhPmUkxuT4Vo\ntcf8wd/6Td+Q0ztN95Trm7utd40vhB4HF/nLoPyDOzax4X5I5OrZdLIRqE5q7ha4\nh3k0qjWA0ZvA7hGEPHd+zLyWi3S1pdYYsxO50gfOoh4t8EOnYZ+N+5KLwQKBgF/J\nrLaLEWPB910mGZlFPK0QcrpWLHmdNFhGL5p+YouyFnRUD4zqPXbkvIzTjksZkuRX\nSvjXo1qgNyVe5tkrPBtMlJainhTH20aiu2Ol1zMqV+c1TxQ2ChezhzIbt0Ceu6Sc\nRpD7HP9elsalLwVKlg/pPSUncJsAPlx4BuIfaJORAoGBAIpxKvsBR5ljjvUWXPrc\n5yJJ80Hz7m7IPv1KLYTPMiOJ54qvvM/PWX3PFpUEURljzfS0JaZTA3db7SrleU89\nxtRZpaJ2tP54Spp/S53SdSsbKkkbibvuuqKJlv9SSAEb6lP9W6YFJRupMUt1HaAC\n/clQG6F5/sZf2GVESSYsEd25\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-g3srf@pyminiproject.iam.gserviceaccount.com",
  "client_id": "103798281264116231160",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-g3srf%40pyminiproject.iam.gserviceaccount.com"
}

cred = credentials.Certificate(firebase_sdk)
firebase = pyrebase.initialize_app(config)
firebase_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pyminiproject-default-rtdb.firebaseio.com/'
})

firestore_app = firestore.client()

storage = firebase.storage()


CORS(app, supports_credentials=True)

@app.route('/getImage', methods=['POST', 'OPTIONS', 'GET'])
def getImage():
    images = db.reference('Image').get()
    return jsonify(images)
    
@app.route('/contact', methods=['POST', 'OPTIONS', 'GET'])
def contact():
    data = request.json
    name = data['name']
    email = data['email']
    phone = data['phone']
    message = data['message']
    print ("it'working")
    db.reference(f'Contact/{email}').push({
        'name': name,
        'email': email,
        'phone': phone,
        'message': message
    })
    msg = Message(f'{name} your message has been sent', recipients=[email])
    msg.body = f'Your messge is : {message}'
    mail.send(msg)
    
    return jsonify({'success': True})








if __name__ == '__main__':
    app.run(debug=True)