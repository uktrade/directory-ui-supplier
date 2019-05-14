# directory-ui-supplier
[Find a Supplier](https://www.great.gov.uk/trade/)

[![code-climate-image]][code-climate]
[![circle-ci-image]][circle-ci]
[![codecov-image]][codecov]
[![gitflow-image]][gitflow]
[![calver-image]][calver]

---

## Development

### Installing

    $ git clone https://github.com/uktrade/directory-ui-supplier
    $ cd directory-ui-supplier
    $ virtualenv .venv -p python3.6
    $ source .venv/bin/activate
    $ pip install -r requirements_text.txt

### Requirements

[Python 3.6](https://www.python.org/downloads/release/python-366/)

[redis](https://redis.io/)

### Configurations

Secrets such as API keys and environment specific configurations are placed in `conf/.env` - a file that is not added to version control. You will need to create that file locally in order for the project to run.

Here are the env vars to get you going:

```
DIRECTORY_FORMS_API_API_KEY=debug
DIRECTORY_FORMS_API_SENDER_ID=debug
```

### Directory Forms

Form submissions are powered by [directory-forms-api](https://github.com/uktrade/directory-forms-api). Set that up locally then generate a API client [here](http://forms.trade.great:8011/admin/client/client/) and add the values to env vars to `conf/.env`.

### Run the webserver

    $ make debug_webserver

### Run the test

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

## Translations

Follow the [Django documentation](https://docs.djangoproject.com/en/1.9/topics/i18n/translation/#localization-how-to-create-language-files).

To create or update `.po` files:

	$ make debug_manage cmd="makemessages"

To compile `.mo` files (no need to add these to source code, as this is done automatically during build):

	$ make debug_manage cmd="compilemessages"

## Helpful links
* [Developers Onboarding Checklist](https://uktrade.atlassian.net/wiki/spaces/ED/pages/32243946/Developers+onboarding+checklist)
* [Gitflow branching](https://uktrade.atlassian.net/wiki/spaces/ED/pages/737182153/Gitflow+and+releases)
* [GDS service standards](https://www.gov.uk/service-manual/service-standard)
* [GDS design principles](https://www.gov.uk/design-principles)

 ## Related projects:
https://github.com/uktrade?q=directory
https://github.com/uktrade?q=great

[code-climate-image]: https://codeclimate.com/github/uktrade/directory-ui-supplier/badges/issue_count.svg
[code-climate]: https://codeclimate.com/github/uktrade/directory-ui-supplier

[circle-ci-image]: https://circleci.com/gh/uktrade/directory-ui-supplier/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/directory-ui-supplier/tree/master

[codecov-image]: https://codecov.io/gh/uktrade/directory-ui-supplier/branch/master/graph/badge.svg
[codecov]: https://codecov.io/gh/uktrade/directory-ui-supplier

[gitflow-image]: https://img.shields.io/badge/Branching%20strategy-gitflow-5FBB1C.svg
[gitflow]: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

[calver-image]: https://img.shields.io/badge/Versioning%20strategy-CalVer-5FBB1C.svg
[calver]: https://calver.org
