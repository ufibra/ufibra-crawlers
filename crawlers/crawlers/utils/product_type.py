import re

COMBO = 'combo'
WHEY_PROTEIN = 'wheyprotein'

def is_combo(text):
    if not text:
        return False
    return 'combo' in text.lower()

def is_wheyprotein(text):
    if not text:
        return False
    return not is_combo(text) and re.search('whey (protein)?', text, re.I)
