# encoding: utf:8 
"""
@author: Joey
@contact: zengjiayi666@gmail.com
@file: upload.py
@time: 2022/4/18 12:35
"""
import os
import time

import flask
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory, \
    session
from flask_socketio import emit

from flaskr import socketio
from flaskr.db import get_db
from flaskr.cfg import PIC_BED

bp = Blueprint('upload', __name__)


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        user = request.form['user']
        room = request.form['room']
        form_time = request.form['time']
        print('测试upload', user, room)
        if file:
            filename = str(time.time())
            file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads', filename)
            file.save(file_path)
            flash('文件上传成功')
            db = get_db()
            db.execute(
                'INSERT INTO chat (content, time, send, room, content_type)'
                ' VALUES (?, ?, ?, ?, ?)',
                (PIC_BED + filename, form_time, user, room, 1)
            )
            datas = db.execute(
                'SELECT c.id, content, `time`, send, room, content_type'
                ' FROM chat c'
                ' WHERE c.room = ?',
                (str(room),)
            ).fetchall()
            data = [{'id': d[0], 'content': d[1], 'time': d[2], 'send': d[3], 'room': d[4],
                     'content_type': d[5]} for d in datas]
            db.commit()
            emit('rcvRoom',
                 {'data': data},
                 to=room, broadcast=False, namespace='/chat')
            return redirect(url_for('upload.upload'))
    return render_template('base.html')


@bp.route('/images/<filename>/')
def get_image(filename):
    file_url = 'http://0.0.0.0:5000/images/' + filename
    return flask.jsonify({'filename': file_url})
