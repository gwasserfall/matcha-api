from flask import Flask
from dotenv import load_dotenv

import os

load_dotenv()

app = Flask(__name__)

debug = False if os.getenv("DEBUG").lower() == "false" else True

@app.route('/webhooks/611f19e75e9a482ecbafee68509d16e2a708711c3a311d95c4106ee7c4ab4c6c', methods=["POST"])
def webhook():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=debug, port=9999)