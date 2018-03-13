#!/bin/bash
# This script will render the project css files.

# put the path of library scss files we want to incluide
libraries="\
	--load-path node_modules/govuk_frontend_toolkit/stylesheets \
	--load-path node_modules/trade_elements/sass \
	--load-path enrolment/static/sass \
	--load-path node_modules/govuk-elements-sass/public/sass \
"

# put the path of source code files we want to include, and where we want them
# to be exported to e.g., input.scss:output.css
input_output_map="\
	enrolment/static/sass/main.scss:enrolment/static/main.css \
	enrolment/static/sass/main-bidi.scss:enrolment/static/main-bidi.css \
	enrolment/static/sass/enrolment.scss:enrolment/static/enrolment.css \
	enrolment/static/sass/company-profile-details.scss:enrolment/static/company-profile-details.css \
	enrolment/static/sass/company-profile-details-bidi.scss:enrolment/static/company-profile-details-bidi.css \
	enrolment/static/sass/company-profile-form.scss:enrolment/static/company-profile-form.css \
	enrolment/static/sass/supplier-profile-details.scss:enrolment/static/supplier-profile-details.css \
	enrolment/static/sass/supplier-case-study-detail.scss:enrolment/static/supplier-case-study-detail.css \
	enrolment/static/sass/landing-page.scss:enrolment/static/landing-page.css \
	enrolment/static/sass/landing-page-bidi.scss:enrolment/static/landing-page-bidi.css \
	enrolment/static/sass/marketing-page.scss:enrolment/static/marketing-page.css \
	enrolment/static/sass/marketing-page-bidi.scss:enrolment/static/marketing-page-bidi.css \
	enrolment/static/sass/legal.scss:enrolment/static/legal.css \
	enrolment/static/sass/ie8fixes.scss:enrolment/static/ie8fixes.css \
	enrolment/static/sass/company-search_results.scss:enrolment/static/company-search_results.css \
	enrolment/static/sass/lead-generation-page.scss:enrolment/static/lead-generation-page.css \
	enrolment/static/sass/industries.scss:enrolment/static/industries.css \
	enrolment/static/sass/industry-article.scss:enrolment/static/industry-article.css \

"

prod_command="sass --sourcemap=none --style compressed"

eval 'rm enrolment/static/*.css'
eval $prod_command$libraries$input_output_map
