FROM python:3.10.4-alpine3.16

WORKDIR /webapp

COPY static/ static/
COPY database/ database/
COPY Userlogins/ Userlogins/
COPY manage.py manage.py
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD [ "/webapp/manage.py", "runserver", "0.0.0.0:8000" ]
