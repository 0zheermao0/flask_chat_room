# encoding: utf:8 
"""
@author: Joey
@contact: zengjiayi666@gmail.com
@file: chat.py
@time: 2022/4/18 21:37
"""
import flask
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_cors import cross_origin

from flaskr.db import get_db
from flask_socketio import emit, join_room, leave_room
from . import socketio


bp = Blueprint('chat', __name__, url_prefix='/chat')
online_users = []


@bp.route('/send', methods=['POST'])
@cross_origin()
def chat():
    if request.method == 'POST':
        db = get_db()
        content = request.form['content']
        send_time = request.form['time']
        send = request.form['send']
        db.execute(
            'INSERT INTO chat (content, time, send)'
            ' VALUES (?, ?, ?)',
            (content, send_time, send)
        )
        contents = db.execute(
            'SELECT c.id, content, `time`, send'
            ' FROM chat c'
        ).fetchall()
        contents = [{'id': content[0], 'content': content[1], 'time': content[2], 'send': content[3]} for content in contents]
        db.commit()
    return flask.jsonify({"code": 200, "data": contents, "msg": "success"})


@socketio.on('broadcast', namespace='/chat')
def broadcast():
    print('调用了broadcast')
    db = get_db()
    contents = db.execute(
        'SELECT c.id, content, `time`, send'
        ' FROM chat c'
    ).fetchall()
    contents = [{'id': content[0], 'content': content[1], 'time': content[2], 'send': content[3]} for content in
                contents]
    data = {'code': 200, 'data': contents, 'total_user': len(online_users)}
    socketio.emit('message', data, namespace='/chat')


@socketio.on('connect', namespace='/chat')
def test_connect():
    online_users.append(request.sid)
    print('Client connected')
    return flask.jsonify({"code": 200, "msg": len(online_users)})


@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    print('Client disconnected')
    online_users.remove(request.sid)
    broadcast()
    return flask.jsonify({"code": 200, "msg": len(online_users)})
