from Handler import *
import hmac

cookie_secret = "fight_club"

def hash_str(s):
	return hmac.new(cookie_secret,s).hexdigest()

def make_secure_val(s):
	return "%s|%s" % (s,hash_str(s))

def check_secure_val(h):
	val=h.split('|')[0]
	if h==make_secure_val(val):
		return val
