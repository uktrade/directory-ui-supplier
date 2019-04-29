from directory_constants import choices
from directory_components import forms, fields, widgets

from django.forms import ValidationError
from django.forms.widgets import HiddenInput, TextInput

from investment_support_directory.fields import IntegerField


CHOICES_FINANCIAL = (
    'Opening bank accounts',
    'Accounting and Tax (including registration for VAT and PAYE)',
    'Insurance',
    'Raising Capital',
    'Regulatory support',
    'Mergers and Acquisitions',
)

CHOICES_MANAGEMENT_CONSULTING = (
    'Business development',
    'Product safety regulation and compliance',
    'Commercial/pricing strategy',
    'Workforce development',
    'Strategy & long-term planning',
    'Risk consultation',
)

CHOICES_HUMAN_RESOURCES = (
    'Staff management & progression',
    (
        'Onboarding, including new starter support and contracts '
        'of employment'
    ),
    'Payroll',
    'Salary benchmarking and employee benefits ',
    'Succession planning',
    'Employment & talent research',
    'Sourcing and Hiring',
)

CHOICES_LEGAL = (
    'Company incorporation',
    'Employment',
    'Immigration',
    'Land use planning',
    'Intellectual property',
    'Data Protection and Information Assurance',
)

CHOICES_PUBLICITY = (
    'Public Relations',
    'Branding',
    'Social Media',
    'Public Affairs',
    'Advertising',
    'Marketing',
)

CHOICES_FURTHER_SERVICES = (
    'Business relocation',
    'Planning consultants',
    'Facilities (water, wifi, electricity)',
    'Translation services',
    'Staff and family relocation including schooling for children',
)


class CompanyHomeSearchForm(forms.Form):

    q = fields.CharField(
        label='',
        max_length=255,
        widget=TextInput(
            attrs={
                'autofocus': 'autofocus',
                'dir': 'auto',
                'placeholder': 'Type the product,service,expertises or keyword'
            }
        ),
    )


class CompanySearchForm(forms.Form):

    MESSAGE_MINIMUM_VIABLE_SEARCH = (
        'Please specify a search term or expertise.'
    )

    q = fields.CharField(
        label='Search by product, service or company keyword',
        max_length=255,
        required=False,
        widget=TextInput(
            attrs={
                'placeholder': 'Search for UK suppliers',
                'autofocus': 'autofocus',
                'dir': 'auto'
            }
        ),
    )
    page = IntegerField(
        required=False,
        widget=HiddenInput,
        initial=1,
    )
    expertise_industries = fields.MultipleChoiceField(
        label='Industry expertise',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-industry-expertise'},
            use_nice_ids=True,
        ),
        choices=choices.INDUSTRIES,
        required=False,
    )
    expertise_regions = fields.MultipleChoiceField(
        label='Regional expertise',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-regional-expertise'},
            use_nice_ids=True,
        ),
        choices=choices.EXPERTISE_REGION_CHOICES,
        required=False,
    )
    expertise_countries = fields.MultipleChoiceField(
        label='International expertise',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-international-expertise'},
            use_nice_ids=True,
        ),
        choices=choices.COUNTRY_CHOICES,
        required=False,
    )
    expertise_languages = fields.MultipleChoiceField(
        label='Language expertise',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-language-expertise'},
            use_nice_ids=True,
        ),
        choices=choices.EXPERTISE_LANGUAGES,
        required=False,
    )
    expertise_products_services_financial = fields.MultipleChoiceField(
        label='',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-expertise-products-services-financial'},
            use_nice_ids=True,
        ),
        choices=[(item, item) for item in CHOICES_FINANCIAL],
        required=False,
    )
    expertise_products_services_management = fields.MultipleChoiceField(
        label='',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-products-services-management-expertise'},
            use_nice_ids=True,
        ),
        choices=[(item, item) for item in CHOICES_MANAGEMENT_CONSULTING],
        required=False,
    )
    expertise_products_services_human_resources = fields.MultipleChoiceField(
        label='',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-products-services-human-expertise'},
            use_nice_ids=True,
        ),
        choices=[(item, item) for item in CHOICES_HUMAN_RESOURCES],
        required=False,
    )
    expertise_products_services_legal = fields.MultipleChoiceField(
        label='',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-products-services-legal-expertise'},
            use_nice_ids=True,
        ),
        choices=[(item, item) for item in CHOICES_LEGAL],
        required=False,
    )
    expertise_products_services_publicity = fields.MultipleChoiceField(
        label='',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-products-services-publicity-expertise'},
            use_nice_ids=True,
        ),
        choices=[(item, item) for item in CHOICES_PUBLICITY],
        required=False,
    )
    expertise_products_services_further_services = fields.MultipleChoiceField(
        label='',
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-products-services-further-expertise'},
            use_nice_ids=True,
        ),
        choices=[(item, item) for item in CHOICES_FURTHER_SERVICES],
        required=False,
    )

    def clean_page(self):
        return self.cleaned_data['page'] or self.fields['page'].initial

    def clean(self):
        super().clean()
        # these field values are all stored in expertise_products_services, but
        # the form expresses them as separate fields for better user experience
        product_services_fields = [
            'expertise_products_services_management',
            'expertise_products_services_human_resources',
            'expertise_products_services_legal',
            'expertise_products_services_publicity',
            'expertise_products_services_further_services',
        ]

        products_services = []
        for field_name in product_services_fields:
            if field_name in self.cleaned_data:
                products_services += self.cleaned_data[field_name]
        self.cleaned_data['expertise_products_services'] = products_services

        minimum_vialble_search_fields = {
            'expertise_industries',
            'expertise_regions',
            'expertise_countries',
            'expertise_languages',
            'expertise_products_services',
            'q',
        }
        searched_fields = set(
            key for key, value in self.cleaned_data.items() if value
        )
        if not searched_fields.intersection(minimum_vialble_search_fields):
            raise ValidationError({'q': self.MESSAGE_MINIMUM_VIABLE_SEARCH})
