"""Pure text-cleaning logic (no GUI imports, so it is easy to unit-test)."""
import re

_INVISIBLE = dict.fromkeys(map(ord, "​‌‍﻿"), None)


def clean_text(text, keep_paragraphs=False):
    """Collapse extra spaces / line breaks.

    keep_paragraphs=False -> everything becomes one single line.
    keep_paragraphs=True  -> blank lines separate paragraphs, each paragraph is one line.
    """
    text = text.translate(_INVISIBLE).replace(" ", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if keep_paragraphs:
        paragraphs = re.split(r"\n\s*\n", text)
        cleaned = (re.sub(r"\s+", " ", p).strip() for p in paragraphs)
        return "\n\n".join(p for p in cleaned if p)
    return re.sub(r"\s+", " ", text).strip()
