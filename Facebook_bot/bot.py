import os
import json
import random
import requests
import sys
import time
from flask import Flask, request, redirect


PAGE_ACCESS_TOKEN = os.environ["PAGE_ACCESS_TOKEN"]
VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]
FB_ID = os.environ["FB_ID"]

app = Flask(__name__)

@app.route("/", methods=['GET'])
def verify():
    # Endpoint registration. Echos back
    # the 'hub.challenge' value
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world @ {}".format(time.localtime()), 200

@app.route('/', methods=['POST'])
def webhook():
    # Endpoint for processing incoming messaging events
    data = request.get_json()
    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    send_message(FB_ID, 
                        "resp message: {}. at {}. to {}".format(
                            message_text, str(time.localtime()), sender_id))

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200

def send_message(recipient_id, message_text):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", 
        params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(str(r.text))
        sys.stdout.flush()

def get_quote():
    quotes = [
        "Waste No More Time Arguing What A Good Man Should Be. Be One. - Marcus Aurelius",
        "If you are neutral in situations of injustice, you have chosen the side of the oppressor. - Desmond Tutu",
        "To people who care only about money and fame: one day you’ll meet a person who doesn’t care about any of those things and you’ll realize how poor you are. - Guy Kawasaki",
        "Give me six hours to chop down a tree and I will spend the first four sharpening the axe. - Abraham Lincoln",
        "The man who walks alone is likely to find himself in places no one has ever been before. Creativity in living is not without its attendant difficulties, for peculiarity breeds contempt. And the unfortunate thing about being ahead of your time is that when people finally realize you were right, they’ll say it was obvious all along - Alan Ashley-Pitt",
        "To live in the hearts we leave behind is not to die - Thomas Campbell (poet)",
        "It’s easy to stand in the crowd but it takes courage to stand alone - Mahatma Gandhi",
        "Early to bed and early to rise, makes a man healthy, wealthy and wise. – Benjamin Franklin",
        "The sky is not my limit… I am. – T.F. Hodge",
        "Man surprised me most about humanity. Because he sacrifices his health in order to make money. Then he sacrifices money to recuperate his health. And then he is so anxious about the future that he does not enjoy the present; the result being that he does not live in the present or the future; he lives as if he is never going to die, and then dies having never really lived. - The Dalai Lama",
        "It hurts because it matters - John Green",
        "Keep your eyes on the stars, and your feet on the ground - Teddy Roosevelt",
        "GDP measures everything, except what makes life worthwhile - Robert Kennedy, 1968",
        "When they say you can't, they show you their limits, not yours. – Kevin Keenoo",
        "We cannot become what we want to be by remaining what we are. – Max DePree",
        "The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking - Albert Einstein",
        "It is not the strongest of the species that survive, nor the most intelligent, but the one most responsive to change - Charles Darwin"
        ]
    return random.choice(quotes)

def quote_reminders():
    message = get_quote()
    send_message(FB_ID, message)
    return "Message {} sent to {}".format(
        message, FB_ID), 200



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)