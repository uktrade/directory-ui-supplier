dit.tagging = dit.tagging || {};

dit.tagging.fas = new function() {
    this.init = function(page) {
        $(document).ready(function() {
            switch (page) {
                case 'FindASupplierLandingPage':
                    addTaggingForSearch();
                    addTaggingForContact();
                    break;
                default:
                    // do nothing
            }
        });

        function addTaggingForSearch() {
            $("[data-ga-class='company-search-form']").on('submit', function() {
                window.dataLayer.push({
                    'eventAction': 'Search',
                    'eventCategory': 'Search Form',
                    'eventLabel': 'Find A Supplier',
                    'eventValue': "Search: " + getSearchInputText() + " :: Filter: " + getIndustryFilterValue()
                });
            });
        }

        function getSearchInputText() {
            return $("[data-ga-id='search-input']").val();
        }

        function getIndustryFilterValue() {
            return $("[data-ga-id='select-input-container']").find('select').val() || 'NONE';
        }

        function addTaggingForContact() {
            $("[data-ga-class='contact-cta']").on('click', function() {
                window.dataLayer.push({
                    'eventAction': 'Cta',
                    'eventCategory': 'Contact',
                    'eventLabel': 'Link',
                    'eventValue': $(this).text()
                });
            });
        }
    };
};
