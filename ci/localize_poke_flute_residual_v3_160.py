#!/usr/bin/env python3
"""Qarro v3.160: localize the remaining audited FireRed Poke Flute runtime text.

Targets one English-only runtime string confirmed by RU runtime surface audit #294
on v3.159 GREEN and verified against pinned upstream e8bd1cd7. Text-only pass:
no gameplay, trainer, reward, inventory, flag, progression, Ash Bond or Ash Cap
logic is touched. Pokemon/Move/Ability proper names remain English by policy.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_POKE_FLUTE_RESIDUAL_V3_160"
REL = Path("src/item_use.c")
SYMBOL = "sText_PlayedPokeFluteCatchy"
OLD = "Played the POKé FLUTE.\\pNow, that's a catchy tune!{PAUSE_UNTIL_PRESS}"
NEW = "Сыграна мелодия на POKé FLUTE.\\pКакая запоминающаяся мелодия!{PAUSE_UNTIL_PRESS}"
TOKEN_RE = re.compile(r"\{[^{}]+\}")
STRING_RE = re.compile(r'"((?:\\.|[^"\\])*)"', re.S)


def decode_c_literal(literal: str) -> str:
    out = []
    i = 0
    while i < len(literal):
        ch = literal[i]
        if ch != "\\" or i + 1 >= len(literal):
            out.append(ch)
            i += 1
            continue
        nxt = literal[i + 1]
        if nxt == "n":
            out.append("\n")
        elif nxt == "r":
            out.append("\r")
        elif nxt == "t":
            out.append("\t")
        elif nxt == "\\":
            out.append("\\")
        elif nxt == '"':
            out.append('"')
        elif nxt == "'":
            out.append("'")
        else:
            # Preserve FireRed text controls such as \p and \l verbatim.
            out.append("\\" + nxt)
        i += 2
    return "".join(out)


def decode_c_string_body(body: str) -> str:
    parts = []
    for literal in STRING_RE.findall(body):
        literal = literal.replace("\\\r\n", "").replace("\\\n", "")
        parts.append(decode_c_literal(literal))
    return "".join(parts)


def c_escape(s: str) -> str:
    # Preserve FireRed control escapes; only encode ordinary C whitespace/quotes.
    return (
        s.replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_poke_flute_residual_v3_160.py <upstream-root>")
    if TOKEN_RE.findall(OLD) != TOKEN_RE.findall(NEW):
        raise RuntimeError("control token mismatch")

    root = Path(sys.argv[1]).resolve()
    path = root / REL
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        rf"(?ms)^(?P<prefix>[ \\t]*(?:static\\s+)?const\\s+u8\\s+{re.escape(SYMBOL)}\\[\\]\\s*=\\s*_?\\()"
        rf"(?P<body>.*?)(?P<suffix>\\);)"
    )
    matches = list(pat.finditer(text))
    exact = [m for m in matches if decode_c_string_body(m.group("body")) == OLD]
    if len(exact) != 1:
        observed = [decode_c_string_body(m.group("body")) for m in matches]
        raise RuntimeError(f"expected one exact pinned declaration for {SYMBOL}; found {len(exact)}; observed={observed!r}")

    m = exact[0]
    repl = m.group("prefix") + '"' + c_escape(NEW) + '"' + m.group("suffix")
    path.write_text(text[:m.start()] + repl + text[m.end():], encoding="utf-8")

    out = root / "build" / "qarro_ru_poke_flute_residual_v3_160_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "file": str(REL),
        "symbol": SYMBOL,
        "old": OLD,
        "new": NEW,
        "translatedCount": 1,
        "policy": "FireRed / Expansion 1.17.0 / Gen I-V; Pokemon+Move+Ability proper names English",
        "logicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {SYMBOL}; gameplay/logic/Ash untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
