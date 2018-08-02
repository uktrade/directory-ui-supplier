from company import constants
from company.templatetags import email_tags


def test_email_image_returns_constant_image():
    expected = constants.EMAIL_STATIC_FILE_BUCKET + 'a'
    assert email_tags.email_image('a') == expected
