from investment_support_directory import helpers


def test_company_parser_serialize_for_template(retrieve_profile_data):
    company = helpers.CompanyParser(retrieve_profile_data)

    assert company.serialize_for_template() == {
        'address': '123 Fake Street, Fakeville, London, E14 6XK',
        'address_line_1': '123 Fake Street',
        'address_line_2': 'Fakeville',
        'country': 'GB',
        'date_of_creation': '02 March 2015',
        'description': 'Ecommerce website',
        'email_address': 'test@example.com',
        'email_full_name': 'Jeremy',
        'employees': '501-1,000',
        'expertise_countries': '',
        'expertise_industries': '',
        'expertise_languages': '',
        'expertise_products_services': {},
        'expertise_regions': '',
        'facebook_url': 'http://www.facebook.com',
        'has_expertise': False,
        'keywords': 'word1, word2',
        'linkedin_url': 'http://www.linkedin.com',
        'locality': 'London',
        'logo': 'nice.jpg',
        'mobile_number': '07506043448',
        'modified': '2016-11-23T11:21:10.977518Z',
        'name': 'Great company',
        'number': '01234567',
        'po_box': 'abc',
        'postal_code': 'E14 6XK',
        'postal_full_name': 'Jeremy',
        'sectors': 'Security',
        'slug': 'great-company',
        'summary': 'this is a short summary',
        'supplier_case_studies': [],
        'twitter_url': 'http://www.twitter.com',
        'verified_with_code': True,
        'website': 'http://example.com',
    }


def test_company_parser_serialize_for_template_empty():
    company = helpers.CompanyParser({})

    assert company.serialize_for_template() == {}