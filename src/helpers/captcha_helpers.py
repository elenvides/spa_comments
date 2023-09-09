import random
from django.conf import settings


def custom_challenge():
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    ret = "".join(random.choice(chars) for _ in range(settings.CAPTCHA_LENGTH))
    return ret.upper(), ret


