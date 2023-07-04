from flask import Flask
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'This is an example response from the API'}
    emit('data_response', data)
    return {'success': True}

if __name__ == '_main_':
    socketio.run(app)