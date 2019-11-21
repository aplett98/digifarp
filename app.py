from flask import Flask, request, jsonify
app = Flask(__name__)

import sqlite3

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/farp', methods=['POST', 'GET'])
def create_farp():
    conn = sqlite3.connect('digifarp.db')
    c = conn.cursor()
    if request.method == 'GET':
        rows = list(c.execute('SELECT * FROM farps'))
        conn.close()
        return jsonify(rows)
    if not request.json or not 'name' in request.json:
        abort(400)

    name = request.json['name']
    items = [
        (None, name, item['amount'], item['description'], item['category'], item['department'])
        for item in request.json.get('items', [])
    ]
    c.executemany('INSERT INTO farps VALUES (?,?,?,?,?,?)', items)
    conn.commit()
    rows = list(c.execute('SELECT * FROM farps'))
    conn.close()

    return jsonify(rows)
