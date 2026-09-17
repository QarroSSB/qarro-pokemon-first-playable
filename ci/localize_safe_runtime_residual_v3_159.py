#!/usr/bin/env python3
"""Qarro v3.159: safe residual main-menu/item/Pokedex runtime localization.

Targets seven English-only runtime strings confirmed by RU runtime audit #289 on
v3.158 GREEN. Text-only pass: no gameplay, trainer, reward, inventory, flag,
progression, Ash Bond or Ash Cap logic is touched. Pokemon/Move/Ability names
remain English by policy. Brace/control tokens are preserved exactly.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

MARKER = "QARRO_RU_SAFE_RUNTIME_RESIDUAL_V3_159"
REPLACEMENTS = {
    Path("src/main_menu.c"): {
        "gText_MysteryGiftCantUse": (
            "MYSTERY GIFT can't be used while\nthe Wireless Adapter is attached.",
            "ТАЙНЫЙ ПОДАРОК недоступен,\nпока подключен беспроводной адаптер.",
        ),
        "gText_MysteryEventsCantUse": (
            "MYSTERY EVENTS can't be used while\nthe Wireless Adapter is attached.",
            "ТАЙНЫЕ СОБЫТИЯ недоступны,\nпока подключен беспроводной адаптер.",
        ),
    },
    Path("src/item_use.c"): {
        "sText_ItemFinderNearby": (
            "Huh?\nThe ITEMFINDER's responding!\\pThere's an item buried around here!{PAUSE_UNTIL_PRESS}",
            "А?\nITEMFINDER реагирует!\\pГде-то рядом зарыт предмет!{PAUSE_UNTIL_PRESS}",
        ),
        "sText_CantThrowPokeBall_TwoMons": (
            "Cannot throw a ball!\nThere are two Pokémon out there!\\p",
            "Нельзя бросить покебол!\nПеред тобой два покемона!\\p",
        ),
        "sText_CantThrowPokeBall_SemiInvulnerable": (
            "Cannot throw a ball!\nThere's no Pokémon in sight!\\p",
            "Нельзя бросить покебол!\nПокемона не видно!\\p",
        ),
    },
    Path("src/pokedex.c"): {
        "sText_SearchForPkmnBasedOnParameters": (
            "Search for POKéMON based on\nselected parameters.",
            "Искать ПОКЕМОНОВ по\nвыбранным параметрам.",
        ),
        "sText_ListByFirstLetter": (
            "List by the first letter in the name.\nSpotted POKéMON only.",
            "Список по первой букве имени.\nТолько замеченные ПОКЕМОНЫ.",
        ),
    },
}
TOKEN_RE = re.compile(r"\{[^{}]+\}")
STRING_RE = re.compile(r'"((?:\\.|[^"\\])*)"', re.S)


def c_escape(s: str) -> str:
    """Encode ordinary C whitespace while preserving FireRed text controls."""
    # FireRed controls such as \p and \l are consumed by the project preprocessor.
    # Doubling their backslash turns them into an ordinary backslash and breaks
    # charmap preprocessing (the v3.159 Build #607 failure in src/item_use.c).
    return (
        s.replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )


def decode_c_literal(literal: str) -> str:
    """Decode only ordinary C escapes and preserve FireRed text escapes verbatim."""
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
            # FireRed control escapes such as \p and \l are not Python escapes.
            out.append("\\" + nxt)
        i += 2
    return "".join(out)


def decode_c_string_body(body: str) -> str:
    parts = []
    for literal in STRING_RE.findall(body):
        # Physical source line splices are formatting only.
        literal = literal.replace("\\\r\n", "").replace("\\\n", "")
        parts.append(decode_c_literal(literal))
    return "".join(parts)


def replace_symbol(text: str, symbol: str, old_raw: str, new_raw: str) -> str:
    if TOKEN_RE.findall(old_raw) != TOKEN_RE.findall(new_raw):
        raise RuntimeError(f"token mismatch in {symbol}")
    pat = re.compile(
        rf"(?ms)^(?P<prefix>[ \t]*(?:static\s+)?const\s+u8\s+{re.escape(symbol)}\[\]\s*=\s*_?\()"
        rf"(?P<body>.*?)(?P<suffix>\);)"
    )
    matches = list(pat.finditer(text))
    exact = []
    observed = []
    for m in matches:
        decoded = decode_c_string_body(m.group("body"))
        observed.append(decoded)
        if decoded == old_raw:
            exact.append(m)
    if len(exact) != 1:
        raise RuntimeError(
            f"expected exactly one audited declaration for {symbol}, "
            f"found {len(exact)}; observed={observed!r}"
        )
    m = exact[0]
    repl = m.group("prefix") + '"' + c_escape(new_raw) + '"' + m.group("suffix")
    return text[:m.start()] + repl + text[m.end():]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_safe_runtime_residual_v3_159.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    applied = []
    for rel, items in REPLACEMENTS.items():
        path = root / rel
        text = path.read_text(encoding="utf-8")
        for symbol, (old_raw, new_raw) in items.items():
            text = replace_symbol(text, symbol, old_raw, new_raw)
            applied.append({"file": str(rel), "symbol": symbol, "old": old_raw, "new": new_raw})
        path.write_text(text, encoding="utf-8")
    out = root / "build" / "qarro_ru_safe_runtime_residual_v3_159_audit.json"
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
    print(f"[{MARKER}] PASS: translated {len(applied)} safe runtime strings; gameplay/logic/Ash untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
