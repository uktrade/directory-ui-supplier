import re

from django.core.validators import RegexValidator

MESSAGE_REMOVE_URL = 'Please remove the web address.'


class ContainsUrlValidator(RegexValidator):
    # Modified django.core.validators.URLValidator.regex.pattern, without the
    # '://'' in the pattern and start/end of the string
    link_pattern = (
        '(?:[a-z0-9\\.\\-]*)(?:\\S+(?::\\S*)?@)?(?:(?:25[0-5]|2[0-4]\\d|[0-1]'
        '?\\d?\\d)(?:\\.(?:25[0-5]|2[0-4]\\d|[0-1]?\\d?\\d)){3}|\\[[0-9a-f:\\'
        '.]+\\]|([a-z¡-\uffff0-9](?:[a-z¡-\uffff0-9-]*[a-z¡-\uffff0-9])?(?:\\'
        '.(?!-)[a-z¡-\uffff0-9-]+(?<!-))*\\.(?!-)(?:[a-z¡-\uffff-]{2,}|xn--[a'
        '-z0-9]+)(?<!-)\\.?|localhost))(?::\\d{2,5})?(?:[/?#][^\\s]*)?'
    )
    regex = re.compile(link_pattern, re.IGNORECASE)


def not_contains_url(value):
    if not value:
        return
    ContainsUrlValidator(inverse_match=True, message=MESSAGE_REMOVE_URL)(value)
