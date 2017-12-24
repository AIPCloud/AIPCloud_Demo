# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = None

import time
from flask import Flask, render_template
import socketio
import grpc

import new_demo_portal_pb2
import new_demo_portal_pb2_grpc

sio = socketio.Server(logger=True, async_mode=async_mode)
app = Flask(__name__)
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)
app.config['SECRET_KEY'] = 'secret!'
_NEW_DEMO_PORTAL_PORT = 50050
thread = None
audioChunks = []


def signal_generator():
    global audioChunks
    while True:
        sio.sleep(0.5)
        if len(audioChunks) > 0:
            print("Yielding first chunk in line.")
            chunk = audioChunks[0]
            yield new_demo_portal_pb2.Request(
                signal=chunk["signal"],
                sample_rate=chunk["sample_rate"])
            audioChunks.pop(0)

def emit_data_thread(iterator):
    while True:
        sio.sleep(0.5)
        try:
            print("Testing if new data arrived.")
            print(iterator._next())
            # sio.emit('my response', {'data': message['data']}, room=sid,
            #          namespace='/test')
        except StopIteration:
            pass

def grpc_client_thread():
    ########## gRPC ###########
    channel = grpc.insecure_channel(
        'localhost:{}'.format(_NEW_DEMO_PORTAL_PORT))
    stub = new_demo_portal_pb2_grpc.NewDemoPortalStub(channel)
    print("Connection with server established.")
    return stub.Analyze(signal_generator())


@app.route('/')
def index():
    return render_template('index.html')


@sio.on('audio_buffer', namespace='/new_demo_portal')
def receive_audio_buffer(sid, message):
    global Signal, thread
    # if thread is None:
    #     thread = sio.start_background_task(background_thread)
    #     print("Backgroud thread started.")

    signal = list(message["signal"].values())
    sample_rate = message["sample_rate"]
    audioChunks.append({
        "signal": signal,
        "sample_rate": sample_rate
    })


@sio.on('my event', namespace='/test')
def test_message(sid, message):
    sio.emit('my response', {'data': message['data']}, room=sid,
             namespace='/test')


@sio.on('my broadcast event', namespace='/test')
def test_broadcast_message(sid, message):
    sio.emit('my response', {'data': message['data']}, namespace='/test')


@sio.on('join', namespace='/test')
def join(sid, message):
    sio.enter_room(sid, message['room'], namespace='/test')
    sio.emit('my response', {'data': 'Entered room: ' + message['room']},
             room=sid, namespace='/test')


@sio.on('leave', namespace='/test')
def leave(sid, message):
    sio.leave_room(sid, message['room'], namespace='/test')
    sio.emit('my response', {'data': 'Left room: ' + message['room']},
             room=sid, namespace='/test')


@sio.on('close room', namespace='/test')
def close(sid, message):
    sio.emit('my response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'], namespace='/test')
    sio.close_room(message['room'], namespace='/test')


@sio.on('my room event', namespace='/test')
def send_room_message(sid, message):
    sio.emit('my response', {'data': message['data']}, room=message['room'],
             namespace='/test')


@sio.on('disconnect request', namespace='/test')
def disconnect_request(sid):
    sio.disconnect(sid, namespace='/test')


@sio.on('connect', namespace='/test')
def test_connect(sid, environ):
    sio.emit('my response', {'data': 'Connected', 'count': 0}, room=sid,
             namespace='/test')


@sio.on('disconnect', namespace='/test')
def test_disconnect(sid):
    print('Client disconnected')


if __name__ == '__main__':

    if sio.async_mode == 'threading':
        print("Threading")
        # deploy with Werkzeug
        app.run(threaded=True)
    elif sio.async_mode == 'eventlet':
        print("Eventlet")
        # deploy with eventlet
        import eventlet
        import eventlet.wsgi
        from eventlet import tpool
        response_iterator = grpc_client_thread()
        # tpool.execute(emit_data_thread, response_iterator)
        sio.start_background_task(emit_data_thread, response_iterator)

        print("Backgroud thread started.")
        eventlet.wsgi.server(eventlet.listen(('', 5001)), app)
    elif sio.async_mode == 'gevent':
        print("Gevent")
        # deploy with gevent
        from gevent import pywsgi
        try:
            from geventwebsocket.handler import WebSocketHandler
            websocket = True
        except ImportError:
            websocket = False
        if websocket:
            pywsgi.WSGIServer(('', 5001), app,
                              handler_class=WebSocketHandler).serve_forever()
        else:
            pywsgi.WSGIServer(('', 5001), app).serve_forever()
    elif sio.async_mode == 'gevent_uwsgi':
        print("Gevent UWSGI")
        print('Start the application through the uwsgi server. Example:')
        print('uwsgi --http :5001 --gevent 1000 --http-websockets --master '
              '--wsgi-file app.py --callable app')
    else:
        print('Unknown async_mode: ' + sio.async_mode)
