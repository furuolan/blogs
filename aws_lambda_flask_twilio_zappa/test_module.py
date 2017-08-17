import os
import json
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def test():
    return "Test response 2 OK"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)