from raven.processors import SanitizePasswordsProcessor


class SanitizeEmailMessagesProcessor(SanitizePasswordsProcessor):
    FIELDS = frozenset([
        'body',
    ])
