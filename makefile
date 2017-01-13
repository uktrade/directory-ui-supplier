build: docker_test

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

test_requirements:
	pip install -r requirements_test.txt

API_CLIENT_ENV_VARS := API_CLIENT_KEY=debug API_CLIENT_BASE_URL=http://debug
FLAKE8 := flake8 . --exclude=migrations
PYTEST := pytest . --cov=. --cov-config=.coveragerc --capture=no $(pytest_args)
COLLECT_STATIC := python manage.py collectstatic --noinput

test:
	$(COLLECT_STATIC) && $(FLAKE8) && $(API_CLIENT_ENV_VARS) $(PYTEST)

DJANGO_WEBSERVER := \
	python manage.py collectstatic --noinput && \
	python manage.py runserver 0.0.0.0:$$PORT

django_webserver:
	$(DJANGO_WEBSERVER)

DOCKER_COMPOSE_REMOVE_AND_PULL := docker-compose -f docker-compose.yml -f docker-compose-test.yml rm -f && docker-compose -f docker-compose.yml -f docker-compose-test.yml pull
DOCKER_COMPOSE_CREATE_ENVS := python ./docker/env_writer.py ./docker/env.json ./docker/env.test.json

docker_run:
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose up --build

DOCKER_SET_DEBUG_ENV_VARS := \
	export DIRECTORY_UI_SUPPLIER_API_CLIENT_CLASS_NAME=unit-test; \
	export DIRECTORY_UI_SUPPLIER_API_CLIENT_KEY=debug; \
	export DIRECTORY_UI_SUPPLIER_API_CLIENT_BASE_URL=http://api.trade.great.dev:8000; \
	export DIRECTORY_UI_SUPPLIER_PORT=8005; \
	export DIRECTORY_UI_SUPPLIER_SECRET_KEY=debug; \
	export DIRECTORY_UI_SUPPLIER_DEBUG=true; \
	export DIRECTORY_UI_SUPPLIER_FEATURE_LANGUAGE_SWITCHER_ENABLED=true; \
	export DIRECTORY_UI_SECTOR_LINKS_JSON=\{\"CREATIVE_AND_MEDIA\":\{\"company_one\":\"https:\/\/www.example.com\",\"company_two\":\"http:\/\/www.example.com\",\"case_study\":\"http:\/\/www.example.com\"\},\"HEALTHCARE_AND_MEDICAL\":\{\"company_one\":\"http:\/\/www.example.com\",\"company_two\":\"http:\/\/www.example.com\",\"case_study\":\"http:\/\/www.example.com\"\},\"FOOD_AND_DRINK\":\{\"company_one\":\"http:\/\/www.example.com\",\"company_two\":\"http:\/\/www.example.com\",\"case_study\":\"http:\/\/www.example.com\"\},\"SOFTWARE_AND_COMPUTER_SERVICES\":\{\"company_one\":\"http:\/\/www.example.com\",\"company_two\":\"http:\/\/www.example.com\",\"case_study\":\"http:\/\/www.example.com\"\}\}


DOCKER_REMOVE_ALL := \
	docker ps -a | \
	grep directoryui_ | \
	awk '{print $$1 }' | \
	xargs -I {} docker rm -f {}

docker_remove_all:
	$(DOCKER_REMOVE_ALL)

docker_debug: docker_remove_all
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	docker-compose pull && \
	docker-compose build && \
	docker-compose run --service-ports webserver make django_webserver

docker_webserver_bash:
	docker exec -it directoryui_webserver_1 sh

docker_test: docker_remove_all
	$(DOCKER_SET_DEBUG_ENV_VARS) && \
	$(DOCKER_COMPOSE_CREATE_ENVS) && \
	$(DOCKER_COMPOSE_REMOVE_AND_PULL) && \
	docker-compose -f docker-compose-test.yml build && \
	docker-compose -f docker-compose-test.yml run sut

docker_build:
	docker build -t ukti/directory-ui-supplier:latest .

DEBUG_SET_ENV_VARS := \
	export PORT=8005; \
	export SECRET_KEY=debug; \
	export DEBUG=true ;\
	export API_CLIENT_CLASS_NAME=unit-test; \
	export API_CLIENT_KEY=debug; \
	export API_CLIENT_BASE_URL=http://api.trade.great.dev:8000; \
	export FEATURE_LANGUAGE_SWITCHER_ENABLED=true; \
	export SECTOR_LINKS_JSON=\{\"CREATIVE_AND_MEDIA\":\{\"company_one\":\"https:\/\/www.example.com\",\"company_two\":\"http:\/\/www.example.com\",\"case_study\":\"http:\/\/www.example.com\"\},\"HEALTHCARE_AND_MEDICAL\":\{\"company_one\":\"http:\/\/www.example.com\",\"company_two\":\"http:\/\/www.example.com\",\"case_study\":\"http:\/\/www.example.com\"\},\"FOOD_AND_DRINK\":\{\"company_one\":\"http:\/\/www.example.com\",\"company_two\":\"http:\/\/www.example.com\",\"case_study\":\"http:\/\/www.example.com\"\},\"SOFTWARE_AND_COMPUTER_SERVICES\":\{\"company_one\":\"http:\/\/www.example.com\",\"company_two\":\"http:\/\/www.example.com\",\"case_study\":\"http:\/\/www.example.com\"\}\}


debug_webserver:
	$(DEBUG_SET_ENV_VARS) && $(DJANGO_WEBSERVER)

debug_pytest:
	$(DEBUG_SET_ENV_VARS) && $(COLLECT_STATIC) && $(PYTEST)

debug_test:
	$(DEBUG_SET_ENV_VARS) && $(COLLECT_STATIC) && $(FLAKE8) && $(PYTEST) --cov-report=html

debug_manage:
	$(DEBUG_SET_ENV_VARS) && ./manage.py $(cmd)

debug_shell:
	$(DEBUG_SET_ENV_VARS) && ./manage.py shell

debug: test_requirements debug_test

heroku_deploy_dev:
	docker build -t registry.heroku.com/directory-ui-supplier-dev/web .
	docker push registry.heroku.com/directory-ui-supplier-dev/web

.PHONY: build clean test_requirements docker_run docker_debug docker_webserver_bash docker_test debug_webserver debug_test debug heroku_deploy_dev heroku_deploy_demo
