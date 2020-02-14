#!/bin/bash
#setup env variables
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
export DEBUG=0
export DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,glaros.uk
export SECRET_KEY=alpha_beta-please-change-me
export DASHBOARD_PATH=$(pwd)/dashboard
#configure nginx
apt update
apt install nginx -y
systemctl stop nginx
ufw allow 'Nginx HTTP'
rm /etc/nginx/conf.d/default.conf
touch /etc/nginx/sites-available/dashboard
cp ./nginx/nginx.conf /etc/nginx/sites-available/dashboard
ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled
systemctl start nginx

#enable gunicorn
cd $DASHBOARD_PATH
# python manage.py flush --no-input
# python manage.py migrate
# python manage.py collectstatic --no-input --clear
gunicorn dashboard.wsgi:application --bind 0.0.0.0:8000