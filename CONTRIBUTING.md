# Contributing

Thanks for helping build **awesome-chatgpt-codex-auth**.

The goal is to curate tools that let developers authenticate through ChatGPT, Codex OAuth, Codex app-server auth, or local Codex sign-in for real workflows. Quality, evidence, and security caveats matter more than list size.

## Inclusion Criteria

A project should be included only when it satisfies all of the following:

- It publicly documents ChatGPT account sign-in, ChatGPT subscription support, OpenAI Codex OAuth, Codex app-server managed auth, or reuse of a local Codex sign-in.
- The subscription-auth flow is a meaningful feature, not a rumor, search snippet, or buried issue comment.
- The project is installable or usable by developers.
- The listing links to durable public evidence.

## Exclusion Criteria

Do not add:

- OpenAI API-only clients.
- Account resellers, shared-account services, token marketplaces, or unlimited Plus products.
- Tools designed primarily for quota evasion, credential sharing, or resale.
- Projects that require pasting raw cookies/session tokens unless the security model is unusually clear and the listing is marked high-risk.
- Abandoned forks with no unique subscription-auth support.

## Status Labels

Use the most conservative status that fits:

- `official` - official OpenAI project or first-party product surface.
- `documented-third-party` - third-party project with public docs for ChatGPT/Codex subscription sign-in.
- `experimental-adapter` - plugin, adapter, bridge, or CLI wrapper that may depend on local Codex behavior.
- `experimental-proxy` - local API server, OpenAI-compatible shim, or reverse proxy backed by subscription auth.
- `high-risk` - account pooling, undocumented endpoints, credential-sensitive architecture, or terms-sensitive behavior.

## Adding A Project

1. Add the project to [`data/projects.json`](data/projects.json).
2. Do not edit `README.md` or `data/catalog.json` by hand.
3. Regenerate outputs:

```bash
python3 scripts/generate_outputs.py
```

4. Validate the repo:

```bash
python3 scripts/validate_data.py
python3 scripts/generate_outputs.py --check
```

5. Optionally check external links:

```bash
python3 scripts/check_links.py --verify-evidence
```

6. Open a PR with evidence links and caveats.

## Required Fields

Each project must include:

- `name` and `slug`.
- `category` and `status`.
- `auth`, listing the concrete auth path.
- `subscription_auth_support`, summarizing how the ChatGPT/Codex auth flow works.
- `description`, `url`, and one or more `docs` evidence URLs.
- `notes`, especially for limitations, security, terms, proxy behavior, or plan caveats.
- `last_verified` in `YYYY-MM-DD` format.

## Preferred Wording

Use precise wording:

- Good: "Docs say it supports OpenAI Codex OAuth with ChatGPT Plus/Pro."
- Good: "Uses a local Codex CLI session; experimental adapter."
- Avoid: "Free API access."
- Avoid: "Unlimited ChatGPT API."
- Avoid: "Bypasses API billing."

## Verification Date

Set `last_verified` to the date you checked the docs in `YYYY-MM-DD` format. Current seed date: `2026-06-02`.
