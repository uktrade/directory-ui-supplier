from django.conf import settings

from directory_cms_client import DirectoryCMSClient

cms_client = DirectoryCMSClient(
    base_url=settings.CMS_URL,
    api_key=settings.CMS_SIGNATURE_SECRET,
)
