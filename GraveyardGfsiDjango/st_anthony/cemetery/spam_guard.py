"""Light spam protection for the public contact and newsletter forms.

Each form carries a hidden "website" field that people never see (bots fill it)
and a signed timestamp. check_submission() returns:
  'ok'      - looks like a person
  'bot'     - trap filled, stamp missing/forged, or sent back implausibly fast
  'expired' - genuine stamp, but the page was left open too long
IP-based rate limiting isn't used: behind Render's proxy the client IP comes
from a header that can be spoofed.
"""
import time

from django.core import signing

SALT = 'cemetery.spam-guard'
MIN_SECONDS = 2
MAX_AGE = 7 * 24 * 60 * 60
TRAP_FIELD = 'website'
STAMP_FIELD = 'form_stamp'


def make_stamp():
    return signing.dumps(int(time.time()), salt=SALT)


def check_submission(post):
    if post.get(TRAP_FIELD):
        return 'bot'
    try:
        issued = signing.loads(post.get(STAMP_FIELD, ''), salt=SALT, max_age=MAX_AGE)
    except signing.SignatureExpired:
        return 'expired'
    except signing.BadSignature:
        return 'bot'
    if time.time() - int(issued) < MIN_SECONDS:
        return 'bot'
    return 'ok'
