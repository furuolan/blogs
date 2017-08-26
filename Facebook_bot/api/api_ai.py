import datetime
import json
import os
import requests

from api.google_timezone import city_time

APIAI_BEARER = os.environ["APIAI_BEARER"]

def parse_text(user_text):
    url_template = "https://api.api.ai/v1/query?v=20150910&query={}&lang=en&sessionId={}"
    url = url_template.format(user_text, datetime.datetime.utcnow())
    headers = {"Authorization":  APIAI_BEARER}
    resp = requests.get(url, headers=headers)
    resp = resp.json()
    city = None
    try:
        city = resp['result']['parameters']['geo-city']
    except:
        print("API user string not understood by api.ai")
    if not city:
        return "Sorry, I couldn't understand that question"
    else:
        time_now = city_time(city)
        return "Current time in {} is {}".format(city, time_now)