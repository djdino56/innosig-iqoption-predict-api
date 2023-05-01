import eventlet
import socketio
from settings import REDIS_HOST, REDIS_PORT
eventlet.monkey_patch(socket=True, select=True, thread=True)
mgr = socketio.RedisManager('redis://{}:{}/0'.format(REDIS_HOST, REDIS_PORT))
socket = socketio.Server(client_manager=mgr, cors_allowed_origins='*', logger=True, engineio_logger=True)
app = socketio.WSGIApp(socket)
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
