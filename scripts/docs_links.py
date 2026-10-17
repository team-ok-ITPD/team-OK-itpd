"""Keep repository-only evidence links usable on the docs-only Pages site."""

import posixpath
import re
from urllib.parse import urlsplit, urlunsplit


REPOSITORY = "https://github.com/team-ok-ITPD/team-OK-itpd/blob/main/"


def on_page_markdown(markdown, page, **kwargs):
    if page.file.src_uri == 'assumptions.md':
        markdown = re.sub(
            r'^(## (ASM-\d+) .+)$',
            lambda m: m.group(1) + ' {#' + m.group(2).lower() + '}',
            markdown, flags=re.MULTILINE,
        )

    def rewrite(match):
        target = urlsplit(match.group(1))
        if target.scheme or target.netloc or not target.path:
            return match.group(0)
        resolved = posixpath.normpath(
            posixpath.join(posixpath.dirname(page.file.src_uri), target.path)
        )
        if not resolved.startswith("../"):
            return match.group(0)
        repository_path = posixpath.normpath(posixpath.join("docs", resolved))
        url = urlunsplit(("", "", repository_path, target.query, target.fragment))
        return "](" + REPOSITORY + url + ")"

    return re.sub(r"\]\(([^\s)]+)\)", rewrite, markdown)
