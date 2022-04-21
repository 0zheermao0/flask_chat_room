FROM python:3.8
WORKDIR /flaskProjectTest
COPY . .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gunicorn gevent
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
EXPOSE 5000
CMD flask run --host=0.0.0.0 --port=5000
#CMD gunicorn -c gun.conf app:app