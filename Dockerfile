FROM flask_env:v1
WORKDIR /flaskProjectTest
COPY . .
EXPOSE 5000
CMD flask run --host=0.0.0.0 --port=5000
#CMD gunicorn -c gun.conf app:app