from flask import Flask, request
from dotenv import load_dotenv

import hashlib
import hmac
import json
import os

load_dotenv()

app = Flask(__name__)

debug = False if os.getenv("DEBUG").lower() == "false" else True



@app.route('/611f19e75e9a482ecbafee68509d16e2a708711c3a311d95c4106ee7c4ab4c6c', methods=["POST"])
def webhook():
	try:
		key = bytes(os.getenv("WEBHOOK_SECRET"), 'utf-8')
		msg = json.dumps(request.json, separators=(',',':')).encode()
		signature = hmac.new(key, msg, hashlib.sha1).hexdigest()
		github_sig = request.headers.get('X-Hub-Signature')

		if github_sig == signature:
			return "OK", 200
		else:
			return "Who are you?", 500

	except Exception as e:
		return "404 Not Found", 404

if __name__ == '__main__':
    app.run(debug=True, port=9999)