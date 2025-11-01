import string
import random
from validators import url as validate_url

ALPHABET = string.ascii_letters + string.digits

def generate_short_id(length=6):
    # secure random choice
    return ''.join(random.SystemRandom().choice(ALPHABET) for _ in range(length))

def is_valid_url(url):
    # ensure scheme exists; validators.url returns True for valid urls
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return validate_url(url), url
