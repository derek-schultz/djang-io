# djang-io
[python-socketio](https://github.com/miguelgrinberg/python-socketio) integration for Django

## Installation
```
pip install djang-io
```

Add djangio to your installed apps:
```
INSTALLED_APPS = (
    ...
    'djangio',
)
```

Create a `sockets.py` in any of your apps:
```
from djangio import listener

@listener.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)

@listener.on('chat message', namespace='/chat')
def message(sid, data):
    print("message ", data)
    listener.emit(sid, 'reply')
```

For more information on implementing your listeners, see [python-socketio](https://github.com/miguelgrinberg/python-socketio).

## Running
```
python manage.py runsocketserver 0.0.0.0:9000
```
The IP and port are optional.
