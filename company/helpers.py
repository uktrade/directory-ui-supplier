import datetime

from directory_validators.constants import choices


EMPLOYEE_CHOICES = {key: value for key, value in choices.EMPLOYEES}
SECTOR_CHOICES = {key: value for key, value in choices.COMPANY_CLASSIFICATIONS}


def format_date_of_creation(raw_date_of_creation):
    if not raw_date_of_creation:
        return raw_date_of_creation
    return datetime.datetime.strptime(raw_date_of_creation, '%Y-%m-%d')


def get_employees_label(employees_value):
    if not employees_value:
        return employees_value
    return EMPLOYEE_CHOICES.get(employees_value)


def pair_sector_values_with_label(sectors_values):
    if not sectors_values:
        return []
    return [pair_sector_value_with_label(value) for value in sectors_values]


def pair_sector_value_with_label(sectors_value):
    return {'value': sectors_value, 'label': get_sectors_label(sectors_value)}


def get_sectors_label(sectors_value):
    if not sectors_value:
        return sectors_value
    return SECTOR_CHOICES.get(sectors_value)


def get_case_study_details_from_response(response):
    parsed = response.json()
    # `format_company_details` expects `supplier_case_studies` key.
    parsed['company']['supplier_case_studies'] = []
    parsed['sector'] = pair_sector_value_with_label(parsed['sector'])
    parsed['company'] = format_company_details(parsed['company'])
    return parsed


def get_public_company_profile_from_response(response):
    return format_company_details(response.json())


def get_company_profile_from_response(response):
    return format_company_details(response.json())


def get_company_list_from_response(response):
    parsed = response.json()
    if parsed['results']:
        results = map(format_company_details, parsed['results'])
        parsed['results'] = list(results)
    return parsed


def format_company_details(details):
    date_of_creation = format_date_of_creation(details.get('date_of_creation'))
    case_studies = map(format_case_study, details['supplier_case_studies'])
    return {
        'website': details['website'],
        'description': details['description'],
        'summary': details['summary'],
        'number': details['number'],
        'date_of_creation': date_of_creation,
        'sectors': pair_sector_values_with_label(details['sectors']),
        'logo': details['logo'],
        'name': details['name'],
        'keywords': details['keywords'],
        'employees': get_employees_label(details['employees']),
        'supplier_case_studies': list(case_studies),
        'modified': datetime.datetime.strptime(
            details['modified'], '%Y-%m-%dT%H:%M:%S.%fZ'),
        'verified_with_code': details['verified_with_code'],
        'postal_full_name': details['postal_full_name'],
        'address_line_1': details['address_line_1'],
        'address_line_2': details['address_line_2'],
        'locality': details['locality'],
        'country': details['country'],
        'postal_code': details['postal_code'],
        'po_box': details['po_box'],
        'mobile_number': details['mobile_number'],
        'twitter_url': details['twitter_url'],
        'facebook_url': details['facebook_url'],
        'linkedin_url': details['linkedin_url'],
        'email_address': details['email_address'],
        'email_full_name': details['email_full_name'],
        'has_social_links': bool(
            details['twitter_url'] or
            details['facebook_url'] or
            details['linkedin_url']
        )
    }


def format_case_study(case_study):
    case_study['sector'] = pair_sector_value_with_label(case_study['sector'])
    return case_study
