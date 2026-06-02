#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from project_data import (
    CATALOG_FILE,
    CATEGORY_LABELS,
    CATEGORY_NOTES,
    CATEGORY_ORDER,
    DESCRIPTION,
    DISPLAY_TITLE,
    README_FILE,
    REPO_SLUG,
    ROOT,
    STATUS_DESCRIPTIONS,
    STATUS_LABELS,
    STATUS_ORDER,
    catalog,
    load_projects,
    project_metadata,
)


def markdown_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ").strip()


def docs_links(project: dict[str, Any]) -> str:
    links = []
    for index, doc in enumerate(project["docs"], start=1):
        links.append(f"[evidence {index}]({doc})")
    return " ".join(links)


def status_table() -> list[str]:
    lines = [
        "| Badge | Meaning |",
        "|---|---|",
    ]
    for status in STATUS_ORDER:
        lines.append(f"| {STATUS_LABELS[status]} | {STATUS_DESCRIPTIONS[status]} |")
    return lines


def summary_table(metadata: dict[str, Any]) -> list[str]:
    lines = [
        "| Category | Projects |",
        "|---|---:|",
    ]
    for category in metadata["categories"]:
        lines.append(f"| {category['label']} | {category['count']} |")
    return lines


def status_summary(metadata: dict[str, Any]) -> str:
    return ", ".join(f"{status['count']} {status['label']}" for status in metadata["statuses"])


def render_project_row(project: dict[str, Any]) -> str:
    support_parts = [
        markdown_escape(project["subscription_auth_support"]),
        f"<br><sub>Auth path: {markdown_escape(', '.join(project['auth']))}</sub>",
        f"<br><sub>{docs_links(project)}</sub>",
    ]

    if project["status"] in {"experimental-proxy", "high-risk"}:
        support_parts.append(f"<br><sub>Caveat: {markdown_escape(project['notes'])}</sub>")

    cells = [
        f"[{markdown_escape(project['name'])}]({project['url']})",
        markdown_escape(project["description"]),
        "".join(support_parts),
        STATUS_LABELS[project["status"]],
    ]
    return "| " + " | ".join(cells) + " |"


def project_tables(projects: list[dict[str, Any]]) -> list[str]:
    by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for project in projects:
        by_category[project["category"]].append(project)

    lines: list[str] = []
    for category in CATEGORY_ORDER:
        category_projects = by_category.get(category)
        if not category_projects:
            continue

        lines.extend(["", f"### {CATEGORY_LABELS[category]}", ""])
        if category in CATEGORY_NOTES:
            lines.extend([CATEGORY_NOTES[category], ""])
        lines.extend(
            [
                "| Project | What it is | Subscription-auth support | Status |",
                "|---|---|---|---|",
            ]
        )
        lines.extend(render_project_row(project) for project in category_projects)
    return lines


def render_readme(projects: list[dict[str, Any]]) -> str:
    metadata = project_metadata(projects)
    latest_verified = metadata["last_verified"]["latest"] or "n/a"

    lines = [
        f"# {DISPLAY_TITLE} [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)",
        "",
        f"> {DESCRIPTION}",
        "",
        f"**Repository slug:** `{REPO_SLUG}`",
        f"**Projects:** {metadata['project_count']}",
        f"**Data verified through:** {latest_verified}",
        "",
        "_Generated from [`data/projects.json`](data/projects.json). Edit the data file, then run `python3 scripts/generate_outputs.py`._",
        "",
        "## Contents",
        "",
        "- [What counts](#what-counts)",
        "- [Legend](#legend)",
        "- [Summary](#summary)",
        "- [Projects](#projects)",
        "- [Methodology](#methodology)",
        "- [Important caveats](#important-caveats)",
        "- [Contributing](#contributing)",
        "- [Data and automation](#data-and-automation)",
        "- [Related searches](#related-searches)",
        "",
        "## What counts",
        "",
        "Included projects should meet all of these requirements:",
        "",
        "1. The project publicly documents a way to authenticate with a ChatGPT account, ChatGPT subscription, Codex OAuth, Codex app-server managed auth, or a local Codex sign-in.",
        "2. The project does not require a separate OpenAI Platform API key for its primary listed ChatGPT/Codex subscription-auth flow.",
        "3. The project is an app, editor integration, coding agent, plugin, local service, SDK, or adapter that a developer can actually install or use.",
        "4. The listing includes durable evidence: official docs, a README, release notes, or another public source that can be reviewed later.",
        "",
        "Not included:",
        "",
        "- Generic OpenAI API clients that only support `OPENAI_API_KEY`.",
        "- Account resellers, shared-account marketplaces, cheap Plus sellers, credential rentals, or quota-bypass services.",
        "- Tools that require users to paste browser cookies/session tokens without a clearly documented security model.",
        "- Scrapers or automation whose main purpose is bypassing product limits, access controls, or provider terms.",
        "",
        "## Legend",
        "",
        *status_table(),
        "",
        "## Summary",
        "",
        *summary_table(metadata),
        "",
        f"Status mix: {status_summary(metadata)}.",
        "",
        "## Projects",
        *project_tables(projects),
        "",
        "## Methodology",
        "",
        "Listings are added only from durable public evidence, not search snippets, social posts without supporting docs, or private claims. Each project has a `last_verified` date in `data/projects.json`; validation fails when a listing becomes too stale to treat as current.",
        "",
        "Statuses are intentionally conservative. A project that exposes a local API, proxy, reverse proxy, or account-pooling surface is kept separate from normal editor and agent integrations even if it works technically.",
        "",
        "High-risk entries are listed for visibility and triage, not endorsement. Prefer OAuth, device-code flows, or local Codex-managed auth over copied cookies or raw session tokens.",
        "",
        "## Important caveats",
        "",
        "A ChatGPT subscription is not the same thing as an OpenAI Platform API key. Some tools expose only Codex-style coding models or app-server capabilities. API-only features such as embeddings, speech, realtime APIs, fine-tuning, or production API usage may still require platform billing.",
        "",
        "Plan support varies. Some official Codex surfaces work across multiple ChatGPT plans, while many third-party integrations specifically document Plus/Pro. Always check the linked evidence before assuming your plan is supported.",
        "",
        "Security matters. Any project that asks for OAuth tokens, stores local credentials, exposes a local proxy, or controls your editor/terminal should be reviewed before use.",
        "",
        "## Contributing",
        "",
        "Contributions are welcome. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a PR.",
        "",
        "When adding a project, include:",
        "",
        "- Project name and URL.",
        "- Category and status.",
        "- Exact authentication method.",
        "- Link proving ChatGPT subscription, Codex OAuth, Codex app-server auth, or local Codex sign-in support.",
        "- Security or terms caveats, especially for proxies, adapters, undocumented auth flows, or credential-sensitive designs.",
        "",
        "## Data and automation",
        "",
        "The source list lives in [`data/projects.json`](data/projects.json), and [`data/catalog.json`](data/catalog.json) is generated for downstream tooling. The schema lives in [`data/schema.json`](data/schema.json).",
        "",
        "Useful maintenance commands:",
        "",
        "```bash",
        "make generate",
        "make validate",
        "make links",
        "",
        "python3 scripts/generate_outputs.py",
        "python3 scripts/generate_outputs.py --check",
        "python3 scripts/validate_data.py",
        "python3 scripts/check_links.py",
        "```",
        "",
        "## Related searches",
        "",
        "Useful GitHub/search queries for finding candidates:",
        "",
        "```text",
        '"ChatGPT Plus/Pro" "Codex" "OAuth"',
        '"ChatGPT subscription" "Codex app server"',
        '"Sign in with ChatGPT" "coding agent"',
        '"OpenAI Codex OAuth" "VS Code"',
        '"use your ChatGPT subscription" "OpenCode"',
        '"local Codex sign-in" "ChatGPT subscription"',
        "```",
        "",
        "## Disclaimer",
        "",
        "This repository is community-maintained and is not affiliated with OpenAI. Listings are for discovery, not endorsement. Use tools only within the terms of the providers and projects involved.",
        "",
    ]
    return "\n".join(lines)


def write_outputs(projects: list[dict[str, Any]]) -> None:
    README_FILE.write_text(render_readme(projects))
    CATALOG_FILE.write_text(json.dumps(catalog(projects), indent=2, ensure_ascii=False) + "\n")


def check_file(path: Path, expected: str) -> bool:
    actual = path.read_text() if path.exists() else ""
    if actual == expected:
        return True
    print(f"ERROR: {path.relative_to(ROOT)} is out of date.", file=sys.stderr)
    return False


def check_outputs(projects: list[dict[str, Any]]) -> int:
    expected_readme = render_readme(projects)
    expected_catalog = json.dumps(catalog(projects), indent=2, ensure_ascii=False) + "\n"
    ok = True
    ok = check_file(README_FILE, expected_readme) and ok
    ok = check_file(CATALOG_FILE, expected_catalog) and ok
    if ok:
        print("Generated outputs are current.")
        return 0
    print("Run `python3 scripts/generate_outputs.py` to refresh generated files.", file=sys.stderr)
    return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate README and catalog outputs.")
    parser.add_argument("--check", action="store_true", help="Fail if generated outputs are stale.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    projects = load_projects()
    if args.check:
        return check_outputs(projects)
    write_outputs(projects)
    print(f"Generated {README_FILE.relative_to(ROOT)} and {CATALOG_FILE.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
