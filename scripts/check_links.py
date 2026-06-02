#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ssl
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

from project_data import EVIDENCE_TERMS, load_projects

USER_AGENT = (
    "awesome-chatgpt-codex-auth link checker"
)
MAX_READ_BYTES = 512_000
BLOCKED_STATUSES = {401, 403, 429}


def ssl_context() -> ssl.SSLContext:
    try:
        import certifi  # type: ignore[import-not-found]

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:  # noqa: BLE001
        return ssl.create_default_context()


@dataclass(frozen=True)
class Target:
    url: str
    labels: tuple[str, ...]
    is_evidence: bool


@dataclass
class Result:
    target: Target
    ok: bool
    status: int | None
    blocked: bool
    message: str
    body: str = ""


def collect_targets(projects: list[dict[str, Any]]) -> list[Target]:
    labels_by_url: dict[str, list[str]] = {}
    evidence_by_url: dict[str, bool] = {}

    for project in projects:
        labels_by_url.setdefault(project["url"], []).append(f"{project['name']} project")
        evidence_by_url[project["url"]] = evidence_by_url.get(project["url"], False)
        for doc in project["docs"]:
            labels_by_url.setdefault(doc, []).append(f"{project['name']} evidence")
            evidence_by_url[doc] = True

    return [
        Target(url=url, labels=tuple(labels), is_evidence=evidence_by_url[url])
        for url, labels in sorted(labels_by_url.items())
    ]


def request_url(url: str, method: str, timeout: float, context: ssl.SSLContext) -> tuple[int, str]:
    request = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
        status = response.getcode()
        if method == "HEAD":
            return status, ""
        body = response.read(MAX_READ_BYTES).decode("utf-8", errors="ignore")
        return status, body


def apple_documentation_data_url(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.netloc != "developer.apple.com":
        return None

    parts = parsed.path.strip("/").split("/")
    if len(parts) < 2 or parts[0].lower() != "documentation":
        return None

    data_path = "/".join(parts[1:])
    if not data_path or data_path.endswith(".json"):
        return None
    return f"https://developer.apple.com/tutorials/data/documentation/{data_path}.json"


def enrich_evidence_body(url: str, body: str, timeout: float, context: ssl.SSLContext) -> str:
    if any(term in body.casefold() for term in EVIDENCE_TERMS):
        return body

    data_url = apple_documentation_data_url(url)
    if not data_url:
        return body

    try:
        _, data_body = request_url(data_url, "GET", timeout, context)
    except Exception:  # noqa: BLE001 - normal link reachability already passed.
        return body
    return f"{body}\n{data_body}" if body else data_body


def check_target(target: Target, timeout: float, allow_blocked: bool, context: ssl.SSLContext) -> Result:
    status = None
    body = ""
    try:
        status, _ = request_url(target.url, "HEAD", timeout, context)
        if 200 <= status < 400:
            try:
                _, body = request_url(target.url, "GET", timeout, context)
            except Exception:  # noqa: BLE001 - reachability already passed.
                body = ""
            if target.is_evidence:
                body = enrich_evidence_body(target.url, body, timeout, context)
            return Result(target, True, status, False, "ok", body)
    except urllib.error.HTTPError as exc:
        status = exc.code
    except Exception as exc:  # noqa: BLE001
        try:
            status, body = request_url(target.url, "GET", timeout, context)
            if 200 <= status < 400:
                if target.is_evidence:
                    body = enrich_evidence_body(target.url, body, timeout, context)
                return Result(target, True, status, False, "ok", body)
        except urllib.error.HTTPError as get_exc:
            status = get_exc.code
        except Exception as get_exc:  # noqa: BLE001
            return Result(target, False, None, False, f"{type(exc).__name__}: {exc}; GET: {type(get_exc).__name__}: {get_exc}")

    if status in BLOCKED_STATUSES and allow_blocked:
        return Result(target, True, status, True, "blocked by remote site")
    if status is not None:
        return Result(target, False, status, False, f"HTTP {status}")
    return Result(target, False, None, False, "unreachable")


def evidence_warnings(results: list[Result]) -> list[str]:
    warnings: list[str] = []
    for result in results:
        if not result.target.is_evidence:
            continue
        if result.blocked:
            warnings.append(f"{result.target.url}: evidence content could not be inspected ({result.message})")
            continue
        if not result.body:
            warnings.append(f"{result.target.url}: evidence content was reachable but not inspectable")
            continue
        body = result.body.casefold()
        if not any(term in body for term in EVIDENCE_TERMS):
            warnings.append(f"{result.target.url}: fetched evidence did not contain expected auth terms")
    return warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check project and evidence links.")
    parser.add_argument("--timeout", type=float, default=15.0, help="Per-request timeout in seconds.")
    parser.add_argument("--workers", type=int, default=8, help="Number of concurrent checks.")
    parser.add_argument(
        "--strict-blocked",
        action="store_true",
        help="Fail on 401/403/429 responses instead of treating them as anti-bot blocks.",
    )
    parser.add_argument(
        "--verify-evidence",
        action="store_true",
        help="Warn when fetched evidence pages do not contain expected ChatGPT/Codex auth terms.",
    )
    parser.add_argument(
        "--strict-evidence",
        action="store_true",
        help="Turn --verify-evidence warnings into failures.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    targets = collect_targets(load_projects())
    allow_blocked = not args.strict_blocked
    context = ssl_context()

    results: list[Result] = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [
            executor.submit(check_target, target, args.timeout, allow_blocked, context)
            for target in targets
        ]
        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda result: result.target.url)
    failures = [result for result in results if not result.ok]
    blocked = [result for result in results if result.blocked]

    for result in failures:
        labels = ", ".join(result.target.labels)
        print(f"ERROR: {result.target.url} ({labels}) - {result.message}", file=sys.stderr)

    evidence_notes: list[str] = []
    if args.verify_evidence or args.strict_evidence:
        evidence_notes = evidence_warnings(results)
        for note in evidence_notes:
            stream = sys.stderr if args.strict_evidence else sys.stdout
            print(f"WARNING: {note}", file=stream)

    checked = len(results)
    print(f"Checked {checked} unique URLs.")
    if blocked:
        print(f"Remote blocking tolerated for {len(blocked)} URL(s). Use --strict-blocked to fail on those.")

    if failures or (args.strict_evidence and evidence_notes):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
