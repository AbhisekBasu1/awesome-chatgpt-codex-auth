#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "projects.json"
SCHEMA_FILE = ROOT / "data" / "schema.json"
CATALOG_FILE = ROOT / "data" / "catalog.json"
README_FILE = ROOT / "README.md"

REPO_SLUG = "awesome-chatgpt-codex-auth"
DISPLAY_TITLE = "Awesome ChatGPT/Codex Auth"
DESCRIPTION = (
    "A curated index of developer tools that authenticate through ChatGPT, "
    "Codex OAuth, Codex app-server auth, or a local Codex sign-in instead of "
    "requiring a separate OpenAI Platform API key."
)

CATEGORY_ORDER = [
    "official-platform",
    "editors-agents",
    "remote-control",
    "plugins-adapters",
    "proxies-api-shims",
]

CATEGORY_LABELS = {
    "official-platform": "Official OpenAI and platform integrations",
    "editors-agents": "Editors, IDEs, and coding agents",
    "remote-control": "Remote control and orchestration",
    "plugins-adapters": "Plugins, adapters, and companion CLIs",
    "proxies-api-shims": "OpenAI-compatible local APIs and proxies",
}

CATEGORY_NOTES = {
    "proxies-api-shims": (
        "These tools expose local API/proxy surfaces backed by subscription auth. "
        "Review terms, token handling, and network exposure before using them."
    ),
}

STATUS_ORDER = [
    "official",
    "documented-third-party",
    "experimental-adapter",
    "experimental-proxy",
    "high-risk",
]

STATUS_LABELS = {
    "official": "\U0001f7e2 Official / first-party",
    "documented-third-party": "\U0001f535 Documented third-party integration",
    "experimental-adapter": "\U0001f7e1 Experimental adapter or plugin",
    "experimental-proxy": "\U0001f7e0 Experimental proxy or API shim",
    "high-risk": "\u26a0\ufe0f High-risk / verify terms and security",
}

STATUS_DESCRIPTIONS = {
    "official": "Official OpenAI project or first-party product surface.",
    "documented-third-party": (
        "Third-party project with clear public docs for ChatGPT/Codex subscription sign-in."
    ),
    "experimental-adapter": (
        "Works through a plugin, adapter, bridge, or local-session integration; verify current compatibility."
    ),
    "experimental-proxy": (
        "Exposes a local API/proxy surface backed by subscription auth; verify terms and security."
    ),
    "high-risk": (
        "May involve account pooling, reverse proxies, undocumented endpoints, or other sensitive patterns."
    ),
}

STATUS_ALLOWED_CATEGORIES = {
    "official": {"official-platform"},
    "documented-third-party": {"editors-agents", "plugins-adapters"},
    "experimental-adapter": {"editors-agents", "remote-control", "plugins-adapters"},
    "experimental-proxy": {"proxies-api-shims"},
    "high-risk": {"proxies-api-shims"},
}

EVIDENCE_TERMS = {
    "chatgpt",
    "codex",
    "openai codex",
    "oauth",
    "subscription",
    "sign in",
    "login",
    "local codex",
    "app-server",
    "managed auth",
    "device-code",
}

RISK_TERMS = {
    "proxy",
    "shim",
    "reverse proxy",
    "account",
    "pool",
    "token",
    "credential",
    "endpoint",
    "terms",
}

BANNED_LISTING_PHRASES = {
    "free api access",
    "unlimited chatgpt api",
    "bypasses api billing",
    "bypass api billing",
    "cheap plus",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def load_projects() -> list[dict[str, Any]]:
    projects = load_json(DATA_FILE)
    if not isinstance(projects, list):
        raise TypeError("data/projects.json must contain a JSON array")
    return projects


def load_schema() -> dict[str, Any]:
    schema = load_json(SCHEMA_FILE)
    if not isinstance(schema, dict):
        raise TypeError("data/schema.json must contain a JSON object")
    return schema


def ordered_counts(values: list[str], order: list[str]) -> list[dict[str, Any]]:
    counts = Counter(values)
    return [{"id": item, "count": counts.get(item, 0)} for item in order if counts.get(item, 0)]


def project_metadata(projects: list[dict[str, Any]]) -> dict[str, Any]:
    dates = [project["last_verified"] for project in projects]
    categories = Counter(project["category"] for project in projects)
    statuses = Counter(project["status"] for project in projects)

    return {
        "repository": REPO_SLUG,
        "title": DISPLAY_TITLE,
        "description": DESCRIPTION,
        "generated_from": "data/projects.json",
        "project_count": len(projects),
        "last_verified": {
            "earliest": min(dates) if dates else None,
            "latest": max(dates) if dates else None,
        },
        "categories": [
            {
                "id": category,
                "label": CATEGORY_LABELS[category],
                "count": categories.get(category, 0),
            }
            for category in CATEGORY_ORDER
            if categories.get(category, 0)
        ],
        "statuses": [
            {
                "id": status,
                "label": STATUS_LABELS[status],
                "count": statuses.get(status, 0),
            }
            for status in STATUS_ORDER
            if statuses.get(status, 0)
        ],
    }


def catalog(projects: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "metadata": project_metadata(projects),
        "projects": projects,
    }
