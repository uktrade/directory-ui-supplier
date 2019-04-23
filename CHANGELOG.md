# Changelog

## Pre-release

**Implemented enhancements:**

- Upgraded [CMS client][directory-cms-client] to allow `lookup_by_path`, to facilitate CMS tree based routing.
- Upgraded [CMS client][directory-cms-client] reduces noisy fallback cache logging.
- Upgraded [API client][directory-api-client], [Forms client][directory-forms-api-client] and because [CMS client][directory-cms-client] upgrade results in [Client core][directory-client-core] being upgraded.
- Added `DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS` env var.
- Use international header and base templates provided by [Directory components][directory-components].
- Hard-code /trade/ url prefix (was previously feature flagged).
- Upgraded [Constants][directory-constants].
- Removed application-level IP filtering (replaced with routing solution at platform level).
- Added Investment Support Directory profile.
- Added fallback cache for API

**Fixed bugs:**
- Upgraded urllib3 to fix [vulnerability](https://nvd.nist.gov/vuln/detail/CVE-2019-11324)


[directory-api-client]: https://github.com/uktrade/directory-api-client
[directory-client-core]: https://github.com/uktrade/directory-client-core
[directory-cms-client]: https://github.com/uktrade/directory-cms-client
[directory-forms-api-client]: https://github.com/uktrade/directory-forms-api-client
[directory-components]: https://github.com/uktrade/directory-components
[directory-constants]: https://github.com/uktrade/directory-constants
