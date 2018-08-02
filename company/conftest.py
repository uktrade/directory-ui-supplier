from copy import deepcopy
import http
from unittest.mock import patch

from directory_api_client.client import api_client
import requests
import pytest


@pytest.fixture
def list_public_profiles_data(retrieve_profile_data):
    return {
        'results': [
            retrieve_profile_data,
        ],
        'count': 20
    }


@pytest.fixture
def supplier_case_study_data(retrieve_profile_data):
    return {
        'description': 'Damn great',
        'sector': 'SOFTWARE_AND_COMPUTER_SERVICES',
        'image_three': 'https://image_three.jpg',
        'website': 'http://www.google.com',
        'video_one': 'https://video_one.wav',
        'title': 'Two',
        'slug': 'two',
        'company': retrieve_profile_data,
        'image_one': 'https://image_one.jpg',
        'testimonial': 'I found it most pleasing.',
        'keywords': 'great',
        'pk': 2,
        'year': '2000',
        'image_two': 'https://image_two.jpg'
    }


@pytest.fixture
def api_response_company_profile_200(retrieve_profile_data):
    response = requests.Response()
    response.status_code = http.client.OK
    response.json = lambda: deepcopy(retrieve_profile_data)
    return response


@pytest.fixture
def api_response_list_public_profile_200(
    api_response_200, list_public_profiles_data
):
    response = api_response_200
    response.json = lambda: deepcopy(list_public_profiles_data)
    return response


@pytest.fixture
def api_response_retrieve_public_case_study_200(
    supplier_case_study_data, api_response_200
):
    response = api_response_200
    response.json = lambda: deepcopy(supplier_case_study_data)
    return response


@pytest.fixture(autouse=True)
def list_public_profiles(api_response_list_public_profile_200):
    stub = patch.object(
        api_client.company, 'list_public_profiles',
        return_value=api_response_list_public_profile_200,
    )
    stub.start()
    yield
    stub.stop()


@pytest.fixture(autouse=True)
def retrieve_supplier_case_study(
    api_response_retrieve_public_case_study_200
):
    stub = patch.object(
        api_client.company, 'retrieve_public_case_study',
        return_value=api_response_retrieve_public_case_study_200,
    )
    stub.start()
    yield
    stub.stop()


@pytest.fixture(autouse=True)
def retrieve_profile(api_response_company_profile_200):
    stub = patch.object(
        api_client.company, 'retrieve_private_profile',
        return_value=api_response_company_profile_200,
    )
    stub.start()
    yield
    stub.stop()


@pytest.fixture(autouse=True)
def retrieve_public_profile(api_response_company_profile_200):
    stub = patch.object(
        api_client.company, 'retrieve_public_profile',
        return_value=api_response_company_profile_200,
    )
    stub.start()
    yield
    stub.stop()
