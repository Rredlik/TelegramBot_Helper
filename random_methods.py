import random


def random_number(a, b):
    ph_number = str(random.randint(a,b))
    return ph_number


def cats_photo_name(a, b):
    ph_name = 'static/cat_' + random_number(a, b) + '.jpg'
    return ph_name
