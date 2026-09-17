#!/usr/bin/env python3
"""Qarro v3.158: low-risk residual party/runtime localization.

Targets five English-only runtime strings confirmed by RU runtime audit #285 on
v3.157 GREEN. Text-only pass: no gameplay, trainer, reward, inventory, flag,
progression, Ash Bond or Ash Cap logic is touched. Pokemon/Move/Ability names
remain English by policy. Brace/control tokens are preserved exactly.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

MARKER = "QARRO_RU_PARTY_RUNTIME_RESIDUAL_V3_158"

REPLACEMENTS = {
    Path("src/party_menu.c"): {
        "sText_CannotSendMonToBoxHM": (
            "Cannot send that mon to the box,\nbecause it knows a HM move.{PAUSE_UNTIL_PRESS}",
            "Нельзя отправить этого покемона в Бокс,\nпотому что он знает HM-прием.{PAUSE_UNTIL_PRESS}",
        ),
        "sText_CannotSendMonToBoxPartner": (
            "Cannot send a mon that doesn't\nbelong to you to the box.{PAUSE_UNTIL_PRESS}",
            "Нельзя отправить в Бокс покемона,\nкоторый тебе не принадлежит.{PAUSE_UNTIL_PRESS}",
        ),
        "sText_askText": (
            "It might affect {STR_VAR_1}'s stats.\nAre you sure you want to use it?",
            "Это может повлиять на параметры {STR_VAR_1}.\nВсе равно использовать?",
        ),
        "sText_doneText": (
            "{STR_VAR_1}'s stats may have changed due\nto the effects of the {STR_VAR_2}!{PAUSE_UNTIL_PRESS}",
            "Параметры {STR_VAR_1} могли измениться\nиз-за эффекта {STR_VAR_2}!{PAUSE_UNTIL_PRESS}",
        ),
    },
    Path("src/data/moves_info.h"): {
        "gNotDoneYetDescription": (
            "This move can't be used.\nIts effect is in development.",
            "Этот прием пока нельзя использовать.\nЕго эффект еще разрабатывается.",
        ),
    },
}

TOKEN_RE = re.compile(r"\{[^{}]+\}")

def c_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

def replace_symbol(text: str, symbol: str, old_raw: str, new_raw: str) -> str:
    if TOKEN_RE.findall(old_raw) != TOKEN_RE.findall(new_raw):
        raise RuntimeError(f"token mismatch in {symbol}")
    # Expansion strings use _("..."); match one declaration only and fail closed.
    pat = re.compile(
        rf"(?m)^(?P<prefix>(?:static\s+)?const\s+u8\s+{re.escape(symbol)}\[\]\s*=\s*_?\()"
        rf"(?P<quote>\"(?:\\.|[^\"\\])*\")(?P<suffix>\);)"
    )
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one declaration for {symbol}, found {len(matches)}")
    m = matches[0]
    literal = m.group("quote")[1:-1]
    decoded = bytes(literal, "utf-8").decode("unicode_escape") if all(ord(c) < 128 for c in literal) else literal
    # For the pinned English anchors all source bytes are ASCII; compare exact runtime text.
    if decoded != old_raw:
        raise RuntimeError(f"source drift for {symbol}: {decoded!r}")
    repl = m.group("prefix") + '"' + c_escape(new_raw) + '"' + m.group("suffix")
    return text[:m.start()] + repl + text[m.end():]

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_party_runtime_residual_v3_158.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    applied = []
    for rel, items in REPLACEMENTS.items():
        path = root / rel
        text = path.read_text(encoding="utf-8")
        for symbol, (old_raw, new_raw) in items.items():
            text = replace_symbol(text, symbol, old_raw, new_raw)
            applied.append({"file": str(rel), "symbol": symbol})
        path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_party_runtime_residual_v3_158_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "translated": applied,
        "translatedCount": len(applied),
        "policy": "Pokemon/Move/Ability names English; descriptions/UI/dialogue/system text Russian",
        "logicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {len(applied)} residual runtime strings; logic/Ash Bond/Ash Cap untouched")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
