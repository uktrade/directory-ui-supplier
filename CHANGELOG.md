# Changelog

## Pre release

### Implemented enhancements

- TT-1556 - Add newsletter subscribe form on FAS results pages
- TT-1518 - Port ISD search changes to FAS
    + TT-1546 - Fix FAS page title
    + TT-1567 - Remove "free advice" for FAS profiles
    + TT-1551 - Remove unwanted capitalisation from industries
    + TT-1527 - Replace "of" with "for" International Trade
    + TT-1539 - Fix bad text wrapping on tablet
- TT-1506 - Port ISD profile changes to FAS
- TT-1505 - Port ISD contact change to FAS
- CI-108 - Add more tags for GA 360
- TT-1545 - Change Filter Labels
- no ticket - Remove obsolete feature of showing article_summaries on FAS homepage
- TT-1505 - Send FAS message via notify
- TT-1522 - Improve the content of FAS contact form

## Fixed bugs

- No ticket - Remove noisy CMS healthcheck
- TT-1532 - Fix FAS Pagination
- TT-1530 - profile links corrupt
- TT-1534 - FAS Breadcrumb search results
- TT-1536 - 500-Error-on-Results upgraded sorl-thumbnail to 12.5
- TT-1528 - 500 ISE on industry page
- CI-217 - Update Django Version to fix security vulnerability.
- TT-1529 - Fix 500 error pages so links work
- TT-1531 FAS - Logos are misaligned on trade profiles (fixed cross browser compatibility issues)
- TT-1547 - Prevent FAS "&sectors=" getting encoded as "§ors=" by renaming to industries.
- TT-1522 - fix none when clear filters ISD search
- TT-1576 -fix next allignment


## [2019.06.05] (https://github.com/uktrade/directory-ui-supplier/releases/tag/2019.06.05)
[Full Changelog](https://github.com/uktrade/directory-ui-supplier/compare/2019.05.28_1...2019.06.05)

### Implemented enhancements

- TT-1477 - Improve breadcrumbs on ISD pages
- CI-108 - Add back sending additional data to GA 360, and update this data to newest spec.
- TT-1492 Add link to T&Cs on disclaimer page
- No ticket - Show ISD address only if not in companies house
- TT-1478 - Improve content on ISD search page for communicating not results. Persist search filters on viewing ISD profile and contracting company.
- No ticket - Remove `FEATURE_INVESTMENT_SUPPORT_DIRECTORY_ENABLED` feature flag

## Fixed bugs

- TT-1486 - Fixed ISD results issue on IE11
- TT-1474 - Fixed missing social links images
- No ticket - Fall loudly id redis is not configured
- TT-1482 - Reduce font size of ISD selected filters
- TT-1422 - Added "filter results" title to ISD

## [2019.05.28] (https://github.com/uktrade/directory-ui-supplier/releases/tag/2019.05.28)
[Full Changelog](https://github.com/uktrade/directory-ui-supplier/compare/2019.05.23...2019.05.28)

### Implemented enhancements

### Fixed bugs
- TT-1487 403-on-specialist-filters change HR specialist rendering 
- TT-1487 403-on-specialist-filters change pagination to handle HR filters
- TT-1487 403-on-specialist-filters remove labels from pagination
- TT-1321-industry-rewording

## [2019.05.23](https://github.com/uktrade/directory-ui-supplier/releases/tag/2019.05.23)

[Full Changelog](https://github.com/uktrade/directory-ui-supplier/compare/2019.05.16...2019.05.23)

### Implemented enhancements

### Fixed bugs
- TT-1487 403-on-specialist-filters upgrade directory components
- TT-1485 Make ISD root 
- TT-1489 Redirect Trade/Investment-support-directory/ to /Investment-support-directory/


## [2019.05.16](https://github.com/uktrade/directory-ui-supplier/releases/tag/2019.05.16)

[Full Changelog](https://github.com/uktrade/directory-ui-supplier/compare/2019.04.14...2019.05.16)

### Implemented enhancements

- TT-1443 - Add ISD home page images.
- CMS-1528 - Add feature flag for country select header.
- CMS-108 - Temporarily turn off additional GA tagging.
- TT-1383 - Return all ISD companies if no terms supplied. 

### Fixed bugs

- TT-1462 - Solve padding bug fix on ISD search.
- TT-1409 - Fixed the links to filtered search on ISD home page.
- TT-1441 - Fixed search results broken layout.
- TT-1318 - Improved consistency of header styles across pages
- TT-1476 - Fix Title to show 'Find a UK Specialist'
- TT-1479 - Pagination on products & services clears filters

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
