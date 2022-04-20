# encoding: utf:8 
"""
@author: Joey
@contact: zengjiayi666@gmail.com
@file: app.py
@time: 2022/4/19 12:25
"""
from flask_cors import CORS

from flaskr import create_app, socketio


app = create_app()
if __name__ == '__main__':
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
