from helpers.arguments import Arguments
import re

def is_email(email):
	return True if re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email) else False