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

bp = Blueprint('upload', __name__)


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = str(time.time()) + file.filename
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads', filename))
            flash('文件上传成功')
            return redirect(url_for('upload.upload'))
    return render_template('base.html')
