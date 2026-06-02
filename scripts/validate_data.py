#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from typing import Any
from urllib.parse import urlparse

from project_data import (
    BANNED_LISTING_PHRASES,
    CATEGORY_ORDER,
    DATA_FILE,
    EVIDENCE_TERMS,
    RISK_TERMS,
    STATUS_ALLOWED_CATEGORIES,
    load_projects,
    load_schema,
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def label_for(project: Any, index: int) -> str:
    if isinstance(project, dict) and isinstance(project.get("name"), str) and project["name"].strip():
        return project["name"]
    return f"item #{index}"


def check_type(label: str, field: str, value: Any, expected_type: str) -> None:
    if expected_type == "string":
        if not isinstance(value, str):
            fail(f"{label}: {field} must be a string")
        return
    if expected_type == "array":
        if not isinstance(value, list):
            fail(f"{label}: {field} must be an array")
        return
    if expected_type == "object":
        if not isinstance(value, dict):
            fail(f"{label}: {field} must be an object")
        return
    fail(f"{label}: unsupported schema type {expected_type!r} for {field}")


def validate_string_rules(label: str, field: str, value: str, rules: dict[str, Any]) -> None:
    if rules.get("minLength", 0) and len(value.strip()) < rules["minLength"]:
        fail(f"{label}: {field} must be a non-empty string")
    if "pattern" in rules and not re.match(rules["pattern"], value):
        fail(f"{label}: {field} does not match pattern {rules['pattern']!r}")
    if "enum" in rules and value not in rules["enum"]:
        fail(f"{label}: invalid {field} {value!r}")
    if rules.get("format") == "uri" and not is_url(value):
        fail(f"{label}: {field} must be an http(s) URL")


def validate_array_rules(label: str, field: str, value: list[Any], rules: dict[str, Any]) -> None:
    if len(value) < rules.get("minItems", 0):
        fail(f"{label}: {field} must contain at least {rules['minItems']} item(s)")
    if rules.get("uniqueItems") and len(value) != len(set(map(repr, value))):
        fail(f"{label}: {field} must not contain duplicates")

    item_rules = rules.get("items", {})
    item_type = item_rules.get("type")
    for index, item in enumerate(value):
        item_field = f"{field}[{index}]"
        if item_type:
            check_type(label, item_field, item, item_type)
        if item_type == "string":
            validate_string_rules(label, item_field, item, item_rules)


def validate_against_schema(projects: list[dict[str, Any]], schema: dict[str, Any]) -> None:
    if schema.get("type") != "array":
        fail("data/schema.json must describe an array")
    if not isinstance(projects, list):
        fail("data/projects.json must be a JSON array")

    item_schema = schema.get("items")
    if not isinstance(item_schema, dict):
        fail("data/schema.json must define an items schema")

    required = set(item_schema.get("required", []))
    properties = item_schema.get("properties", {})
    if not isinstance(properties, dict):
        fail("data/schema.json item properties must be an object")

    additional_allowed = item_schema.get("additionalProperties", True)

    for index, project in enumerate(projects):
        label = label_for(project, index)
        if not isinstance(project, dict):
            fail(f"{label}: project must be an object")

        missing = required - set(project)
        extra = set(project) - set(properties)
        if missing:
            fail(f"{label}: missing fields: {sorted(missing)}")
        if extra and not additional_allowed:
            fail(f"{label}: unexpected fields: {sorted(extra)}")

        for field, rules in properties.items():
            if field not in project:
                continue
            expected_type = rules.get("type")
            if expected_type:
                check_type(label, field, project[field], expected_type)
            if expected_type == "string":
                validate_string_rules(label, field, project[field], rules)
            elif expected_type == "array":
                validate_array_rules(label, field, project[field], rules)


def validate_semantics(projects: list[dict[str, Any]], max_verification_age_days: int) -> None:
    seen_names: set[str] = set()
    seen_slugs: set[str] = set()
    seen_urls: set[str] = set()
    last_category_index = -1
    today = date.today()

    for index, project in enumerate(projects):
        label = label_for(project, index)
        name = project["name"].strip()
        slug = project["slug"]
        category = project["category"]
        status = project["status"]

        normalized_name = name.casefold()
        if normalized_name in seen_names:
            fail(f"{label}: duplicate name")
        seen_names.add(normalized_name)

        if slug in seen_slugs:
            fail(f"{label}: duplicate slug {slug!r}")
        seen_slugs.add(slug)

        if project["url"] in seen_urls:
            fail(f"{label}: duplicate project URL {project['url']!r}")
        seen_urls.add(project["url"])

        category_index = CATEGORY_ORDER.index(category)
        if category_index < last_category_index:
            fail(f"{label}: category {category!r} is out of display order")
        last_category_index = category_index

        allowed_categories = STATUS_ALLOWED_CATEGORIES.get(status, set())
        if category not in allowed_categories:
            fail(f"{label}: status {status!r} is not valid for category {category!r}")

        listing_text = " ".join(
            [
                project["name"],
                project["description"],
                project["subscription_auth_support"],
                project["notes"],
                " ".join(project["auth"]),
            ]
        ).casefold()

        if not any(term in listing_text for term in EVIDENCE_TERMS):
            fail(f"{label}: listing text must mention a ChatGPT/Codex auth evidence term")

        banned = [phrase for phrase in BANNED_LISTING_PHRASES if phrase in listing_text]
        if banned:
            fail(f"{label}: avoid misleading phrase(s): {banned}")

        if status in {"experimental-proxy", "high-risk"}:
            if not any(term in listing_text for term in RISK_TERMS):
                fail(f"{label}: proxy/high-risk listings must include explicit risk caveats")

        try:
            verified = datetime.strptime(project["last_verified"], "%Y-%m-%d").date()
        except ValueError:
            fail(f"{label}: last_verified must be a real YYYY-MM-DD date")

        if verified > today:
            fail(f"{label}: last_verified {verified} is in the future")

        age_days = (today - verified).days
        if age_days > max_verification_age_days:
            fail(
                f"{label}: last_verified is {age_days} days old; "
                f"refresh evidence or raise --max-verification-age-days"
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=f"Validate {DATA_FILE.relative_to(DATA_FILE.parents[1])}.")
    parser.add_argument(
        "--max-verification-age-days",
        type=int,
        default=365,
        help="Fail if any listing verification date is older than this many days.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    projects = load_projects()
    schema = load_schema()
    validate_against_schema(projects, schema)
    validate_semantics(projects, args.max_verification_age_days)
    print(f"Validated {len(projects)} projects.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
