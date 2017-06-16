from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


links = settings.SECTOR_LINKS

COMPANIES_HOUSE_SEARCH_URL = 'https://beta.companieshouse.gov.uk'

HEALTH_SECTOR_CONTEXT = {
    'sector_value': 'HEALTHCARE_AND_MEDICAL',
    'case_study': {
        'image_url': '/static/images/touch-bionics-right-hand.png',
        'image_caption': mark_safe(_('Rebekah Marine: i-limb&trade; user')),
        'title': 'Touch Bionics',
        'synopsis': _(
            'Touch Bionics has transformed thousands of lives in '
            'dozens of countries through world-leading prosthetic '
            'technologies. We have a range of myoelectric prosthetic '
            'hands and prosthetic fingers that help people increase '
            'their independence and confidence.'
        ),
        'url': links['HEALTHCARE_AND_MEDICAL']['case_study'],
        'testimonial': mark_safe(_(
            'The i-limb&trade; quantum is the next best thing to real hands '
            'and as a bilateral amputee having the ability to do what I want '
            'to do independently is truly remarkable.'
        )),
        'testimonial_name': _('Jason'),
        'testimonial_company': mark_safe(_('i-limb quantum&trade; user')),
        'company_name': 'Touch Bionics',
        'sectors': [
            {
                'label': _('Healthcare and life sciences'),
                'value': 'HEALTHCARE_AND_MEDICAL'
            },
            {
                'label': _('Technology'),
                'value': 'SOFTWARE_AND_COMPUTER_SERVICES'
            }
        ],
        'keywords': _(
            'prosthetics, bionics, robotics, healthcare, technology, limb loss'
        ),
    },
    'companies': [
        {
            'image_url': '/static/images/r-d-biomed.png',
            'name': 'RD Biomed',
            'description': mark_safe(_(
                'RD Biomed designs and makes Peptest&trade;- the world’s '
                'first non-invasive reflux diagnostic test. RD Biomed '
                'specialises in diagnostics for gastroenterology and '
                'respiratory conditions.'
            )),
            'url': links['HEALTHCARE_AND_MEDICAL']['company_one'],
        },
        {
            'image_url': '/static/images/touch-bionics-left-hand.png',
            'name': 'Touch Bionics',
            'description': _(
                'Touch Bionics is responsible for developing and improving '
                'the world’s first bionic hand with 5 independently '
                'moving fingers, transforming lives across the globe.'
            ),
            'url': links['HEALTHCARE_AND_MEDICAL']['company_two'],
        },
    ]
}

TECH_SECTOR_CONTEXT = {
    'sector_value': 'SOFTWARE_AND_COMPUTER_SERVICES',
    'case_study': {
        'image_url': '/static/images/evrythng.jpg',
        'image_caption': 'EVRYTHNG',
        'title': 'EVRYTHNG',
        'synopsis': _(
            'EVRYTHNG’s commercial Internet of Things traceability '
            'solution allows brands to track and report the status, '
            'location and history of everything they produce from '
            'manufacture through to the home. EVRYTHNG’s flexible data '
            'model enables the complex, interlinked hierarchy of '
            'component parts, finished product, batches, cases and '
            'pallets can be identified and mapped.'
        ),
        'url': links['SOFTWARE_AND_COMPUTER_SERVICES']['case_study'],
        'testimonial': _(
            'Companies can transform the value of their physical assets '
            'in the EVRYTHNG cloud by adding an intelligent, personalised '
            'layer of digital content, services and data analytics.'
        ),
        'testimonial_name': '',
        'testimonial_company': '',
        'company_name': 'EVRYTHNG',
        'sectors': [
            {
                'label': _('Technology'),
                'value': 'SOFTWARE_AND_COMPUTER_SERVICES',
            },
        ],
        'keywords': _(
            'Internet of Things, data analytics, traceability, connectivity'
        ),
    },
    'companies': [
        {
            'image_url': '/static/images/evrything.png',
            'name': 'EVRYTHNG',
            'description': mark_safe(_(
                'EVRYTHNG is an Internet of Things software company that '
                'helps manufacturers <i>digitalise</i> their physical '
                'products by connecting them to the web. From everyday '
                'consumer packaged products connected via smart packaging '
                'and smartphones, to fully-connected smart home '
                'appliances, each individual item managed in the EVRYTHNG '
                'cloud has a unique Active Digital Identity'
            )),
            'url': links['SOFTWARE_AND_COMPUTER_SERVICES']['company_one'],
        },
        {
            'image_url': '/static/images/arkessa.png',
            'name': 'Arkessa',
            'description': _(
                'Arkessa enables devices and applications developers to '
                'connect to the Internet of Things (IoT), regardless of '
                'location, network operator or wireless technology. It '
                'provides enterprises with a secure and future-proof '
                'mobility platform that is easy to adopt, integrate and '
                'scale.'
            ),
            'url': links['SOFTWARE_AND_COMPUTER_SERVICES']['company_two'],
        },
    ]
}

CREATIVE_SECTOR_CONTEXT = {
    'sector_value': 'CREATIVE_AND_MEDIA',
    'case_study': {
        'image_url': '/static/images/immersive-hero.jpg',
        'image_caption': '',
        'title': 'Immersive',
        'synopsis': _(
            'For Adidas’ 2014 World Cup campaign, Immersive developed '
            'concepts, storyboards and produced final audio and video '
            'designs. It also produced the entire technical event, which '
            'included projection mapping on the mansion and a 2m ball and '
            'consulting on live-camera press shot positions'
        ),
        'url': links['CREATIVE_AND_MEDIA']['case_study'],
        'testimonial': _(
            'Creating the grandest projection mapping the world has ever seen.'
        ),
        'testimonial_name': '',
        'testimonial_company': _('Fast Company magazine'),
        'company_name': 'Immersive',
        'sectors': [
            {
                'label': _('Creative'),
                'value': 'CREATIVE_AND_MEDIA',
            },
        ],
        'keywords': _(
            'Interactive installations, video content, projection mapping'
        ),
    },
    'companies': [
        {
            'image_url': '/static/images/immersive.png',
            'name': 'Immersive',
            'description': _(
                'Immersive is a complete solution provider for audio-visual '
                'projects of any scale. Immersive uses new media technology '
                '(such as LED, holograms, projection, virtual reality and '
                'augmented reality) to design and create cutting-edge '
                'lighting, video and interactive installations.'
            ),
            'url': links['CREATIVE_AND_MEDIA']['company_one'],
        },
        {
            'image_url': '/static/images/blippar.png',
            'name': 'Blippar',
            'description': _(
                'Blippar is the leading visual discovery app, harnessing '
                'augmented reality, image-recognition technology and '
                'artificial intelligence to bring the physical world to '
                'life through smartphones.'
            ),
            'url': links['CREATIVE_AND_MEDIA']['company_two'],
        },
    ]
}

FOOD_SECTOR_CONTEXT = {
    'sector_value': 'FOOD_AND_DRINK',
    'case_study': {
        'image_url': '/static/images/fever-tree-pour.png',
        'image_caption': _('Clementine and cinnamon tonic water'),
        'title': _('Clementine and cinnamon tonic water'),
        'synopsis': _(
            'Fever-Tree has established itself as the mixer drink '
            'specialist, crafting a range of fourteen products sourced '
            'from the highest quality natural ingredients for the best '
            'tasting mixers.'
        ),
        'url': links['FOOD_AND_DRINK']['case_study'],
        'testimonial': _(
            'If three-quarters of your gin and tonic is the tonic, make sure '
            'you use the best.'
        ),
        'testimonial_name': _('Tim Warrillow'),
        'testimonial_company': 'Fever-Tree',
        'company_name': 'Fever-Tree',
        'sectors': [
            {
                'label': _('Food and drink'),
                'value': 'FOOD_AND_DRINK',
            },
        ],
        'keywords': _('Mixers, Quality, Taste'),
    },
    'companies': [
        {
            'image_url': '/static/images/joe-and-steph.png',
            'name': "Joe & Seph's",
            'description': mark_safe(_(
                'All Joe & Seph’s popcorn is handmade in small batches to '
                'ensure superior texture and an intense flavour. The '
                'ingredients used are 100&#37; natural and the kernels are '
                'all air-popped – a healthier cooking method compared to '
                'frying.'
            )),
            'url': links['FOOD_AND_DRINK']['company_one'],
        },
        {
            'image_url': '/static/images/fever-tree.png',
            'name': 'Fever-Tree',
            'description': _(
                'Fever-Tree has pioneered premium mixers and is now the '
                'world’s leading premium mixer company.'
            ),
            'url': links['FOOD_AND_DRINK']['company_two'],
        },
    ]
}


ADVANCED_MANUFACTURING_CONTEXT = {
    'sector_value': 'MECHANICAL_ELECTRICAL_AND_PROCESS_ENGINEERING',
    'case_study': {
        'image_url': '',
        'image_caption': '',
        'title': '',
        'synopsis': '',
        'url': '',
        'testimonial': '',
        'testimonial_name': '',
        'testimonial_company': '',
        'company_name': '',
        'sectors': [],
        'keywords': '',
    },
    'companies': [
        {
            'image_url': '',
            'name': '',
            'description': '',
            'url': '',
        },
        {
            'image_url': '',
            'name': '',
            'description': '',
            'url': '',
        },
    ]
}


GLOBAL_SPORTS_INFRASTRUCTURE_CONTEXT = {
    'sector_value': 'GLOBAL_SPORTS_INFRASTRUCTURE',
    'case_study': {
        'image_url': (
            '/static/images/'
            'Queen-Elizabeth-Olympic-Park---Movement-Strategies.jpg'
        ),
        'image_caption': _('Queen Elizabeth Olympic Park, London'),
        'title': _('London 2012 Olympic and Paralympic Games'),
        'synopsis': _(
            'Movement Strategies leads design standards for '
            'major events such as the Olympic Games, helping plan '
            'crowd movement and safety, and driving increased '
            'ticket sales.'
        ),
        'url': links['GLOBAL_SPORTS_INFRASTRUCTURE']['case_study'],
        'testimonial': '',
        'testimonial_name': '',
        'testimonial_company': '',
        'company_name': 'Movement Strategies',
        'sectors': [
            {
                'label': _('Global sports infrastructure'),
                'value': 'Global_sports_infrastructure',
            },
        ],
        'keywords': _('Crowd safety, Pedestrian flow, Movement analytics'),
    },
    'companies': [
        {
            'image_url': '/static/images/Movement-Strategies---Baku.jpg',
            'name': 'Movement Strategies',
            'description': _(
                'Movement Strategies is the largest and most '
                'experienced independent, specialist people movement '
                'consultancy in the world.'
            ),
            'url': links['GLOBAL_SPORTS_INFRASTRUCTURE']['company_one'],
        },
        {
            'image_url': '/static/images/Fortress---The-London-Stadium.jpg',
            'name': 'Fortress GB',
            'description': _(
                'Fortress GB proved its reputation as the market-leading '
                'e-ticketing provider by being selected to '
                'install and manage the very latest in turnstile '
                'technology at West Ham’s new home at the London Stadium.'
            ),
            'url': links['GLOBAL_SPORTS_INFRASTRUCTURE']['company_two'],
        },
    ]
}
