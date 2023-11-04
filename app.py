from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_letters

app = Flask(__name__)
app.config["SECRET KEY"] = 'secret!'
socketio = SocketIO(app)

rooms = {}

def generate_unqiue_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_letters)

        if code not in rooms:
            break

    return code

@app.get("/")
def index():
    return render_template('index.html')


@app.post("/")
def create_room():
    name = request.form.get('name')
    code = request.form.get('code')
    join = request.form.get('join', False)
    create = request.form.get('create', False)

    if not name:
        return render_template('index.html', error="Please enter name...", code=code, name=name)

    if join != False and not code:
        return render_template('index.html', error="Please enter room code...", code=code, name=name)

    room = code
    if create != False:
        room = generate_unqiue_code(4)
        rooms[room] = {'members': 0, 'messages': []}
    elif code not in rooms:
        return render_template('index.html', error="Room does not exist...", code=code, name=name)

    session["room"] = room
    session["name"] = name

    return redirect(url_for("room"))

@app.get('/room')
def room():
    return render_template("room.html")

if __name__ == '__main__':
    socketio.run(app, debug=True)
