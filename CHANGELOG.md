# Changelog

## [2019.05.16](https://github.com/uktrade/directory-ui-supplier/releases/tag/2019.05.16)

[Full Changelog](https://github.com/uktrade/directory-ui-supplier/compare/2019.04.14...2019.05.16)

### Implemented enhancements

- TT-1443 - Add ISD home page images.
- CMS-1528 - Add feature flag for country select header.
- CMS-108 - Temporarily turn off additional GA tagging.

### Fixed bugs

- TT-1462 - Solve padding bug fix on ISD search.
- TT-1409 - Fixed the links to filtered search on ISD home page.
- TT-1441 - Fixed search results broken layout.
- TT-1318 - Improved consistency of header styles across pages
- TT-1476 - Fix Title to show 'Find a UK Specialist'

## [2019.05.14](https://github.com/uktrade/directory-ui-supplier/releases/tag/2019.05.14)

[Full Changelog](https://github.com/uktrade/directory-ui-supplier/compare/2019.04.25...2019.05.14)

### Implemented enhancements

- TT-1328 - Added Investment Support Directory profile.
- TT-1352 - Added Investment Support Directory search.
- TT-1320 - Added Investment Support Directory contact.
- TT-1437 - Link case study to ISD profile if ingress was ISD profile.
- TT-1395 - Send ISD Contact notification to support.

### Fixed bugs:

- CMS-1261 - Fixed missing search icon on industry page
- CMS-1256 - Fix mobile vertical spacing in footer
- CMS-1262 - Fix mobile column spacing on industries list page
- TT-1339 - Display keywords added via new profile "other" expertise interface
- TT-1345 - Fixed position of logos on ISD profile.
- CMS-1395 - Fix language cookie name and domain to be the same across all our services.
- TT-1345 - Fixed position of logos on ISD profile.
- TT-1428 - ISD companies 404 if they are also not published to FAS.
- TT-1409 - Fixed the missing links under 'Business Support' Category
- TT-1409 - Fixed the links to filtered search on ISD home page


## [2019.04.25](https://github.com/uktrade/directory-ui-supplier/releases/tag/2019.04.25)

[Full Changelog](https://github.com/uktrade/directory-ui-supplier/compare/2019.04.03...2019.04.25)

### Implemented enhancements:

- Upgraded [CMS client][directory-cms-client] to allow `lookup_by_path`, to facilitate CMS tree based routing.
- Upgraded [CMS client][directory-cms-client] reduces noisy fallback cache logging.
- Upgraded [API client][directory-api-client], [Forms client][directory-forms-api-client] and because [CMS client][directory-cms-client] upgrade results in [Client core][directory-client-core] being upgraded.
- Added `DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS` env var.
- Use international header and base templates provided by [Directory components][directory-components].
- Implement language switching introduced in the international header and footer
- Hard-code /trade/ url prefix (was previously feature flagged).
- Upgraded [Constants][directory-constants].
- Removed application-level IP filtering (replaced with routing solution at platform level).
- Added fallback cache for API
- GA360 changes FAB search to use q instead of term. Redirect also in place for backwards compatibility.
- GA360 change isd search to use q instead of term.

### Fixed bugs:

- Upgraded urllib3 to fix [vulnerability](https://nvd.nist.gov/vuln/detail/CVE-2019-11324)
- Fixed 500 internal server error response on contact forms caused by slugs


[directory-api-client]: https://github.com/uktrade/directory-api-client
[directory-client-core]: https://github.com/uktrade/directory-client-core
[directory-cms-client]: https://github.com/uktrade/directory-cms-client
[directory-forms-api-client]: https://github.com/uktrade/directory-forms-api-client
[directory-components]: https://github.com/uktrade/directory-components
[directory-constants]: https://github.com/uktrade/directory-constants
