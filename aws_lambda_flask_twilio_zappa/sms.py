import os
import json
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = Flask(__name__)

@app.route("/sms_reply", methods=['GET', 'POST'])
def sms_reply():
    """
    Sending text to twilio number, return response resp.message
    bank to sender
    See: https://www.twilio.com/docs/quickstart/python/sms#overview
    """
    resp = MessagingResponse()
    resp.message("Response from server")
    return str(resp)

@app.route("/sms_send", methods=['GET', 'POST'])
def sms_send():
    account_sid = os.environ["ACCOUNT_SID"]
    auth_token = os.environ["AUTH_TOKEN"]
    client = Client(account_sid, auth_token)
    client.messages.create(
        to = os.environ["MY_NUMBER"],
        from_ = os.environ["TWILIO_NUMBER"],
        body = "test message"
    )
    return "Message sent. OK"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)