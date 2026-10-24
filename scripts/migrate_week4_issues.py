"""Preview the one-time W4 issue conversion; apply only after specs reach main.

Run from the repository root. Preview and backups are written outside the repo
when --output-dir points there. No issue is closed and no comment is posted.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen


REPO = "team-ok-ITPD/team-OK-itpd"
BASE = f"https://github.com/{REPO}/blob/main/docs/"
RETIRED = {"user-story", "task", "moscow:must", "moscow:should", "moscow:could", "moscow:wont"}
STORIES = {
    28: ([1], [1]), 29: ([2], [1, 3]), 30: ([3], [1, 2]),
    31: ([4], [1, 2]), 32: ([5], [1, 3]), 33: ([6], [1]), 34: ([7], [1]),
}


def credentials():
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return "Bearer " + token
    result = subprocess.run(
        ["git", "-c", "credential.interactive=false", "credential", "fill"],
        input="protocol=https\nhost=github.com\n\n", text=True,
        capture_output=True, check=True,
    )
    values = dict(line.split("=", 1) for line in result.stdout.splitlines() if "=" in line)
    if "password" not in values:
        raise RuntimeError("No GitHub credentials; set GH_TOKEN or use Git credential manager")
    value = (values.get("username", "") + ":" + values["password"]).encode()
    return "Basic " + base64.b64encode(value).decode()


def api(path, auth, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    request = Request(
        "https://api.github.com/" + path, data=data, method=method,
        headers={"Authorization": auth, "User-Agent": "debug-gym-w4-conversion", "Content-Type": "application/json"},
    )
    with urlopen(request, timeout=30) as response:
        body = response.read()
        return json.loads(body) if body else None


def section(body, heading):
    match = re.search(r"(?ms)^### " + re.escape(heading) + r"\s*\n(.*?)(?=^### |\Z)", body)
    return match.group(1).strip() if match else ""


def put_section(body, heading, text):
    pattern = r"(?ms)^### " + re.escape(heading) + r"\s*\n.*?(?=^### |\Z)"
    replacement = f"### {heading}\n\n{text.strip()}\n\n"
    return re.sub(pattern, lambda _: replacement, body, count=1) if re.search(pattern, body) else body.rstrip() + "\n\n" + replacement


def criteria(body):
    original = section(body, "Acceptance criteria")
    if not original:
        return body
    updated = re.sub(r"(?m)^\s*\d+\.\s+(AC-\d+:)", r"- [ ] \1", original)
    updated = re.sub(r"(?m)^\s*-\s*\[\s*\]\s*(AC-\d+:)", r"- [ ] \1", updated)
    return put_section(body, "Acceptance criteria", updated) if updated != original else body


def links(frs, adrs):
    return "\n".join(
        [f"- [FR-{n:03}]({BASE}functional-requirements/fr/FR-{n:03}.md)" for n in sorted(set(frs))]
        + [f"- [ADR-{n:03}]({BASE}architecture/adr/ADR-{n:03}.md)" for n in sorted(set(adrs))]
    )


def planned_change(issue):
    body = issue.get("body") or ""
    old_labels = [label["name"] for label in issue.get("labels", [])]
    kind = (issue.get("type") or {}).get("name")
    number = issue["number"]
    is_story = kind == "User Story" or "user-story" in old_labels or re.match(r"US-\d+:", issue["title"])
    is_task = kind == "Task" or "task" in old_labels
    if not is_story and not is_task:
        if RETIRED.intersection(old_labels):
            raise RuntimeError(f"Issue #{number} has retired labels but no reviewed issue type")
        return None
    payload = {"type": "User Story" if is_story else "Task"}
    if is_story:
        if number not in STORIES:
            raise RuntimeError(f"Story #{number} needs a reviewed specification mapping")
        fields = {v["issue_field_name"]: (v.get("single_select_option") or {}).get("name") for v in issue.get("issue_field_values", [])}
        if not fields.get("MoSCoW"):
            raise RuntimeError(f"Story #{number} has no MoSCoW value; set its real priority first")
        body = criteria(body)
        if fields["MoSCoW"] != "Won't Have":
            body = put_section(body, "Specified by", links(*STORIES[number]))
    elif issue["state"] == "open":
        body = criteria(body)
        if number in (77, 81):
            requirements = links(range(1, 8), range(1, 4))
        elif number in (74, 75):
            requirements = links(range(1, 8), range(1, 4) if number == 75 else [])
        else:
            related = [int(n) for n in re.findall(r"#(\d+)", section(body, "Story")) if int(n) in STORIES]
            frs = [f for n in related for f in STORIES[n][0]]
            adrs = [a for n in related for a in STORIES[n][1]]
            requirements = links(frs, adrs) if related else "None: repository upkeep."
        body = put_section(body, "Requirements", requirements)
    if body != (issue.get("body") or ""):
        payload["body"] = body
    remaining = [name for name in old_labels if name not in RETIRED]
    if remaining != old_labels:
        payload["labels"] = remaining
    if issue.get("milestone") and issue["state"] == "open":
        fields = {v["issue_field_name"]: (v.get("single_select_option") or {}).get("name") for v in issue.get("issue_field_values", [])}
        owners = [fields.get("Responsible"), fields.get("Accountable")]
        if all(owners) and len(set(owners)) == 2:
            if set(owners) != {a["login"] for a in issue.get("assignees", [])}:
                payload["assignees"] = owners
    if kind == payload["type"]:
        del payload["type"]
    return payload or None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--apply", action="store_true", help="Apply the reviewed conversion after specs exist on main")
    args = parser.parse_args()
    auth = credentials()
    issues = []
    page = 1
    while True:
        batch = api(f"repos/{REPO}/issues?state=all&per_page=100&page={page}", auth)
        issues.extend(i for i in batch if "pull_request" not in i)
        if len(batch) < 100:
            break
        page += 1
    changes = [{"number": i["number"], "before": i, "patch": patch} for i in issues if (patch := planned_change(i))]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    snapshot = args.output_dir / "issue-conversion.json"
    if snapshot.exists():
        raise RuntimeError("Choose a new output directory; existing review/backups are never overwritten")
    snapshot.write_text(json.dumps(changes, indent=2), encoding="utf-8")
    print(f"Prepared {len(changes)} issue changes in {snapshot}")
    if not args.apply:
        print("Preview only. No issues, labels, milestones or verification states were changed.")
        return
    # Full preflight before the first remote mutation.
    for kind, total, folder in (("FR", 7, "functional-requirements/fr"), ("ADR", 3, "architecture/adr")):
        for n in range(1, total + 1):
            path = f"docs/{folder}/{kind}-{n:03}.md"
            try:
                api(f"repos/{REPO}/contents/{path}?ref=main", auth)
            except HTTPError as error:
                raise RuntimeError(f"Specification {path} is not available on main; no issues were changed") from error
    # Check every issue for concurrent edits before making any change.
    for item in changes:
        current = api(f"repos/{REPO}/issues/{item['number']}", auth)
        if current["updated_at"] != item["before"]["updated_at"]:
            raise RuntimeError(f"Issue #{item['number']} changed during review; regenerate the preview")
    for item in changes:
        api(f"repos/{REPO}/issues/{item['number']}", auth, "PATCH", item["patch"])
        print(f"Converted #{item['number']}")
    for label in sorted(RETIRED):
        try:
            api(f"repos/{REPO}/labels/{quote(label, safe='')}", auth, "DELETE")
        except HTTPError as error:
            if error.code != 404:
                raise
    print("Conversion applied. No issue states or historical verification ticks were changed.")


if __name__ == "__main__":
    main()
