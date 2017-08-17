# run in docker container
virtualenv my_env;
source my_env/bin/activate;
pip install -r requirements.txt;
cp keys/credentials ~/.aws;
cp keys/config ~/.aws;