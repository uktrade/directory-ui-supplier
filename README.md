# directory-ui-supplier
[Export Directory UI](https://www.directory.exportingisgreat.gov.uk/)

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]

---
### See also:
| [directory-api](https://github.com/uktrade/directory-api) | [directory-ui-buyer](https://github.com/uktrade/directory-ui-buyer) | [directory-ui-supplier](https://github.com/uktrade/directory-ui-supplier) | [directory-ui-export-readiness](https://github.com/uktrade/directory-ui-export-readiness) |
| --- | --- | --- | --- |
| **[directory-sso](https://github.com/uktrade/directory-sso)** | **[directory-sso-proxy](https://github.com/uktrade/directory-sso-proxy)** | **[directory-sso-profile](https://github.com/uktrade/directory-sso-profile)** |  |

For more information on installation please check the [Developers Onboarding Checklist](https://uktrade.atlassian.net/wiki/spaces/ED/pages/32243946/Developers+onboarding+checklist)

## Requirements

[Python 3.6](https://www.python.org/downloads/release/python-366/)

[redis](https://redis.io/)


## Local installation

    $ git clone https://github.com/uktrade/directory-ui-supplier
    $ cd directory-ui-supplier
    $ make

## Directory Forms

Form submissions are powered by [directory-forms-api](https://github.com/uktrade/directory-forms-api). Set that up locally then generate a API client [here](http://forms.trade.great:8011/admin/client/client/) and add the following entries to your `conf/.env`.

| Host environment variable                         | Notes                             |
| ------------------------------------------------- | --------------------------------- |
| DIRECTORY_UI_SUPPLIER_DIRECTORY_FORMS_API_API_KEY | Populate from client `access_key` |
| DIRECTORY_UI_SUPPLIER_DIRECTORY_FORMS_API_SENDER_ID   | Populate from client `identifier` |

## Debugging

### Setup debug environment

    $ make debug

### Run debug webserver

    $ make debug_webserver

### Run debug tests

    $ make debug_test

## CSS development

If you're doing front-end development work you will need to be able to compile the SASS to CSS. For this you need:

    $ npm install yarn
    $ yarn install --production=false

We add compiled CSS files to version control. This will sometimes result in conflicts if multiple developers are working on the same SASS files. However, by adding the compiled CSS to version control we avoid having to install node, npm, node-sass, etc to non-development machines.

You should not edit CSS files directly, instead edit their SCSS counterparts.

### Update CSS under version control

	$ gulp make compile_css

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
| 127.0.0.1 | forms.trade.great    |

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
