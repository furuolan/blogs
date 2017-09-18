import datetime
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    password = request.args.get("pwd")
    if password == "1234":
        response = "OK @ UTC {}".format(datetime.datetime.utcnow())
        return response, 200
    else:
        return "No pwd", 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)