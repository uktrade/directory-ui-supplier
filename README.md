# directory-ui-supplier
[Export Directory UI](https://www.directory.exportingisgreat.gov.uk/)

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gemnasium-image]][gemnasium]

---
### See also:
| [directory-api](https://github.com/uktrade/directory-api) | [directory-ui-buyer](https://github.com/uktrade/directory-ui-buyer) | [directory-ui-supplier](https://github.com/uktrade/directory-ui-supplier) | [directory-ui-export-readiness](https://github.com/uktrade/directory-ui-export-readiness) |
| --- | --- | --- | --- |
| **[directory-sso](https://github.com/uktrade/directory-sso)** | **[directory-sso-proxy](https://github.com/uktrade/directory-sso-proxy)** | **[directory-sso-profile](https://github.com/uktrade/directory-sso-profile)** |  |

For more information on installation please check the [Developers Onboarding Checklist](https://uktrade.atlassian.net/wiki/spaces/ED/pages/32243946/Developers+onboarding+checklist)

## Requirements

[Python 3.5](https://www.python.org/downloads/release/python-350/)

[Docker >= 1.10](https://docs.docker.com/engine/installation/)

[Docker Compose >= 1.8](https://docs.docker.com/compose/install/)


## Local installation

    $ git clone https://github.com/uktrade/directory-ui-supplier
    $ cd directory-ui-supplier
    $ make

## Running with Docker
Requires all host environment variables to be set.

    $ make docker_run

### Run debug webserver in Docker

    $ brew link gettext --force (OS X only)
    $ make docker_debug

### Run tests in Docker

    $ make docker_test

### Host environment variables for docker-compose
``.env`` files will be automatically created (with ``env_writer.py`` based on ``env.json``) by ``make docker_test``, based on host environment variables with ``DIRECTORY_UI_SUPPLIER_`` prefix.

#### Web server
| Host environment variable | Docker environment variable  |
| ------------- | ------------- |
| DIRECTORY_UI_SUPPLIER_SECRET_KEY | SECRET_KEY |
| DIRECTORY_UI_SUPPLIER_PORT | PORT |
| DIRECTORY_UI_SUPPLIER_API_SIGNATURE_SECRET | API_SIGNATURE_SECRET |
| DIRECTORY_UI_SUPPLIER_API_CLIENT_BASE_URL | API_CLIENT_BASE_URL |
| DIRECTORY_UI_SUPPLIER_COMPANIES_HOUSE_SEARCH_URL | COMPANIES_HOUSE_SEARCH_URL |
| DIRECTORY_UI_SUPPLIER_SSO_API_CLIENT_BASE_URL | SSO_API_CLIENT_BASE_URL |
| DIRECTORY_UI_SUPPLIER_UI_SESSION_COOKIE_SECURE | UI_SESSION_COOKIE_SECURE |

## Debugging

### Setup debug environment

    $ make debug

### Run debug webserver

    $ make debug_webserver

### Run debug tests

    $ make debug_test

## CSS development

### Requirements
[node](https://nodejs.org/en/download/)
[SASS](http://sass-lang.com/)

	$ npm install
	$ npm run sass-dev

### Update CSS under version control

	$ npm run sass-prod

### Rebuild the CSS files when the scss file changes

	$ npm run sass-watch

## Session

Signed cookies are used as the session backend to avoid using a database. We therefore must avoid storing non-trivial data in the session, because the browser will be exposed to the data.


## SSO
To make sso work locally add the following to your machine's `/etc/hosts`:

| IP Adress | URL                  |
| --------  | -------------------- |
| 127.0.0.1 | buyer.trade.great    |
| 127.0.0.1 | supplier.trade.great |
| 127.0.0.1 | sso.trade.great      |
| 127.0.0.1 | api.trade.great      |
| 127.0.0.1 | profile.trade.great  |
| 127.0.0.1 | exred.trade.great    |

Then log into `directory-sso` via `sso.trade.great:8004`, and use `directory-ui-supplier` on `supplier.trade.great:8005`

Note in production, the `directory-sso` session cookie is shared with all subdomains that are on the same parent domain as `directory-sso`. However in development we cannot share cookies between subdomains using `localhost` - that would be like trying to set a cookie for `.com`, which is not supported by any RFC.

Therefore to make cookie sharing work in development we need the apps to be running on subdomains. Some stipulations:
 - `directory-ui-supplier` and `directory-sso` must both be running on sibling subdomains (with same parent domain)
 - `directory-sso` must be told to target cookies at the parent domain.

## Translations

Follow the <a href="https://docs.djangoproject.com/en/1.9/topics/i18n/translation/#localization-how-to-create-language-files" target="_blank">Django documentation</a>

To create or update `.po` files:

	$ make debug_manage cmd="makemessages"

To compile `.mo` files (no need to add these to source code, as this is done automatically during build):

	$ make debug_manage cmd="compilemessages"


[code-climate-image]: https://codeclimate.com/github/uktrade/directory-ui-supplier/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/directory-ui-supplier

[circle-ci-image]: https://circleci.com/gh/uktrade/directory-ui-supplier/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-ui-supplier/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-ui-supplier/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-ui-supplier

[gemnasium-image]: https://gemnasium.com/badges/github.com/uktrade/directory-ui-supplier.svg
[gemnasium]: https://gemnasium.com/github.com/uktrade/directory-ui-supplier
