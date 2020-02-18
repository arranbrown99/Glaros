#!/bin/bash

pwd=$(pwd)
[ -d logs ] || mkdir logs

############
# GUNICORN #
############

python3 -c "import socket as s; sock = s.socket(s.AF_UNIX); sock.bind('$(pwd)/run/gunicorn.sock')"
touch logs/gunicorn.log
gunicorn dashboard.wsgi:application --workers 3 --bind=unix:$(pwd)/run/gunicorn.sock --log-file logs/gunicorn.log &

#########
# NGINX #
#########

# Install dependencies
apt-get -y install nginx
# Set up
mkdir -p nginx
touch nginx/dashboard.conf


# This is done dynamically to accomodate different paths
cat > nginx/dashboard.conf << EOF
upstream dashboard_gunicorn {
    server unix:$pwd/run/gunicorn.sock fail_timeout=0;
}
server {
    listen 80;
    server_name glaros.uk;
    client_max_body_size 5M;
    keepalive_timeout 5;
    underscores_in_headers on;
    access_log $(pwd)/logs/nginx-access.log;
    error_log $(pwd)/logs/nginx-error.log;
    location /media  {
        alias $(pwd)/media;
    }
    location /static {
        alias $(pwd)/static;
    }
    # location /static/admin {
    #   alias $/site-packages/django/contrib/admin/static/admin/;
    # }
    # Remove comments to enable https (although we dont have certs)
    #location / {
    #    rewrite ^ https://\$http_host\$request_uri? permanent;
    #}
    # To make the site pure HTTPS, comment the following section while
    # uncommenting the above section. Also uncoment the HTTPS section
    location / {
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$http_host;
        proxy_redirect off;
        proxy_pass http://dashboard_gunicorn;
    }
}
EOF

#Linking the files..
ln -sf $(pwd)/nginx/dashboard.conf /etc/nginx/sites-enabled/dashboard
# Reloading nginx
service nginx restart