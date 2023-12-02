from bson import json_util
import json

from flask import Flask, render_template
from flask_socketio import SocketIO
from logger import Logger

app = Flask(__name__)
app.config['SECRET_KEY'] = 'S3cr3t!'
socket = SocketIO(app)

log = Logger()

@app.route('/')
def index():
    return render_template('index.html', data_history=json.dumps(log.read_last_lines(20)), vIdeal=log.getVIdeal(), intVaria=log.getIntVaria())

@socket.on('update')
def vlIdeal_update(msg):
    global log  # Usando a variável global log
    if "vlIdeal" in msg :
        log.setVIdeal(float(msg['vlIdeal']))
    if "intVaria" in msg:
        log.setIntVaria(float(msg['intVaria']))
    print('Received message: ', msg)
    
def data_update(data):
    print(data)
    socket.emit('data_update', json.dumps(data, default=json_util.default))

if __name__ == '__main__':
    log.on_data_updated(data_update)
    app.run(host='0.0.0.0')

