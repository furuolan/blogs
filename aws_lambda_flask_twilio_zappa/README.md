# Flask + Twilio phone + AWS Lambda + Zappa
### [https://www.twilio.com/docs/quickstart/python/sms/sending-via-rest#send-sms-via-library](https://www.twilio.com/docs/quickstart/python/sms/sending-via-rest#send-sms-via-library)

## Instructions to run code in Docker:
  - Save AWS credentials in keys/credentials and keys/config. See (http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)[http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html]

  - Update environmental variables and Twilio tokens in "docker-compose environment:" and "zappa_settings.json"

  - Build docker image, start and SSH into container, install dependencies:

        bash run.sh;
        bash requirements.sh;
        source my_env/bin/activate;

  - Test Flask app
  
        python test_module.py;

  - Run sms app (in browser navigate to 127.0.0.1/sms_send to send sms)
  
        python sms.py;

## Instructions to deploy to AWS Lambda (https://github.com/Miserlou/Zappa)[https://github.com/Miserlou/Zappa]:

        zappa init
        zappa deploy

## Instructions to update to AWS Lambda code:

        zappa update