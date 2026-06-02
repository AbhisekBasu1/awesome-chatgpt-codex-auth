# Security Policy

This repo lists tools that often touch sensitive local developer environments: terminals, editors, source code, OAuth tokens, and local proxy ports.

## Reporting a security issue in this repo

If you find a malicious listing, credential-harvesting project, or dangerous recommendation, please open a private security advisory if GitHub supports it for the repo, or open an issue with minimal public details and mark it clearly as security-sensitive.

## Security expectations for listed tools

Projects are better candidates when they:

- Use OAuth/device-code flows instead of asking users to paste cookies.
- Document where tokens are stored.
- Avoid sending source code to unexpected third-party servers.
- Avoid public unauthenticated local proxy endpoints.
- Provide clear permissions and revocation guidance.

## High-risk categories

Local API shims, reverse proxies, account pools, and tools using undocumented endpoints should be marked `experimental-proxy` or `high-risk` and should include a caution note.

Listings are not endorsements. Review each project before use.
