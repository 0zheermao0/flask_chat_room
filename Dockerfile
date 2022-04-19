FROM python:3.8
WORKDIR /flaskProjectTest
COPY * .
RUN pip install flask gunicorn gevent flask_socketio
EXPOSE 5000
CMD gunicorn -w 2 app:app