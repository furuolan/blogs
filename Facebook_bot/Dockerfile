FROM python:3.6.2

# update ubuntu installation
RUN apt-get -y update
RUN apt-get -y upgrade

# Create directories
RUN mkdir -p /mnt/app
RUN mkdir ~/.aws
ADD . /mnt/app
WORKDIR /mnt/app

# Generate app dependencies
RUN pip install -r requirements.txt
RUN cp keys/credentials ~/.aws
RUN cp keys/config ~/.aws

EXPOSE 5000

CMD ["python", "bot.py"]
