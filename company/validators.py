import re

from django.core.validators import URLValidator, RegexValidator

MESSAGE_REMOVE_URL = 'Please remove the web address.'


class ContainsUrlValidator(RegexValidator):
    # remove the `^` from the start of Django's url validator, and the \Z
    # from the end for substring matching, rather than entire string matching.
    regex = re.compile(
        URLValidator.regex.pattern[1:-2],
        re.IGNORECASE
    )


def not_contains_url(value):
    if not value:
        return None
    ContainsUrlValidator(inverse_match=True, message=MESSAGE_REMOVE_URL)(value)
