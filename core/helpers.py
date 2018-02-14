from urllib.parse import urljoin

import requests

from django.conf import settings

from sigauth.utils import RequestSigner


class CmsClient:

    page_url = '/api/pages/{page_id}/'

    def __init__(self, base_url, api_key):
        assert base_url, "Missing base url"
        assert api_key, "Missing API key"
        self.base_url = base_url
        self.request_signer = RequestSigner(secret=api_key)

    def sign_request(self, request):
        prepared_request = request.prepare()
        headers = self.request_signer.get_signature_headers(
            url=prepared_request.path_url,
            body=prepared_request.body,
            method=prepared_request.method,
            content_type=prepared_request.headers.get('Content-Type'),
        )
        prepared_request.headers.update(headers)
        return prepared_request

    def get(self, path, *args, **kwargs):
        url = urljoin(self.base_url, path)
        request = requests.Request('GET', url, *args, **kwargs)
        signed_request = self.sign_request(request)
        return requests.Session().send(signed_request)

    def get_page(self, page_id, draft_token=None):
        if draft_token:
            params = {'draft_token': draft_token}
        else:
            params = {}
        url = self.page_url.format(page_id=page_id)
        return self.get(url, params=params)


cms_client = CmsClient(
    base_url=settings.CMS_URL,
    api_key=settings.CMS_SIGNATURE_SECRET,
)
