dit.tagging = dit.tagging || {};

dit.tagging.fas = new function() {
    this.init = function(page) {

        addTaggingForPageLinks();
        addTaggingForFeedbackLink();
        addTaggingForBreadcrumbs();

        $(document).ready(function() {
            switch (page) {
                case 'FindASupplierLandingPage':
                    addTaggingForCompanySearchForm();
                    addTaggingForContact();
                    addTaggingForIndustries();
                    break;

                case 'FindASupplierContactCompany' || 'FindASupplierISDContact':
                    addTaggingForContactCompanyForm();
                    break;

                case 'FindASupplierPublishedProfileDetail' || 'FindASupplierISDProfile':
                    addTaggingForContact();
                    addTaggingForCompanyWebsite();
                    addTaggingForSocialShareLinks();
                    addTaggingForCaseStudyCards();
                    addTaggingForShowFullDetails();
                    addTaggingForReportProfile();
                    break;

                case 'FindASupplierCompanySearch' || 'FindASupplierISDCompanySearch':
                    addTaggingForSupplierSearchForm();
                    addTaggingForCompanyDetailsLinks();
                    addTaggingForPagination();
                    break;

                case 'FindASupplierContactCompanySent' || 'FindASupplierISDContactSuccess':
                    addTaggingForNextSteps();
                    break;

                case 'FindASupplierCaseStudyDetail':
                    addTaggingForShowCompanyDetail();
                    addTaggingForContact();
                    addTaggingForCompanyWebsite();
                    addTaggingForReportProfile();
                    break;

                case 'FindASupplierAnonymousSubscribeForm':
                    addTaggingForSubscribeForm();
                    addTaggingForTermsAndConditions();
                    break;

                case 'FindASupplierLeadGenerationForm':
                    addTaggingForLeadGenerationForm();
                    addTaggingForTermsAndConditions();
                    break;

                case 'FindASupplierIndustryArticle':
                    addTaggingForContact();
                    addTaggingForSocialShareLinks();
                    addTaggingForAnchorTags();
                    break;

                case 'FindASupplierIndustryDetailContact':
                    addTaggingForContactIndustryForm();
                    break;

                case 'FindASupplierIndustryDetail':
                    addTaggingForContact();
                    addTaggingForCompanySearchForm();
                    addTaggingSearchCompanies();
                    addTaggingForArticleSummaries();
                    break;

                case 'FindASupplierIndustryLandingPage':
                    addTaggingForContact();
                    addTaggingForFeaturedIndustries();
                    break;

                case 'FindASupplierISDHome':
                    addTaggingForISDSearchForm();
                    addTaggingForServiceSearchLinks();
                    break;

                case 'FindASupplierAnonymousUnsubscribe':
                    addTaggingForUnsubscribeForm();
                    break;

                default:
                    // do nothing
            }
        });

        function addTaggingForFeedbackLink() {
            $("[data-ga-class='feedback-link']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'Feedback'))
            });
        }

        function addTaggingForCompanySearchForm() {
            $("[data-ga-class='company-search-form']").on('submit', function() {
                var value = "Search: " + getSearchInputText() + " :: Filter: " + getIndustryFilterValue();
                sendEvent(formEvent("CompanySearch", value));
            });
        }

        function addTaggingForSupplierSearchForm() {
            $("[data-ga-class='search-form']").on('submit', function() {
                sendEvent(formEvent("Search", getSearchInputText()));
            });

            $("[data-ga-class='clear-filter']").on('click', function () {
                sendEvent(event("Clear", "Form", "Search", $(this).text()))
            });

            $("[data-ga-class='reset']").on('click', function () {
                sendEvent(event("Reset", "Form", "Search", $(this).text()))
            });
        }

        function addTaggingForSubscribeForm() {
            $("[data-ga-class='subscribe-form']").on('submit', function() {
                sendEvent(formEvent("SubscribeToSector", getSectorInputText()));
            });
        }

        function addTaggingForLeadGenerationForm() {
            $("[data-ga-class='lead-generation-form']").on('submit', function() {
                sendEvent(formEvent("LeadGeneration", ''));
            });
        }

        function addTaggingForContactIndustryForm() {
            $("[data-ga-class='contact-industry-form']").on('submit', function() {
                sendEvent(formEvent("ContactIndustry", $(this).data('ga-value')));
            });
        }

        function addTaggingForContactCompanyForm() {
            $("[data-ga-class='contact-form']").on('submit', function() {
                sendEvent(formEvent("CompanyContact", $(this).data('ga-value')));
            });
        }

        function addTaggingForISDSearchForm() {
            $("[data-ga-class='isd-search-form']").on('submit', function() {
                sendEvent(formEvent("ISDSearch", getSearchInputText()));
            });

            $("[data-ga-class='clear-filter']").on('click', function () {
                sendEvent(event("Clear", "Form", "ISDSearch", $(this).text()))
            })
        }

        function addTaggingForUnsubscribeForm() {
            $("[data-ga-class='unsubscribe-form']").on('submit', function() {
                sendEvent(formEvent("Unsubscribe", ''));
            });
        }

        function getSearchInputText() {
            return $("[data-ga-id='search-input']").val();
        }

        function getSectorInputText() {
            return $("[data-ga-id='sector-input']").val();
        }

        function getIndustryFilterValue() {
            return $("[data-ga-id='select-input-container']").find('select').val() || 'NONE';
        }

        function addTaggingForContact() {
            $("[data-ga-class='contact-cta']").on('click', function() {
                sendEvent(ctaEvent($(this).text(), "Contact"));
            });
        }

        function addTaggingForPageLinks() {
            $("[data-ga-class='cta']").on('click', function() {
                sendEvent(ctaEvent($(this).text()));
            });
        }

        function addTaggingForSocialShareLinks() {
            $("[data-ga-class='social-share-link']").on('click', function () {
                sendEvent(event('Link', 'Share', 'Social', $(this).data('ga-value')));
            });
        }

        function addTaggingForCaseStudyCards() {
            $("[data-ga-class='case-study-card']").on('click', function () {
                sendEvent(ctaEvent($(this).data('ga-value'), "CaseStudy"));
            });
        }

        function addTaggingForCompanyWebsite() {
            $("[data-ga-class='company-website']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), "CompanyWebsite"));
            });
        }

        function addTaggingForShowFullDetails() {
            $("[data-ga-class='full-details']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), "ShowFullDetails"));
            });
        }

        function addTaggingForCompanyDetailsLinks() {
            $("[data-ga-class='company-detail-link']").on('click', function () {
                sendEvent(ctaEvent($(this).data('ga-value'), 'CompanyDetailsLink'))
            });

            $("[data-ga-class='company-detail-logo']").on('click', function () {
                sendEvent(ctaEvent($(this).data('ga-value'), 'CompanyDetailsLogo'))
            });
        }

        function addTaggingForPagination() {
            $("[data-ga-class='pagination']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'Pagination'))
            })
        }

        function addTaggingForShowCompanyDetail() {
            $("[data-ga-class='company-detail-link']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'CompanyDetails'))
            })
        }

        function addTaggingForReportProfile() {
            $("[data-ga-class='report-profile']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'ReportProfile'))
            })
        }

        function addTaggingForIndustries() {
            $("[data-ga-class='industry-card']").on('click', function () {
                sendEvent(ctaEvent($(this).data('ga-value'), 'Industries'))
            });

            $("[data-ga-class='all-industries-link']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'Industries'))
            })
        }

        function addTaggingForTermsAndConditions() {
            $("[data-ga-class='terms-and-coniditions']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'TermsAndConditions'))
            })
        }

        function addTaggingForBreadcrumbs() {
            $("[data-ga-class='breadcrumbs']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'Breadcrumbs'))
            })
        }

        function addTaggingSearchCompanies() {
            $("[data-ga-class='company-link']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'SearchCompanies'))
            })
        }

        function addTaggingForFeaturedIndustries() {
            $("[data-ga-class='industry-link']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'FeaturedIndustries'))
            })
        }

        function addTaggingForArticleSummaries() {
            $("[data-ga-class='article-summary']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'ArticleSummaries'))
            })
        }

        function addTaggingForServiceSearchLinks() {
            $("[data-ga-class='search-link']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'ServiceSearchLinks'))
            })
        }

        function addTaggingForNextSteps() {
            $("[data-ga-class='next-steps']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'NextSteps'))
            })
        }

        function addTaggingForAnchorTags() {
            $("[data-ga-class='anchor-tags']").on('click', function () {
                sendEvent(ctaEvent($(this).text(), 'AnchorTags'))
            })
        }

        function ctaEvent(linkText, element) {
            return event("Link", "CTA", element, linkText)
        }

        function formEvent(element, value) {
            return event("Submit", "Form", element, value)
        }

        function event(action, type, element, value) {
            var event = {
                'event': 'gaEvent',
                'action': action,
                'type': type,
                'value': value
            };

            if (element) {
                event.element = element;
            }

            return event;
        }

        function sendEvent(event) {
            window.dataLayer.push(event);
        }
    };
};
