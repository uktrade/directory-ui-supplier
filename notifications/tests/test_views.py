import http
from unittest.mock import patch

import pytest
import requests

from django.core.urlresolvers import reverse

from notifications import views


@pytest.fixture
def api_response_200():
    response = requests.Response()
    response.status_code = http.client.OK
    return response


@pytest.fixture
def api_response_400():
    response = requests.Response()
    response.status_code = http.client.BAD_REQUEST
    return response


def test_unsubscribe_feature_flag_off(settings, client):
    settings.FEATURE_UNSUBSCRIBE_VIEW_ENABLED = False

    response = client.get(reverse('anonymous-unsubscribe'))

    assert response.status_code == http.client.NOT_FOUND


def test_unsubscribe_reuqired_params(client):
    response = client.get(reverse('anonymous-unsubscribe'), {'email': '123'})

    view = views.AnonymousUnsubscribeView
    assert response.status_code == http.client.OK
    assert response.template_name == [view.template_name]


def test_unsubscribe_missing_reuqired_params(client):
    response = client.get(reverse('anonymous-unsubscribe'))

    view = views.AnonymousUnsubscribeView
    assert response.status_code == http.client.OK
    assert response.template_name == view.failure_template_name


@patch.object(views.api_client.notifications, 'anonymous_unsubscribe')
def test_unsubscribe_api_failure(mock_unsubscribe, api_response_400, client):
    mock_unsubscribe.return_value = api_response_400

    response = client.post(reverse('anonymous-unsubscribe'), {'email': '123'})

    view = views.AnonymousUnsubscribeView
    assert response.status_code == http.client.OK
    assert response.template_name == view.failure_template_name


@patch.object(views.api_client.notifications, 'anonymous_unsubscribe')
def test_unsubscribe_api_success(mock_unsubscribe, api_response_200, client):
    mock_unsubscribe.return_value = api_response_200

    response = client.post(reverse('anonymous-unsubscribe'), {'email': '123'})

    view = views.AnonymousUnsubscribeView
    assert response.status_code == http.client.OK
    assert response.template_name == view.success_template_name
