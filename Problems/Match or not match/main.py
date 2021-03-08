import re


def matched(template, string):
    r = re.match(template, string)
    if not r:
        return False
    return True
