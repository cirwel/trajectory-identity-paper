#!/usr/bin/env python3
"""Check mechanical agreement of this repository's release metadata.

This checks the current Markdown, CFF and Zenodo schemas, not scientific claims,
PDF freshness, or whether a release has actually been deposited. The CFF reader
deliberately accepts only the scalar and folded-abstract forms used here; an
unsupported representation fails rather than silently skipping a check.
"""

import argparse
from datetime import datetime
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys


CONCEPT_DOI = "10.5281/zenodo.20098168"
REPOSITORY_URL = "https://github.com/cirwel/trajectory-identity-paper"


def normalized(text):
    return " ".join(text.split())


def one(pattern, text, label):
    matches = re.findall(pattern, text, re.MULTILINE)
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {label}, found {len(matches)}")
    return matches[0]


def cff_scalar(text, key):
    raw = one(rf"^{re.escape(key)}: (.+)$", text, f"CFF {key}")
    if raw.startswith('"'):
        value = json.loads(raw)
        if isinstance(value, str):
            return value
    elif key == "date-released" and re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
        return raw
    raise ValueError(f"unsupported CFF {key} format")


def cff_abstract(text):
    one(r"^(abstract: >)$", text, "CFF folded abstract")
    lines = []
    for line in text.split("abstract: >\n", 1)[1].splitlines():
        if line and not line.startswith("  "):
            break
        lines.append(line.strip())
    return normalized(" ".join(lines))


class Paragraphs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.paragraphs = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            if self.current is not None:
                raise ValueError("nested paragraph in Zenodo description")
            self.current = []

    def handle_endtag(self, tag):
        if tag == "p":
            if self.current is None:
                raise ValueError("unmatched paragraph in Zenodo description")
            self.paragraphs.append(normalized("".join(self.current)))
            self.current = None

    def handle_data(self, data):
        if self.current is not None:
            self.current.append(data)
        elif data.strip():
            raise ValueError("Zenodo description text must be inside paragraphs")


def check(root, tag=None):
    manuscript = (root / "TRAJECTORY_IDENTITY_PAPER.md").read_text()
    cff = (root / "CITATION.cff").read_text()
    zenodo = json.loads((root / ".zenodo.json").read_text())
    title = one(r"^# (.+)$", manuscript, "manuscript title")
    version = one(r"^\*\*Version:\*\* (.+)$", manuscript, "manuscript version")
    if not re.fullmatch(r"\d+\.\d+(?:\.\d+)?(?:-[A-Za-z0-9.-]+)?", version):
        raise ValueError("unsupported manuscript version format")
    date = datetime.strptime(
        one(r"^\*\*Date:\*\* (.+)$", manuscript, "manuscript date"),
        "%B %d, %Y",
    ).date().isoformat()
    abstract = one(
        r"^## Abstract\n\n([\s\S]+?)\n\n---$", manuscript, "manuscript abstract"
    ).replace("**", "")
    expected_tag = f"paper-v{version}"
    pairs = [
        ("CFF title", cff_scalar(cff, "title"), title),
        ("Zenodo title", zenodo["title"], title),
        ("CFF version", cff_scalar(cff, "version"), f"v{version}"),
        ("Zenodo version", zenodo["version"], expected_tag),
        ("CFF date", cff_scalar(cff, "date-released"), date),
        ("Zenodo date", zenodo["publication_date"], date),
        ("CFF concept DOI", cff_scalar(cff, "doi"), CONCEPT_DOI),
        ("CFF abstract", cff_abstract(cff), normalized(abstract)),
    ]
    if tag is not None:
        pairs.append(("requested release tag", tag, expected_tag))
    for label, actual, expected in pairs:
        if actual != expected:
            raise ValueError(f"{label} does not match the manuscript/release target")
    description = Paragraphs()
    description.feed(zenodo["description"])
    description.close()
    expected_paragraphs = [normalized(p) for p in abstract.split("\n\n")]
    if description.current is not None or (
        description.paragraphs[-len(expected_paragraphs):] != expected_paragraphs
    ):
        raise ValueError("Zenodo description must end with the current manuscript abstract")
    supplement = f"{REPOSITORY_URL}/tree/{expected_tag}"
    supplements = [
        item["identifier"] for item in zenodo["related_identifiers"]
        if item.get("relation") == "isSupplementTo"
        and item.get("identifier", "").startswith(f"{REPOSITORY_URL}/tree/")
    ]
    if supplements != [supplement]:
        raise ValueError("Zenodo repository supplement does not match the release tag")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--tag", help="also check the tag requested for publication")
    args = parser.parse_args()
    try:
        check(args.root, args.tag)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"release metadata: {error}", file=sys.stderr)
        return 1
    print("release metadata: title, version, date, abstract and target links agree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
