#!/bin/sh
cat <<EOF
server {
    listen 443 ssl;
    server_name ${DJANGO_HOSTNAME};

    ssl_certificate     ${SSL_CERT};
    ssl_certificate_key ${SSL_KEY};

    # from https://gist.github.com/gavinhungry/7a67174c18085f4a23eb
    ssl_protocols TLSv1.3 TLSv1.2;
    ssl_prefer_server_ciphers on;
    ssl_ecdh_curve secp521r1:secp384r1;
    ssl_ciphers EECDH+AESGCM:EECDH+AES256;

    ssl_dhparam /etc/ssl/dhparam.pem;

    ssl_session_cache shared:TLS:2m;
    ssl_session_timeout  10m;
    ssl_buffer_size 4k;

    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 1.1.1.1 1.0.0.1 [2606:4700:4700::1111] [2606:4700:4700::1001]; # Cloudflare

    # Set HSTS to 365 days
    #add_header Strict-Transport-Security 'max-age=31536000; includeSubDomains; preload' always;

    location / {
        uwsgi_pass unix:///tmp/uwsgi.sock;

        uwsgi_param  QUERY_STRING       \$query_string;
        uwsgi_param  REQUEST_METHOD     \$request_method;
        uwsgi_param  CONTENT_TYPE       \$content_type;
        uwsgi_param  CONTENT_LENGTH     \$content_length;

        uwsgi_param  REQUEST_URI        \$request_uri;
        uwsgi_param  PATH_INFO          \$document_uri;
        uwsgi_param  DOCUMENT_ROOT      \$document_root;
        uwsgi_param  SERVER_PROTOCOL    \$server_protocol;
        uwsgi_param  REQUEST_SCHEME     \$scheme;
        uwsgi_param  HTTPS              \$https if_not_empty;

        uwsgi_param  REMOTE_ADDR        \$remote_addr;
        uwsgi_param  REMOTE_PORT        \$remote_port;
        uwsgi_param  SERVER_PORT        \$server_port;
        uwsgi_param  SERVER_NAME        \$server_name;

    }

    location /static {
        alias /app/djstatic;
    }

    location /.well-known {
        root /well_known;
    }
}

server {
    listen 80;
    server_name ${DJANGO_HOSTNAME};
    root /srv/wwwroot;

    return 301 https://${DJANGO_HOSTNAME}\$request_uri;
}
EOF