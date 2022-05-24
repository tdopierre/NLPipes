import socketio


def get_socketio_client_address():
    import os
    return os.environ.get("SOCKETIO_SERVER_ADDRESS", "http://0.0.0.0:8002")


client = socketio.Client()
client.connect(get_socketio_client_address())
