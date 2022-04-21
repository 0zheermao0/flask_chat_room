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
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flaskr.db import get_db

bp = Blueprint('upload', __name__)


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        user = request.form['user']
        room = request.form['room']
        print('测试upload', user, room)
        if file:
            filename = str(time.time()) + file.filename
            file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads', filename)
            file.save(file_path)
            flash('文件上传成功')
            db = get_db()
            db.execute(
                'INSERT INTO file_path (file_name, file_path, user, room)'
                ' VALUES (?, ?, ?, ?)',
                (filename, file_path, '啊吧啊吧', '-1')
            )
            db.commit()
            return redirect(url_for('upload.upload'))
    return render_template('base.html')
