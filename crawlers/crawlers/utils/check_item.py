import scrapy

def is_valid(item):
    if not item or type(item) == scrapy.Request:
        raise ValueError('Wrong type')
    for key in item.keys():
        value = item[key]
        if not value:
            raise ValueError('Value is None')
        if type(value) == str and len(value) <= 0:
            raise ValueError('Value is empty')
        if type(value) == int or type(float) and value == -1:
            raise ValueError('Value is negative')
    return True
