FROM python:3.10.4-alpine3.16

WORKDIR /webapp

COPY static/ static/
COPY database/ database/
COPY Userlogins/ Userlogins/
COPY manage.py manage.py
COPY requirements.txt requirements.txt
COPY run-container.sh run-container.sh

RUN pip3 install -r requirements.txt

EXPOSE 8000

VOLUME /webapp/db

CMD [ "/webapp/run-container.sh" ]
