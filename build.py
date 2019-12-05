from flask import Flask
from dotenv import load_dotenv

import os

load_dotenv()

app = Flask(__name__)

debug = False if os.getenv("DEBUG").lower() == "false" else True

@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=debug, port=9999)