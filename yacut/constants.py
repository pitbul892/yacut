import string

MAX_SHORT_LINK = 16
MAX_GENERATE_LiNK = 6
PATTERN_FOR_SHORT_LINK = f'^[a-zA-Z0-9]{{1,{MAX_SHORT_LINK}}}$'
CHARACTERS = string.ascii_letters + string.digits
MAX_ATTEMPTS = 500