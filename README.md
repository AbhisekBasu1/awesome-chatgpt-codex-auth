# Awesome ChatGPT/Codex Auth [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated index of developer tools that authenticate through ChatGPT, Codex OAuth, Codex app-server auth, or a local Codex sign-in instead of requiring a separate OpenAI Platform API key.

## Contents

- [Legend](#legend)
- [Summary](#summary)
- [Projects](#projects)
- [Methodology](#methodology)
- [Important caveats](#important-caveats)
- [Contributing](#contributing)
- [Data and automation](#data-and-automation)
- [Related searches](#related-searches)

## Legend

| Badge | Meaning |
|---|---|
| 🟢 Official / first-party | Official OpenAI project or first-party product surface. |
| 🔵 Documented third-party integration | Third-party project with clear public docs for ChatGPT/Codex subscription sign-in. |
| 🟡 Experimental adapter or plugin | Works through a plugin, adapter, bridge, or local-session integration; verify current compatibility. |
| 🟠 Experimental proxy or API shim | Exposes a local API/proxy surface backed by subscription auth; verify terms and security. |
| ⚠️ High-risk / verify terms and security | May involve account pooling, reverse proxies, undocumented endpoints, or other sensitive patterns. |

## Summary

| Category | Projects |
|---|---:|
| Official OpenAI and platform integrations | 5 |
| Editors, IDEs, and coding agents | 11 |
| Remote control and orchestration | 1 |
| Plugins, adapters, and companion CLIs | 9 |
| OpenAI-compatible local APIs and proxies | 6 |

Status mix: 5 🟢 Official / first-party, 11 🔵 Documented third-party integration, 10 🟡 Experimental adapter or plugin, 5 🟠 Experimental proxy or API shim, 1 ⚠️ High-risk / verify terms and security.

## Projects

### Official OpenAI and platform integrations

| Project | What it is | Subscription-auth support | Status |
|---|---|---|---|
| [OpenAI Codex](https://github.com/openai/codex) | OpenAI coding agent available as CLI, IDE integrations, web, desktop, and cloud tasks. | Codex can be used through ChatGPT subscription access on supported ChatGPT plans, or with API-key billing.<br><sub>Auth path: Sign in with ChatGPT, OpenAI API key</sub><br><sub>[evidence 1](https://developers.openai.com/codex/auth) [evidence 2](https://developers.openai.com/codex/cli)</sub> | 🟢 Official / first-party |
| [Codex App Server](https://developers.openai.com/codex/app-server) | Protocol/runtime used by apps to run Codex-backed coding agents with managed authentication, tools, and events. | Provides local agent runtime/app-server primitives that can authenticate through ChatGPT-managed auth modes.<br><sub>Auth path: ChatGPT managed auth, Device-code auth, OpenAI API key</sub><br><sub>[evidence 1](https://developers.openai.com/codex/app-server)</sub> | 🟢 Official / first-party |
| [Codex IDE integrations](https://developers.openai.com/codex/ide) | Official Codex integrations for supported IDEs and editor workflows. | OpenAI documents ChatGPT sign-in for Codex IDE integrations.<br><sub>Auth path: Sign in with ChatGPT, OpenAI API key, JetBrains AI subscription where supported</sub><br><sub>[evidence 1](https://developers.openai.com/codex/ide)</sub> | 🟢 Official / first-party |
| [Codex GitHub integration](https://developers.openai.com/codex/integrations/github) | Official Codex integration for GitHub code review and repository workflows. | Codex can review code and work with GitHub repositories from the Codex product surface.<br><sub>Auth path: ChatGPT/Codex account connection</sub><br><sub>[evidence 1](https://developers.openai.com/codex/integrations/github)</sub> | 🟢 Official / first-party |
| [Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc) | OpenAI plugin that lets Claude Code call Codex for reviews, delegation, and related workflows. | Delegates selected Claude Code work to local Codex, using the user’s existing Codex authentication.<br><sub>Auth path: Local Codex sign-in, ChatGPT subscription, OpenAI API key</sub><br><sub>[evidence 1](https://github.com/openai/codex-plugin-cc)</sub> | 🟢 Official / first-party |

### Editors, IDEs, and coding agents

| Project | What it is | Subscription-auth support | Status |
|---|---|---|---|
| [Xcode coding intelligence](https://developer.apple.com/documentation/Xcode/setting-up-coding-intelligence) | Apple Xcode coding intelligence and agent workflows with Codex support. | Apple documents Codex setup with ChatGPT account sign-in or API key.<br><sub>Auth path: Sign in with a ChatGPT account, OpenAI API key</sub><br><sub>[evidence 1](https://developer.apple.com/documentation/Xcode/setting-up-coding-intelligence)</sub> | 🔵 Documented third-party integration |
| [JetBrains IDEs / AI Assistant Codex](https://www.jetbrains.com/help/ai-assistant/codex-agent.html) | Codex integration for IntelliJ IDEA, PyCharm, WebStorm, and other JetBrains IDEs. | JetBrains documents Codex usage via ChatGPT account, OpenAI API key, or JetBrains AI subscription.<br><sub>Auth path: ChatGPT account, OpenAI API key, JetBrains AI subscription</sub><br><sub>[evidence 1](https://blog.jetbrains.com/ai/2026/01/codex-in-jetbrains-ides/) [evidence 2](https://www.jetbrains.com/help/ai-assistant/codex-agent.html)</sub> | 🔵 Documented third-party integration |
| [Zed](https://zed.dev/blog/chatgpt-subscription-in-zed) | Code editor with built-in agent workflows and ChatGPT subscription/Codex support. | Zed documents signing in with a ChatGPT account and running OpenAI models through Zed’s agent with Codex usage.<br><sub>Auth path: ChatGPT subscription, OpenAI API key</sub><br><sub>[evidence 1](https://zed.dev/docs/ai/external-agents) [evidence 2](https://github.com/zed-industries/codex-acp)</sub> | 🔵 Documented third-party integration |
| [OpenCode](https://opencode.ai/) | Open-source terminal coding agent with multiple model providers and OpenAI subscription login support. | OpenCode documents connecting OpenAI and selecting ChatGPT Plus/Pro.<br><sub>Auth path: OpenAI login, ChatGPT Plus/Pro, OpenAI API key through providers</sub><br><sub>[evidence 1](https://opencode.ai/docs/providers/)</sub> | 🔵 Documented third-party integration |
| [Cline](https://cline.bot/) | VS Code AI coding assistant with OpenAI Codex OAuth support. | Cline documents OpenAI Codex OAuth: sign in with OpenAI, no API key required, with model access depending on plan.<br><sub>Auth path: OpenAI Codex OAuth, ChatGPT Plus/Pro, OpenAI API key through other providers</sub><br><sub>[evidence 1](https://docs.cline.bot/provider-config/openai) [evidence 2](https://cline.bot/blog/introducing-openai-codex-oauth)</sub> | 🔵 Documented third-party integration |
| [Roo Code](https://roocode.com/) | Agentic coding extension with a ChatGPT Plus/Pro provider. | Roo Code documents an OpenAI – ChatGPT Plus/Pro provider using OAuth, without an API key.<br><sub>Auth path: OpenAI - ChatGPT Plus/Pro OAuth</sub><br><sub>[evidence 1](https://docs.roocode.com/providers/openai-chatgpt-plus-pro)</sub> | 🔵 Documented third-party integration |
| [Kilo Code](https://kilo.ai/) | AI coding agent/extension with OpenAI ChatGPT Plus/Pro provider support. | Kilo Code documents using a ChatGPT Plus/Pro subscription with OAuth and no separate API key.<br><sub>Auth path: OpenAI - ChatGPT Plus/Pro OAuth</sub><br><sub>[evidence 1](https://kilo.ai/docs/ai-providers/openai-chatgpt-plus-pro)</sub> | 🔵 Documented third-party integration |
| [Pi](https://github.com/earendil-works/pi) | Composable AI agent/coding-agent toolkit with subscription login providers. | Pi documents ChatGPT Plus/Pro (Codex) as a login provider for its coding agent.<br><sub>Auth path: ChatGPT Plus/Pro (Codex), Other subscription logins</sub><br><sub>[evidence 1](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/providers.md) [evidence 2](https://pi.dev/news)</sub> | 🔵 Documented third-party integration |
| [OpenClaw](https://openclaw.ai/) | Local agentic automation interface that can use Codex-backed OpenAI models through subscription auth. | OpenClaw documents ChatGPT/Codex subscription setup through OpenAI Codex OAuth and the Codex app-server runtime.<br><sub>Auth path: OpenAI/Codex OAuth, ChatGPT subscription, OpenAI API key</sub><br><sub>[evidence 1](https://docs.openclaw.ai/providers/openai) [evidence 2](https://openclaw.ai/blog/openai-models-in-openclaw-done-right/)</sub> | 🔵 Documented third-party integration |
| [Hermes Agent](https://hermes-agent.nousresearch.com/) | Terminal agent runtime with Codex provider and app-server integration. | Hermes documents OpenAI Codex provider support and running agent turns through a ChatGPT subscription with Codex app-server runtime.<br><sub>Auth path: OpenAI Codex provider, ChatGPT OAuth, Device-code auth</sub><br><sub>[evidence 1](https://hermes-agent.nousresearch.com/docs/user-guide/features/codex-app-server-runtime) [evidence 2](https://hermes-agent.nousresearch.com/docs/integrations/providers)</sub> | 🔵 Documented third-party integration |
| [Open CoDesign](https://github.com/OpenCoworkAI/open-codesign) | Open-source AI design/coding workflow project with Codex subscription login mentions in releases. | Project releases describe ChatGPT Plus/Codex subscription login/OAuth support for using an existing subscription as model budget.<br><sub>Auth path: ChatGPT Plus/Codex subscription login, OpenAI API key where supported</sub><br><sub>[evidence 1](https://github.com/OpenCoworkAI/open-codesign/releases)</sub> | 🟡 Experimental adapter or plugin |

### Remote control and orchestration

| Project | What it is | Subscription-auth support | Status |
|---|---|---|---|
| [codex-discord](https://github.com/chadingTV/codex-discord) | Discord-based remote control bridge for Codex sessions. | Project describes remote-controlling Codex through Discord with no API key needed and running on a Codex subscription.<br><sub>Auth path: Codex subscription, Local Codex account/session</sub><br><sub>[evidence 1](https://github.com/chadingTV/codex-discord)</sub> | 🟡 Experimental adapter or plugin |

### Plugins, adapters, and companion CLIs

| Project | What it is | Subscription-auth support | Status |
|---|---|---|---|
| [opencode-openai-codex-auth](https://github.com/numman-ali/opencode-openai-codex-auth) | OpenCode plugin/provider for OpenAI Codex OAuth authentication. | Plugin describes OpenAI Codex access in OpenCode through ChatGPT OAuth instead of API keys.<br><sub>Auth path: OpenAI OAuth, ChatGPT Plus/Pro</sub><br><sub>[evidence 1](https://github.com/numman-ali/opencode-openai-codex-auth)</sub> | 🟡 Experimental adapter or plugin |
| [@openhax/codex for OpenCode](https://github.com/open-hax/codex) | OpenCode plugin that routes OpenCode requests to Codex-backed OpenAI models. | Plugin describes enabling OpenCode to use OpenAI Codex through ChatGPT Plus/Pro OAuth.<br><sub>Auth path: ChatGPT Plus/Pro OAuth</sub><br><sub>[evidence 1](https://github.com/open-hax/codex)</sub> | 🟡 Experimental adapter or plugin |
| [codex-acp](https://github.com/zed-industries/codex-acp) | Agent Client Protocol adapter for running Codex inside Zed and other ACP-compatible clients. | Zed’s Codex ACP adapter documents ChatGPT subscription authentication for local use.<br><sub>Auth path: ChatGPT subscription, Codex API key, OpenAI API key</sub><br><sub>[evidence 1](https://github.com/zed-industries/codex-acp)</sub> | 🔵 Documented third-party integration |
| [llm-openai-via-codex](https://github.com/simonw/llm-openai-via-codex) | Simon Willison’s LLM plugin for accessing OpenAI models through local Codex auth. | LLM plugin that uses an installed/authenticated Codex CLI session to access Codex-available models.<br><sub>Auth path: Local Codex CLI session, ChatGPT OAuth credentials</sub><br><sub>[evidence 1](https://simonwillison.net/2026/Apr/23/llm-openai-via-codex/)</sub> | 🟡 Experimental adapter or plugin |
| [ai-sub-auth](https://github.com/AlexAnys/ai-sub-auth) | Developer library for subscription-auth integrations across AI providers. | Library describes reusing AI subscriptions and includes OpenAI Codex/ChatGPT subscription auth.<br><sub>Auth path: Subscription auth library, OpenAI Codex/ChatGPT subscription</sub><br><sub>[evidence 1](https://github.com/AlexAnys/ai-sub-auth)</sub> | 🟡 Experimental adapter or plugin |
| [pi-codex-search](https://pi.dev/packages/pi-codex-search) | Pi extension that adds Codex-backed web search capabilities. | Pi package page describes reusing a ChatGPT Plus/Pro Codex subscription for web search in Pi agents.<br><sub>Auth path: ChatGPT Plus/Pro Codex subscription via Pi</sub><br><sub>[evidence 1](https://pi.dev/packages/pi-codex-search)</sub> | 🟡 Experimental adapter or plugin |
| [@llblab/pi-codex-usage](https://pi.dev/packages/%40llblab/pi-codex-usage) | Pi utility extension for Codex usage tracking. | Pi package page describes summarizing Codex subscription usage inside Pi workflows.<br><sub>Auth path: Pi Codex subscription login</sub><br><sub>[evidence 1](https://pi.dev/packages/%40llblab/pi-codex-usage)</sub> | 🟡 Experimental adapter or plugin |
| [claude-gpt-image-bridge](https://github.com/oakplank/claude-gpt-image-bridge) | Bridge for image generation workflows from Claude Code through Codex/ChatGPT subscription auth. | Project describes using Codex CLI and a ChatGPT subscription to generate GPT images from Claude Code.<br><sub>Auth path: Codex CLI session, ChatGPT subscription</sub><br><sub>[evidence 1](https://github.com/oakplank/claude-gpt-image-bridge)</sub> | 🟡 Experimental adapter or plugin |
| [chatgpt-imagegen](https://github.com/leeguooooo/chatgpt-imagegen) | Command-line image generation tool that uses ChatGPT/Codex auth paths. | Project describes generating images from the command line using a ChatGPT subscription and no API key.<br><sub>Auth path: ChatGPT subscription, Codex CLI auth</sub><br><sub>[evidence 1](https://github.com/leeguooooo/chatgpt-imagegen)</sub> | 🟡 Experimental adapter or plugin |

### OpenAI-compatible local APIs and proxies

These tools expose local API/proxy surfaces backed by subscription auth. Review terms, token handling, and network exposure before using them.

| Project | What it is | Subscription-auth support | Status |
|---|---|---|---|
| [ChatMock](https://github.com/RayBytes/ChatMock) | Local OpenAI-compatible API server backed by ChatGPT subscription auth. | Project describes signing in with ChatGPT and serving an OpenAI-compatible API locally.<br><sub>Auth path: ChatGPT account login, Local OpenAI-compatible API</sub><br><sub>[evidence 1](https://github.com/RayBytes/ChatMock)</sub><br><sub>Caveat: Proxy/API-shim tools are high-risk: review provider terms, token handling, and whether public serving is allowed.</sub> | 🟠 Experimental proxy or API shim |
| [GPTMock](https://github.com/rapidrabbit76/GPTMock) | OpenAI-compatible local API shim backed by ChatGPT subscription auth. | Fork/variant of ChatMock-style local API approach using ChatGPT subscription login.<br><sub>Auth path: ChatGPT account login, Local OpenAI-compatible API</sub><br><sub>[evidence 1](https://github.com/rapidrabbit76/GPTMock)</sub><br><sub>Caveat: Proxy/API-shim tools are high-risk; verify legality, terms, and security before use.</sub> | 🟠 Experimental proxy or API shim |
| [gptAnywhere](https://github.com/playcations/gptAnywhere) | Tooling for programmatic/local access paths backed by ChatGPT subscription auth. | Project describes programmatic access to OpenAI models through a ChatGPT subscription.<br><sub>Auth path: ChatGPT subscription</sub><br><sub>[evidence 1](https://github.com/playcations/gptAnywhere)</sub><br><sub>Caveat: Experimental proxy-style access path; confirm it does not rely on brittle or disallowed automation, token handling, or provider terms for your use case.</sub> | 🟠 Experimental proxy or API shim |
| [CCProxy API](https://github.com/CaddyGlow/ccproxy-api) | Unified local API proxy for coding-agent subscriptions and providers. | Project describes a local reverse proxy with OpenAI Codex/ChatGPT backend support and OAuth for paid accounts.<br><sub>Auth path: ChatGPT/OpenAI Codex OAuth, Other subscription providers</sub><br><sub>[evidence 1](https://github.com/CaddyGlow/ccproxy-api)</sub><br><sub>Caveat: Good candidate for advanced local use; not a substitute for reviewing provider terms and security.</sub> | 🟠 Experimental proxy or API shim |
| [CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI) | Proxy that exposes local CLI agents/tools as API-like endpoints. | Project describes wrapping CLI tools and using existing OAuth subscription auth for API-style access.<br><sub>Auth path: CLI subscription auth, ChatGPT/Claude/Gemini-style OAuth providers</sub><br><sub>[evidence 1](https://github.com/router-for-me/CLIProxyAPI)</sub><br><sub>Caveat: General-purpose CLI proxy; verify current OpenAI/Codex support before listing as fully supported.</sub> | 🟠 Experimental proxy or API shim |
| [Codex-LB](https://github.com/Soju06/codex-lb) | Load-balancer/proxy layer for multiple ChatGPT/Codex accounts. | Project describes a load balancer/proxy for ChatGPT accounts.<br><sub>Auth path: ChatGPT account pool, Local OpenAI-compatible proxy</sub><br><sub>[evidence 1](https://github.com/Soju06/codex-lb)</sub><br><sub>Caveat: Listed for visibility only. Account pooling, shared credentials, resale, or quota-bypass use may violate provider terms. Do not use for abuse or public resale.</sub> | ⚠️ High-risk / verify terms and security |

## Methodology

Listings are added only from durable public evidence, not search snippets, social posts without supporting docs, or private claims. Each project has a `last_verified` date in `data/projects.json`; validation fails when a listing becomes too stale to treat as current.

Statuses are intentionally conservative. A project that exposes a local API, proxy, reverse proxy, or account-pooling surface is kept separate from normal editor and agent integrations even if it works technically.

High-risk entries are listed for visibility and triage, not endorsement. Prefer OAuth, device-code flows, or local Codex-managed auth over copied cookies or raw session tokens.

## Important caveats

A ChatGPT subscription is not the same thing as an OpenAI Platform API key. Some tools expose only Codex-style coding models or app-server capabilities. API-only features such as embeddings, speech, realtime APIs, fine-tuning, or production API usage may still require platform billing.

Plan support varies. Some official Codex surfaces work across multiple ChatGPT plans, while many third-party integrations specifically document Plus/Pro. Always check the linked evidence before assuming your plan is supported.

Security matters. Any project that asks for OAuth tokens, stores local credentials, exposes a local proxy, or controls your editor/terminal should be reviewed before use.

## Contributing

Contributions are welcome. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a PR.

When adding a project, include:

- Project name and URL.
- Category and status.
- Exact authentication method.
- Link proving ChatGPT subscription, Codex OAuth, Codex app-server auth, or local Codex sign-in support.
- Security or terms caveats, especially for proxies, adapters, undocumented auth flows, or credential-sensitive designs.

## Data and automation

The source list lives in [`data/projects.json`](data/projects.json), and [`data/catalog.json`](data/catalog.json) is generated for downstream tooling. The schema lives in [`data/schema.json`](data/schema.json).

Current project count: 32. Data verified through: 2026-06-02.

Useful maintenance commands:

```bash
make generate
make validate
make links

python3 scripts/generate_outputs.py
python3 scripts/generate_outputs.py --check
python3 scripts/validate_data.py
python3 scripts/check_links.py
```

## Related searches

Useful GitHub/search queries for finding candidates:

```text
"ChatGPT Plus/Pro" "Codex" "OAuth"
"ChatGPT subscription" "Codex app server"
"Sign in with ChatGPT" "coding agent"
"OpenAI Codex OAuth" "VS Code"
"use your ChatGPT subscription" "OpenCode"
"local Codex sign-in" "ChatGPT subscription"
```

## Disclaimer

This repository is community-maintained and is not affiliated with OpenAI. Listings are for discovery, not endorsement. Use tools only within the terms of the providers and projects involved.
