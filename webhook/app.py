from subprocess import Popen, PIPE, STDOUT
from flask import Flask, request
from dotenv import load_dotenv

import hashlib
import smtplib
import hmac
import json
import os


load_dotenv()
app = Flask(__name__)
debug = False if os.getenv("DEBUG").lower() == "false" else True


def send_email(output):
	gmail_user = os.getenv("GMAIL_USER")
	gmail_password = os.getenv("GMAIL_PASS")

	sent_from = gmail_user
	to = [gmail_user]
	subject = 'Matcha:: Build Report'
	body = output

	email_text = """\
	From: %s
	To: %s
	Subject: %s

	%s
	""" % (sent_from, ", ".join(to), subject, body)

	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(gmail_user, gmail_password)
		server.sendmail(sent_from, to, email_text)
		server.close()

		print ('Email sent!!')
	except:
		print ('Something went wrong...')

@app.route('/611f19e75e9a482ecbafee68509d16e2a708711c3a311d95c4106ee7c4ab4c6c', methods=["POST"])
def webhook():
	try:
		key = bytes(os.getenv("WEBHOOK_SECRET"), 'utf-8')
		msg = json.dumps(request.json, separators=(',',':')).encode()
		signature = hmac.new(key, msg, hashlib.sha1).hexdigest()
		github_sig = request.headers.get('X-Hub-Signature')

		if github_sig == signature:

			p = Popen("build.sh", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
			output = p.stdout.read()
			send_mail(output)

			return "OK", 200
		else:
			return "Who are you?", 500

	except Exception as e:
		return "404 Not Found", 404

if __name__ == '__main__':
    app.run(debug=True, port=9999)