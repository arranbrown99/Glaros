#!/bin/bash

############
#  DJANGO  #
############

echo "Beginning Django configuration..."

python3 manage.py makemigrations --no-input
python3 manage.py migrate
python3 manage.py collectstatic --no-input

echo "Django configuration complete"

pwd=$(pwd)
my_ip=$(curl --silent http://checkip.amazonaws.com)
domain_ip=$(dig glaros.uk +short)

echo "Machine IP: $my_ip Domain IP: $domain_ip"
while [ $my_ip != $domain_ip ]
do
    echo "Waiting for DNS propagation..."
    sleep 10
    domain_ip=$(dig glaros.uk +short)
    echo "machine IP: $my_ip domain IP: $domain_ip"
done

echo "Domain propagated, beginning web configuration process..."

echo "Initialising required directory structure..."

[ -d logs ] || mkdir logs
[ -d run ] || mkdir run
[ -d nginx ] || mkdir nginx


############
# GUNICORN #
############

echo "Beginning Gunicorn configuration..."

python3 -c "import socket as s; sock = s.socket(s.AF_UNIX); sock.bind('$(pwd)/run/gunicorn.sock')"
touch logs/gunicorn.log
gunicorn3 dashboard.wsgi:application --workers 3 --bind=unix:$(pwd)/run/gunicorn.sock --log-file logs/gunicorn.log &

echo "Gunicorn configuration complete"

###########
#  NGINX  #
###########

echo "Beginning NGINX configuration..."

# Set up
[ -d nginx ] || mkdir nginx
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

#Update conf for su
cat > /etc/nginx/nginx.conf << EOF
user root;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
        worker_connections 768;
        # multi_accept on;
}

http {

        ##
        # Basic Settings
        ##

        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        types_hash_max_size 2048;
        # server_tokens off;

        # server_names_hash_bucket_size 64;
        # server_name_in_redirect off;

        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        ##
        # SSL Settings
        ##

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
        ssl_prefer_server_ciphers on;

        ##
        # Logging Settings
        ##

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        ##
        # Gzip Settings
        ##

        gzip on;

        # gzip_vary on;
        # gzip_proxied any;
        # gzip_comp_level 6;
        # gzip_buffers 16 8k;
        # gzip_http_version 1.1;
        # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

        ##
        # Virtual Host Configs
        ##

        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
}


#mail {
#       # See sample authentication script at:
#       # http://wiki.nginx.org/ImapAuthenticateWithApachePhpScript
#
#       # auth_http localhost/auth.php;
#       # pop3_capabilities "TOP" "USER";
#       # imap_capabilities "IMAP4rev1" "UIDPLUS";
#
#       server {
#               listen     localhost:110;
#               protocol   pop3;
#               proxy      on;
#       }
#
#       server {
#               listen     localhost:143;
#               protocol   imap;
#               proxy      on;
#       }
#}
EOF

# Reloading nginx
service nginx restart

echo "NGINX configuration complete"
echo "Successfully deployed"

exit 0
