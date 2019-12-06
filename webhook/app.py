from subprocess import check_output, PIPE, STDOUT, CalledProcessError
from flask import Flask, request
from dotenv import load_dotenv

import hashlib
import smtplib
import hmac
import json
import os

from send_mail import send_email

load_dotenv()
app = Flask(__name__)

@app.route('/611f19e75e9a482ecbafee68509d16e2a708711c3a311d95c4106ee7c4ab4c6c', methods=["POST"])
def webhook():
	try:
		key = bytes(os.getenv("WEBHOOK_SECRET"), 'utf-8')
		msg = json.dumps(request.json, separators=(',',':')).encode()
		signature = hmac.new(key, msg, hashlib.sha1).hexdigest()
		github_sig = request.headers.get('X-Hub-Signature')

		return "G:{0} == M:{1}".format(github_sig, signature)

		if github_sig == signature:
			try: 
				out = check_output(["/bin/sh", "./build.sh"], stderr=STDOUT)
			except CalledProcessError as e:
				out = e.output

			with open("debug.txt", "w") as f:
				f.write(out)

			#send_email(out)
			return "OK", 200
		else:
			return "NO", 401

	except Exception as e:
		return str(e), 401

if __name__ == '__main__':
    app.run(debug=False, port=9999)