import re

def parse_gram(value, unit):
    if unit in ['kg', 'k']:
        return value * 1000
    elif unit == 'g':
        return value
    elif unit == 'mg':
        return value / 1000.0
    else:
        return -1

def parse_unit(text):
    text = text.strip()
    unit_group = re.search('(k|kg|mg|g)', text, re.I)
    unit = unit_group.group(0)
    return unit.lower()

def parse_weight(text):
    if not text:
        return -1
    text = text.strip()
    weight_group = re.search('\d+.?\d*(g|k|kg|mg)', text, re.I)
    if weight_group:
        weight = weight_group.group(0)
        weight_value = parse_price(weight)
        unit = parse_unit(weight)
        return parse_gram(weight_value, unit)
    return -1

def parse_number(text):
    if not text:
        return -1
    text = text.strip()
    price = re.search('\d+,?\d*', text)
    if price:
        value = price.group(0).replace(',', '.')
        if value.count('.') > 1:
            return float(value.replace('.', '', 1))
        else:
            return float(value)
    return -1

def parse_price(text):
    return parse_number(text)
