#!/bin/bash

# short script that when run using sudo will create a new sudo user with the name of the
# user being the first argument
# run on linux (namely the cloud VM) using
# sudo ./create_user.sh admin1 
# for example 

#exits if no argument is supplied
if [ $# -eq 0 ]
then
	echo "No arguments supplied"
	exit 1
fi
echo $1
mkdir -p /home/$1/.ssh
touch /home/$1/.ssh/authorized_keys
useradd -d /home/$1 $1
usermod -aG sudo $1
chown -R $1:$1 /home/$1
chown root:root /home/$1
chmod 700 /home/$1/.ssh
chmod 644 /home/$1/.ssh/authorized_keys
passwd $1
sudo service ssh restart
