#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path.cwd()
TARGET = ROOT / "src" / "battle_message.c"

REPLACEMENTS = [
    ("Песчаная буря стихла.", "Песчаная буря утихла."),
    ("Пошёл дождь!", "Начался дождь!"),
    ("Солнечный свет стал ярче!", "Солнце засияло ярче!"),
]


def control_signature(text: str):
    return re.findall(r"\\[npl]|\\x[0-9A-Fa-f]{2}|\\[{}]", text)


def main():
    text = TARGET.read_text(encoding="utf-8")
    original = text

    for old, new in REPLACEMENTS:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"FAIL v3.211: expected exactly one anchor for {old!r}, got {count}")
        if control_signature(old) != control_signature(new):
            raise SystemExit(f"FAIL v3.211: control-token mismatch for {old!r}")
        text = text.replace(old, new, 1)

    if text == original:
        raise SystemExit("FAIL v3.211: no changes applied")

    TARGET.write_text(text, encoding="utf-8")
    print("PASS v3.211: battle weather human-quality repolish applied")
    print(f"changedStrings:{len(REPLACEMENTS)}")
    print("gameplayTouched:false")
    print("balanceTouched:false")
    print("ashBondTouched:false")
    print("ashCapTouched:false")


if __name__ == "__main__":
    main()
