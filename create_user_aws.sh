#!/bin/bash

# short script that when run using sudo will
#create a new sudo user with the name of the
# user being the first argument
# run on linux (namely the cloud VM) using
# sudo ./create_user_aws.sh admin1 
# for example 
#remember to configure /etc/ssh/sshd_config 
#if getting Permission denied(public key)

#exits if script is not ran on root
if [ $EUID != 0 ]
then
	echo "please run as root. Use the sudo command"
	exit 1
fi

#exits if no argument is supplied
if [ $# -eq 0 ]
then
	echo "No arguments supplied"
	exit 1
fi
echo $1
useradd -d /home/$1 $1
mkdir -p /home/$1/.ssh
touch /home/$1/.ssh/authorized_keys
usermod -aG wheel $1
chown -R $1:$1 /home/$1
chown root:root /home/$1
chmod 755 /home/$1 
chmod 700 /home/$1/.ssh
chmod 644 /home/$1/.ssh/authorized_keys
passwd $1
sudo service sshd restart
