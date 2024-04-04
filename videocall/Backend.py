from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

room_messages = {}
users = {}  # Esto es solo para demostración. Para producción, usa una base de datos.



@socketio.on_error_default  # Captura todos los espacios de nombres sin un manejador de errores registrado.
def default_error_handler(e):
    print(f'Ha ocurrido un error: {str(e)}')
    emit('error', {'error': 'Ocurrió un error inesperado'})

@app.route('/')
def index():
    return "Servidor de señalización para WebRTC"

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()  # Obtiene los datos del cuerpo de la petición
    userId = data.get('userId')
    if not userId:
        # Retorna un mensaje de error si el userId no está presente
        return jsonify({'error': 'Falta proporcionar userId'}), 400
    
    # Aquí puedes agregar la lógica para manejar el registro del usuario
    # Por ejemplo, guardarlo en una base de datos o alguna otra operación necesaria
    print(f'Usuario registrado: {userId}')
    users[userId] = {"rooms": []}  # Simula almacenamiento en memoria
    # Retorna una respuesta de éxito
    return jsonify({'message': 'Usuario registrado exitosamente'}), 200


# Evento de conexión WebSocket
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

# Evento de desconexión WebSocket
@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

# Unirse a una sala específica
@socketio.on('join')
def on_join(data):
    try:
        username = data['userId']
        room = data['room']
        if not username or not room:
            raise ValueError('Faltan datos necesarios: userId o room.')
        join_room(room)
        print(f'{username} se ha unido a la sala: {room}')
        # Enviar mensajes anteriores de la sala al usuario
        for message in room_messages.get(room, []):
            emit('message', message, to=request.sid)
        emit('joined_room', {'message': f'{username} se ha unido a la sala {room}'}, to=room)
    except KeyError as e:
        emit('error', {'error': f'Falta el campo {e.args[0]}'})
    except ValueError as e:
        emit('error', {'error': str(e)})


@socketio.on('send_message')
def handle_send_message(data):
    try:
        owner = data['owner']
        message = data['message']
        room = data['room']
        if not owner or not message or not room:
            raise ValueError('Faltan datos necesarios: owner, message o room.')
        if room not in room_messages:
            room_messages[room] = []
        room_messages[room].append({'owner': owner, 'message': message})
        emit('message', {'owner': owner, 'message': message}, room=room, include_self=False)
    except KeyError as e:
        emit('error', {'error': f'Falta el campo {e.args[0]}'})
    except ValueError as e:
        emit('error', {'error': str(e)})
        

# Manejar el envío de oferta SDP
@socketio.on('send_offer')
def handle_send_offer(json):
    try:
        room = json['target']
        emit('receive_offer', json, room=room)
    except KeyError as e:
        emit('error', {'error': f'Falta el campo {e.args[0]}'})

# Manejar el envío de respuesta SDP
@socketio.on('send_answer')
def handle_send_answer(json):
    try:
        room = json['target']
        emit('receive_answer', json, room=room)
    except KeyError as e:
        emit('error', {'error': f'Falta el campo {e.args[0]}'})

@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    message = data['message']
    # Almacenar el mensaje en la sala correspondiente
    if room not in room_messages:
        room_messages[room] = []
    room_messages[room].append(message)
    # Emitir el mensaje a todos en la sala
    emit('message', message, to=room)

# Manejar el envío de candidatos ICE
@socketio.on('send_candidate')
def handle_send_candidate(json):
    try:
        room = json['target']
        emit('receive_candidate', json, room=room)
    except KeyError as e:
        emit('error', {'error': f'Falta el campo {e.args[0]}'})

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0', port=80)
