from random import choices
from string import ascii_letters, digits


def get_unique_short_id():
    for _ in range(5):
        random_url = ''.join(choices(ascii_letters + digits, k=6))
    return random_url