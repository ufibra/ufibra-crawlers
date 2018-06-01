import scrapy

def is_valid(item):
    if not item or type(item) == scrapy.Request:
        return True
    for key in item.keys():
        value = item[key]
        if not value:
            raise ValueError(f'{key.capitalize()} is None')
        if type(value) == str and len(value) <= 0:
            raise ValueError(f'{key.capitalize()} is empty')
        if type(value) == int or type(float) and value == -1:
            raise ValueError(f'{key.capitalize()} is negative')
    return True
