# encoding: utf:8 
"""
@author: Joey
@contact: zengjiayi666@gmail.com
@file: chat.py
@time: 2022/4/18 21:37
"""
import time

import flask
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_cors import cross_origin

from flaskr.db import get_db
from flask_socketio import emit, join_room, leave_room, rooms
from . import socketio


bp = Blueprint('chat', __name__, url_prefix='/chat')
online_users = []


@bp.route('/send', methods=['POST'])
@cross_origin()
def chat():
    if request.method == 'POST':
        print('看看request的content', request.form['content'])
        db = get_db()
        content = request.form['content']
        send_time = request.form['time']
        send = request.form['user']
        room = request.form['room']
        db.execute(
            'INSERT INTO chat (content, time, send, room)'
            ' VALUES (?, ?, ?, ?)',
            (content, send_time, send, room)
        )
        contents = db.execute(
            'SELECT c.id, content, `time`, send'
            ' FROM chat c WHERE c.room = -1'
        ).fetchall()
        contents = [{'id': content[0], 'content': content[1], 'time': content[2], 'send': content[3]} for content in contents]
        db.commit()
    return flask.jsonify({"code": 200, "data": contents, "msg": "success"})


@bp.route('/sendFile', methods=['POST'])
@cross_origin()
def sendFile():
    print('调用了sendFile方法')
    if request.method == 'POST':
        print('看看request的content', request.form['content'])
        socketio.emit('rcvFile', request.form['content'], room=request.form['room'])


@socketio.on('broadcast', namespace='/chat')
def broadcast(room):
    print('调用了broadcast')
    db = get_db()
    contents = db.execute(
        'SELECT c.id, content, `time`, send, room'
        ' FROM chat c'
        ' WHERE c.room = -1'
    ).fetchall()
    contents = [{'id': content[0], 'content': content[1], 'time': content[2], 'send': content[3], 'room':content[4]} for content in
                contents]
    data = {'code': 200, 'data': contents, 'total_user': len(online_users)}
    print('看看room', room)
    socketio.emit('message', data, namespace='/chat', to=room['room'], broadcast=False)


@socketio.on('connect', namespace='/chat')
def test_connect():
    online_users.append(request.sid)
    print('Client connected')
    return flask.jsonify({"code": 200, "msg": len(online_users)})


@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    print('Client disconnected')
    online_users.remove(request.sid)
    try:
        broadcast()
    except Exception as e:
        print(e)
        print('以上是错误日志')
    return flask.jsonify({"code": 200, "msg": len(online_users)})


@socketio.on('join', namespace='/chat')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    db = get_db()
    datas = db.execute(
        'SELECT c.id, content, `time`, send, room'
        ' FROM chat c'
        ' WHERE c.room = ?',
        (str(message['room']),)
    ).fetchall()
    data = [{'id': d[0], 'content': d[1], 'time': d[2], 'send': d[3], 'room': d[4]} for d in datas]
    data.append({'id': 0, 'content': '有人加入了房间', 'time': time.localtime(), 'send': 'adminnnn', 'room': message['room']})
    print('join的data', data)
    emit('rcvRoom',
         {'data': data, 'count': session['receive_count']},
         to=message['room'], broadcast=False)
    print('调用了join Client %s joined room %s' % (request.sid, message['room']))


@socketio.on('send2Room', namespace='/chat')
def send2Room(message):
    # print('调用了send2Room, message是', message)
    session['receive_count'] = session.get('receive_count', 0) + 1
    db = get_db()
    db.execute(
        'INSERT INTO chat (content, time, send, room)'
        ' VALUES (?, ?, ?, ?)',
        (message['message']['content'], message['message']['time'], message['message']['user'], message['message']['room'])
    )
    datas = db.execute(
        'SELECT c.id, content, `time`, send, room'
        ' FROM chat c'
        ' WHERE c.room = ?',
        (str(message['message']['room']),)
    ).fetchall()
    data = [{'id': d[0], 'content': d[1], 'time': d[2], 'send': d[3], 'room': d[4]} for d in datas]
    db.commit()
    emit('rcvRoom',
         {'data': data, 'count': session['receive_count']},
         to=message['message']['room'], broadcast=False)


@socketio.on('leave', namespace='/chat')
def leave(message):
    print('调用了leave Client %s left room %s' % (request.sid, message['room']))
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    # emit('my_response',
    #      {'data': 'In rooms: ' + ', '.join(rooms()),
    #       'count': session['receive_count']})
