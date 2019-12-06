from dotenv import load_dotenv

import os

load_dotenv()

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

		print ('Test Email sent!!')
	except:
		print ('Something went wrong...')