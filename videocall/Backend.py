from flask import Flask, request, jsonify, request

from flask_cors import CORS

import threading

  

app = Flask(__name__)

CORS(app)

  

# Este diccionario almacenar la informaci n de se alizaci n de los usuarios

# La clave es un identificador de usuario, y el valor es un diccionario con IP y puerto

user_sessions = {}

  

# Lock para controlar el acceso concurrente al diccionario user_sessions

lock = threading.Lock()

  

@app.route('/register', methods=['POST'])

def register():

    data = request.json

    user_id = data.get('user_id')

    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)

    #ip_address = data.get('ip_address')

    port = data.get('port')

  

    if not all([user_id, ip_address, port]):

        return jsonify({'error': 'Falta informaci n'}), 400

  

    with lock:

        user_sessions[user_id] = {

            'ip_address': ip_address,

            'port': port

        }

        print(ip_address, user_id)

        return jsonify({'message': 'Registro exitoso'}), 200

  

@app.route('/get_user/<user_id>', methods=['GET'])

def get_user(user_id):

    with lock:

        user_info = user_sessions.get(user_id)

        if user_info:

            return jsonify(user_info), 200

        else:

            return jsonify({'error': 'Usuario no encontrado'}), 404

  

    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)
