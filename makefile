clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

test_requirements:
	pip install -r requirements_test.txt

FLAKE8 := flake8 . --exclude=migrations,.venv,node_modules
PYTEST := pytest . --ignore=node_modules --ignore=.venv --ignore=venv --cov=. --cov-config=.coveragerc --capture=no $(pytest_args) -vv
COLLECT_STATIC := python manage.py collectstatic --noinput
COMPILE_TRANSLATIONS := python manage.py compilemessages
CODECOV := \
	if [ "$$CODECOV_REPO_TOKEN" != "" ]; then \
	   codecov --token=$$CODECOV_REPO_TOKEN ;\
	fi

test:
	$(COLLECT_STATIC) && $(COMPILE_TRANSLATIONS) && $(FLAKE8) && $(PYTEST) && $(CODECOV)

DJANGO_WEBSERVER := \
	python manage.py collectstatic --noinput && \
	python manage.py runserver 0.0.0.0:$$PORT

django_webserver:
	$(DJANGO_WEBSERVER)

DEBUG_SET_ENV_VARS := \
	export PORT=8005; \
	export SECRET_KEY=debug; \
	export DEBUG=true ;\
	export DIRECTORY_API_CLIENT_API_KEY=debug; \
	export DIRECTORY_API_CLIENT_BASE_URL=http://api.trade.great:8000; \
	export RECAPTCHA_PUBLIC_KEY=$$DIRECTORY_UI_SUPPLIER_RECAPTCHA_PUBLIC_KEY; \
	export RECAPTCHA_PRIVATE_KEY=$$DIRECTORY_UI_SUPPLIER_RECAPTCHA_PRIVATE_KEY; \
	export GOOGLE_TAG_MANAGER_ID=GTM-TC46J8K; \
	export GOOGLE_TAG_MANAGER_ENV=&gtm_auth=Ok4kd4Wf_NKgs4c5Z5lUFQ&gtm_preview=env-6&gtm_cookies_win=x; \
	export UTM_COOKIE_DOMAIN=.trade.great; \
	export THUMBNAIL_STORAGE_CLASS_NAME=local-storage; \
	export THUMBNAIL_KVSTORE_CLASS_NAME=redis; \
	export REDIS_URL=redis://localhost:6379; \
	export NOCAPTCHA=true; \
	export SESSION_COOKIE_SECURE=false; \
	export SECURE_HSTS_SECONDS=0 ;\
	export SECURE_SSL_REDIRECT=false; \
	export DIRECTORY_CMS_API_CLIENT_BASE_URL=http://cms.trade.great:8010; \
	export DIRECTORY_CMS_API_CLIENT_API_KEY=debug; \
	export FEATURE_SEARCH_ENGINE_INDEXING_DISABLED=true; \
	export DIRECTORY_FORMS_API_BASE_URL=http://forms.trade.great:8011;\
	export PRIVACY_COOKIE_DOMAIN=.trade.great; \
	export HEALTH_CHECK_TOKEN=debug; \
	export FEATURE_EU_EXIT_BANNER_ENABLED=true; \
	export FEATURE_INTERNATIONAL_CONTACT_LINK_ENABLED=true; \
	export FEATURE_NEW_HEADER_FOOTER_ON=true; \
	export DIRECTORY_CONSTANTS_URL_EXPORT_READINESS=http://exred.trade.great:8007; \
	export DIRECTORY_CONSTANTS_URL_FIND_A_BUYER=http://buyer.trade.great:8001; \
	export DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS=http://soo.trade.great:8008; \
	export DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER=http://supplier.trade.great:8005; \
	export DIRECTORY_CONSTANTS_URL_INVEST=http://invest.trade.great:8012; \
	export DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON=http://sso.trade.great:8004; \
	export DIRECTORY_CONSTANTS_URL_GREAT_DOMESTIC=http://exred.trade.great:8007; \
	export CONTACT_INDUSTRY_AGENT_EMAIL_ADDRESS=buying@example.com

TEST_SET_ENV_VARS := \
	export DIRECTORY_FORMS_API_API_KEY=debug; \
	export DIRECTORY_FORMS_API_SENDER_ID=debug


debug_webserver:
	$(DEBUG_SET_ENV_VARS) && $(DJANGO_WEBSERVER)

debug_pytest:
	$(DEBUG_SET_ENV_VARS) && $(TEST_SET_ENV_VARS) && $(COLLECT_STATIC) && $(PYTEST)

debug_test:
	$(DEBUG_SET_ENV_VARS) && $(TEST_SET_ENV_VARS) && $(COLLECT_STATIC) && $(COMPILE_TRANSLATIONS) && $(FLAKE8) && $(PYTEST) --cov-report=html

debug_test_last_failed:
	make debug_test pytest_args='--last-failed'

debug_manage:
	$(DEBUG_SET_ENV_VARS) && ./manage.py $(cmd)

translations:
	$(DEBUG_SET_ENV_VARS) && python manage.py makemessages -a

compile_translations:
	$(DEBUG_SET_ENV_VARS) && $(COMPILE_TRANSLATIONS)

debug_shell:
	$(DEBUG_SET_ENV_VARS) && ./manage.py shell

debug: test_requirements debug_test

compile_requirements:
	python3 -m piptools compile requirements.in
	python3 -m piptools compile requirements_test.in

compile_css:
	./node_modules/.bin/gulp sass

watch_css:
	./node_modules/.bin/gulp sass:watch

.PHONY: build clean test_requirements debug_webserver debug_test debug heroku_deploy_dev heroku_deploy_demo
