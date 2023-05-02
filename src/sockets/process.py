import eventlet
import socketio
import queue
import threading
from settings import REDIS_HOST, REDIS_PORT, BINANCE_API_KEY, BINANCE_SECRET_KEY

q = queue.Queue()

eventlet.monkey_patch(socket=True, select=True,thread=True)

mgr = socketio.RedisManager('redis://{}:{}/0'.format(REDIS_HOST, REDIS_PORT))
socket = socketio.Server(client_manager=mgr, cors_allowed_origins='*', logger=True, engineio_logger=True)

app = socketio.WSGIApp(socket)


def send_message_all(event_name, event_value):
    socket.emit(event_name, event_value)


def send_message(sid, event_name, event_value):
    socket.emit(event_name, event_value, room=sid)


@socket.event
def connect(sid, environ, auth):
    print('connect ', sid)
    q.put({"sid": sid, "data": "HELLO WORLD"})


@socket.event
def disconnect(sid):
    print('disconnect ', sid)


def process_data():
    while True:
        if not q.empty():
            item = q.get()
            data = item.get('data', "")
            sid = item.get('sid', None)
            print("data here: %s" % data)
            eventlet.sleep(1)
            data = "data send from server " + str(data)
            send_message(sid, 'SERVER_UPDATE', data)


threading.Thread(target=process_data).start()

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
