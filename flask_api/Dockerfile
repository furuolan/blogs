FROM python:3.6.2

# update ubuntu installation
RUN apt-get -y update
RUN apt-get -y upgrade

# Create directories
RUN mkdir -p /mnt/app
ADD . /mnt/app
WORKDIR /mnt/app

# Generate app dependencies
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
