FROM python:3.6.2

USER root

# update ubuntu installation
RUN apt-get -y update
RUN apt-get -y upgrade
RUN pip install virtualenv

# switch back to user
USER $NB_USER

# Create app directory
RUN mkdir -p /mnt/app
WORKDIR /mnt/app

# AWS directory
RUN mkdir ~/.aws

EXPOSE 5000
