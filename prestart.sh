#!/bin/sh
# generate dummy ssl certificate

SSL_CERT=/default-cert.pem
SSL_KEY=/default-cert.key
/make-dummy-cert $SSL_KEY $SSL_CERT

export SSL_CERT=/etc/letsencrypt/live/sslcert/fullchain.pem
export SSL_KEY=/etc/letsencrypt/live/sslcert/privkey.pem

certbot certonly -t -d ${DJANGO_HOSTNAME} --non-interactive --agree-tos -m ${LETS_ENCRYPT_EMAIL} --cert-name sslcert --webroot -w /well_known --test-cert

/app/nginx-app.conf.sh > /etc/nginx/conf.d/nginx.conf

# apply migrations, or wait until DB is started up then try again
/app/manage.py migrate || sleep 10 && /app/manage.py migrate

