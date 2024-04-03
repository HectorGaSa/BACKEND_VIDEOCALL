from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

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
        #emit('joined_room', {'message': f'{userId} se ha unido a la sala {room}'})
        emit('joined_room', {'message': f'{username} se ha unido a la sala {room}'}, to=room)
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
