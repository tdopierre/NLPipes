import eventlet
import socketio

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)


@sio.on('message')
def handle_message(sid, data):
    print('message', data)
    sio.emit('message', data)


@sio.on('progress-update')
def handle_progress_update(sid, data):
    print('progress update', data)
    sio.emit('progress-update', data)


@sio.on('new-process')
def handle_new_process(sid, data):
    print('new process', data)
    sio.emit('new-process', data)


@sio.on('delete-process')
def handle_delete_process(sid, data):
    print('delete process', data)
    sio.emit('delete-process', data)


@sio.event
def connect(sid, environ):
    print(sid, 'connected')


@sio.event
def disconnect(sid):
    print(sid, 'disconnected')


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(('', 8002)), app)
