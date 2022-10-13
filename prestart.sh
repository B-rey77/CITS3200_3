#!/bin/sh
# generate dummy ssl certificate

SSL_CERT=/default-cert.pem
SSL_KEY=/default-cert.key
/make-dummy-cert $SSL_KEY $SSL_CERT

SSL_CERT_LE=/etc/letsencrypt/live/sslcert/fullchain.pem
SSL_KEY_LE=/etc/letsencrypt/live/sslcert/privkey.pem

if [ -f $SSL_CERT_LE ]; then
    SSL_CERT=$SSL_CERT_LE
    SSL_KEY=$SSL_KEY_LE
fi


export SSL_CERT SSL_KEY
/app/nginx-app.conf.sh > /etc/nginx/conf.d/nginx.conf

# apply migrations, or wait until DB is started up then try again
/app/manage.py migrate || sleep 10 && /app/manage.py migrate

/app/manage.py createsuperuser --no-input --first_name CITS3200 --last_name Admin --email $ADMIN_EMAIL || echo 'Superuser already exists'

