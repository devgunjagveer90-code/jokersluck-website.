import os
from flask import Flask, request, send_from_directory, abort
import subprocess

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('assets', path)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    if name and email and message:
        name_esc = name.replace("'", "''")
        email_esc = email.replace("'", "''")
        message_esc = message.replace("'", "''")
        
        query = f"INSERT INTO inquiries (name, email, message) VALUES ('{name_esc}', '{email_esc}', '{message_esc}')"
        
        try:
            # Run team-db CLI
            subprocess.run(['team-db', query], check=True)
            return "<h1>Thank you!</h1><p>Your message has been received.</p><a href='/'>Return to home</a>"
        except subprocess.CalledProcessError as e:
            return f"Error saving inquiry: {e}", 500
    
    return "Please fill out all fields.", 400

if __name__ == '__main__':
    # Using port 8000 to replace the existing http.server
    app.run(host='0.0.0.0', port=8000)
