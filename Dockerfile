FROM tiangolo/uwsgi-nginx:python3.10

#WORKDIR /webapp
COPY requirements.txt /app/requirements.txt

COPY static/ /app/static/
COPY database/ /app/database/
COPY Userlogins/ /app/Userlogins/
COPY manage.py /app/manage.py
COPY uwsgi-app.ini /app/uwsgi.ini
# override uwsgi-nginx generated config
COPY nginx.conf /app/nginx.conf
COPY make-dummy-cert /

RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends openssl certbot;

RUN /app/manage.py collectstatic
RUN /app/manage.py check

COPY prestart.sh /app/prestart.sh
COPY nginx-certbot.conf /etc/nginx/default.d/certbot.conf
COPY dhparam.pem /etc/ssl/dhparam.pem
# override uwsgi-nginx generated file
COPY nginx-app.conf.sh /app/nginx-app.conf.sh

ENV DB_HOST localhost

VOLUME /etc/letsencrypt
VOLUME /var/lib/letsencrypt
#VOLUME /well_known

#VOLUME /var/lib/postgresql/data

#CMD [ "/webapp/run-container.sh" ]
