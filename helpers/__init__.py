from helpers.arguments import Arguments
from helpers.jwt_refresh_required import jwt_refresh_required
from helpers.model_encoder import MatchaJSONEncoder

import re

def is_email(email):
	return True if re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email) else False