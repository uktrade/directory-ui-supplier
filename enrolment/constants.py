from django.conf import settings


links = settings.SECTOR_LINKS

COMPANIES_HOUSE_SEARCH_URL = 'https://beta.companieshouse.gov.uk'

HEALTH_SECTOR_CONTEXT = {
    'sector_value': 'HEALTHCARE_AND_MEDICAL',
    'case_study': {
        'image_url': '/static/images/touch-bionics-right-hand.png',
        'image_caption': 'Rebekah Marine: i-limbTM user',
        'title': 'Touch Bionics',
        'synopsis': (
            'Touch Bionics has transformed thousands of lives in '
            'dozens of countries through world-leading prosthetic '
            'technologies. We have a range of myoelectric prosthetic '
            'hands and prosthetic fingers that help people increase '
            'their independence and confidence.'
        ),
        'url': links['HEALTHCARE_AND_MEDICAL']['case_study'],
        'testimonial': (
            'The i-limb™ quantum is the next best thing to real hands and as '
            'a bilateral amputee having the ability to do what I want to do '
            'independently is truly remarkable.'
        ),
        'testimonial_name': 'Jason',
        'testimonial_company': 'i-limb quantum™ user',
        'company_name': 'Touch Bionics',
        'sectors': [
            {
                'label': 'Healthcare and life sciences',
                'value': 'HEALTHCARE_AND_MEDICAL'
            },
            {
                'label': 'Technology',
                'value': 'SOFTWARE_AND_COMPUTER_SERVICES'
            }
        ],
        'keywords': (
            'prosthetics, bionics, robotics, healthcare, technology, limb loss'
        ),
    },
    'companies': [
        {
            'image_url': '/static/images/r-d-biomed.png',
            'name': 'RD Biomed',
            'description': (
                'RD Biomed designs and makes Peptest[TM] - the world’s '
                'first non-invasive reflux diagnostic test. RD Biomed '
                'specialises in diagnostics for gastroenterology and '
                'respiratory conditions.'
            ),
            'url': links['HEALTHCARE_AND_MEDICAL']['company_one'],
        },
        {
            'image_url': '/static/images/touch-bionics-left-hand.png',
            'name': 'Touch Bionics',
            'description': (
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
        'image_url': '/static/images/hawk-eye.png',
        'image_caption': 'Electronic line-calling service',
        'title': 'Electronic line-calling service',
        'synopsis': (
            'Hawk-Eye has developed the most sophisticated vision processing '
            'technology in sport which enables us to not only track balls to '
            'millimetre-accuracy but also players and cars. This vision '
            'processing technology combined with an intelligent IT based '
            'video replay and distribution software and creative graphics '
            'platform powers a revolution for sport.'
        ),
        'url': links['SOFTWARE_AND_COMPUTER_SERVICES']['case_study'],
        'testimonial': (
            'Hawk-Eye has now become an integral part of over 20 sports and '
            'every year covers 7,200 games or events across 450 stadiums in '
            'over 60 countries.'
        ),
        'testimonial_name': None,
        'testimonial_company': None,
        'company_name': 'Hawk-Eye Innovations',
        'sectors': [
            {
                'label': 'Technology',
                'value': 'SOFTWARE_AND_COMPUTER_SERVICES',
            },
        ],
        'keywords': (
            'Sports, officiation, digital, data, broadcast media, '
            'ball-tracking, player-tracking'
        ),
    },
    'companies': [
        {
            'image_url': '/static/images/evrything.png',
            'name': 'EVRYTHING',
            'description': (
                'EVRYTHING is an Internet of Things software company that '
                'helps manufacturers digitize their physical products by '
                'connecting them to the web. From everyday consumer packaged '
                'products connected via smart packaging and smartphones, to '
                'fully-connected smart home appliances, each individual item '
                'managed in the EVRYTHNG cloud has a unique Active Digital '
                'Identity'
            ),
            'url': links['SOFTWARE_AND_COMPUTER_SERVICES']['company_one'],
        },
        {
            'image_url': '/static/images/arkessa.png',
            'name': 'Arkessa',
            'description': (
                'Arkessa enables Internet of Things devices and applications '
                'developers to connect to the IoT, regardless of location, '
                'network operator or wireless technology. It provides '
                'enterprises with a secure and future-proof mobility '
                'platform that is easy to adopt, integrate and scale.'
            ),
            'url': links['SOFTWARE_AND_COMPUTER_SERVICES']['company_two'],
        },
    ]
}

CREATIVE_SECTOR_CONTEXT = {
    'sector_value': 'CREATIVE_AND_MEDIA',
    'case_study': {
        'image_url': '',
        'image_caption': '',
        'title': 'Immersive',
        'synopsis': (
            'For Adidas’ 2014 World Cup campaign, Immersive developed '
            'concepts, storyboards and produced final audio and video '
            'designs. It also produced the entire technical event, which '
            'included projection mapping on the mansion and a 2m ball and '
            'consulting on live-camera press shot positions'
        ),
        'url': links['CREATIVE_AND_MEDIA']['case_study'],
        'testimonial': (
            'Creating the grandest projection mapping the world has ever seen.'
        ),
        'testimonial_name': '',
        'testimonial_company': 'Fast Company magazine',
        'company_name': 'Immersive',
        'sectors': [
            {
                'label': 'Creative',
                'value': 'CREATIVE_AND_MEDIA',
            },
        ],
        'keywords': (
            'Interactive installations, video content, projection mapping'
        ),
    },
    'companies': [
        {
            'image_url': '/static/images/immersive.png',
            'name': 'Immersive',
            'description': (
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
            'description': (
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
        'image_caption': 'Clementine and cinnamon tonic water',
        'title': 'Clementine and cinnamon tonic water',
        'synopsis': (

        ),
        'url': links['FOOD_AND_DRINK']['case_study'],
        'testimonial': (
            'If three-quarters of your gin and tonic is the tonic, make sure '
            'you use the best.'
        ),
        'testimonial_name': 'Tim Warrillow',
        'testimonial_company': 'Fever-Tree',
        'company_name': 'Fever-Tree',
        'sectors': [
            {
                'label': 'Food and Drink',
                'value': 'FOOD_AND_DRINK',
            },
        ],
        'keywords': 'Premium, Natural, Mixers, Drinks, Taste, Quality',
    },
    'companies': [
        {
            'image_url': '/static/images/joe-and-steph.png',
            'name': "Joe & Seph's",
            'description': (
                'All Joe & Seph’s popcorn is handmade in small batches to '
                'ensure superior texture and an intense flavour on each and '
                'every kernel. The ingredients used are 100% natural and the '
                'kernels are all air-popped – a healthier cooking method '
                'compared to frying.'
            ),
            'url': links['FOOD_AND_DRINK']['company_one'],
        },
        {
            'image_url': '/static/images/fever-tree.png',
            'name': 'Fever-Tree',
            'description': (
                "Fever-Tree has pioneered premium mixers and is now the "
                "world's leading premium mixer company."
            ),
            'url': links['FOOD_AND_DRINK']['company_two'],
        },
    ]
}
