#!/usr/bin/env python

import re


__all__ = ['parse_line']


_START = r"^\s*"
_END = r"\s*$"

_COMMENT_MARKERS = r"(//|//!|#)"
_COMMENT_TEXT = r"(?P<comment>\w+(?:\s+\w+)*)"
_COMMENT_RE = re.compile(rf"{_START}{_COMMENT_MARKERS}\s*{_COMMENT_TEXT}{_END}")

_QUANTITY = r"(?P<quantity>\d+)"

_CARD_ATOM = r"(?:\w|[-+,/'\"])"
_CARD_NAME = rf"(?P<card_name>{_CARD_ATOM}+(?:\s+{_CARD_ATOM}+)*)"

_EXTENSION = r"\((?P<extension>\w+)\)"
_COLLECTOR_NUMBER = r"(?P<collector_number>[\w-]+)"

_TAGS_BLOCK = r"(?P<tags>#!?.*)"
_TAG_SPLIT_RE = re.compile(r"#!?\s*")

_CARD_RE = re.compile(
    rf"{_START}"
    rf"{_QUANTITY}\s+{_CARD_NAME}"
    rf"(?:\s+{_EXTENSION}(?:\s+{_COLLECTOR_NUMBER})?)?"
    rf"(?:\s*{_TAGS_BLOCK})?"
    rf"{_END}",
)


def _parse_tags(tags_block: str) -> list[str]:
    parts = _TAG_SPLIT_RE.split(tags_block)
    return [p.strip() for p in parts if p.strip()]


def parse_line(line: str) -> dict[str, str]:
    line = line.strip()

    match = _COMMENT_RE.match(line)
    if match:
        return match.groupdict()

    match = _CARD_RE.match(line)
    if match:
        d = match.groupdict()
        d = {k: v for k, v in d.items() if v is not None}
        if "tags" in d:
            d["tags"] = _parse_tags(d["tags"])
        return d

    return {}
