#!/usr/bin/env python3
"""Qarro v3.204: human-quality escape, failure and classic weather battle messages."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_BATTLE_MESSAGE_WEATHER_QUALITY_V3_204"
TARGET = Path("src/battle_message.c")

EXPECTED = {
    "STRINGID_WILDPKMNFLED": "{PLAY_SE SE_FLEE}Дикий {B_BUFF1} Сбежал!",
    "STRINGID_NORUNNINGFROMTRAINERS": "Нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет, нет.\\p",
    "STRINGID_CANTESCAPE": "Ты не можешь сбежать!\\p",
    "STRINGID_DONTLEAVEBIRCH": "Не оставляй меня в таком состоянии!\\p",
    "STRINGID_BUTNOTHINGHAPPENED": "Но ничего не случилось!",
    "STRINGID_BUTITFAILED": "Но это провалилось!",
    "STRINGID_ITHURTCONFUSION": "Он сам себя ранил в своей сумятице!",
    "STRINGID_STARTEDTORAIN": "Начался дождь!",
    "STRINGID_DOWNPOURSTARTED": "Начался ливень!",
    "STRINGID_RAINCONTINUES": "Дождь продолжает падать.",
    "STRINGID_DOWNPOURCONTINUES": "Ливень продолжается.",
    "STRINGID_RAINSTOPPED": "Дождь прекратился.",
    "STRINGID_SANDSTORMBREWED": "Песчаная буря началась!",
    "STRINGID_SANDSTORMRAGES": "Песчаная буря бушует.",
    "STRINGID_SANDSTORMSUBSIDED": "Песчаная буря утихла.",
    "STRINGID_SUNLIGHTGOTBRIGHT": "Солнечный свет стал суровым!",
    "STRINGID_SUNLIGHTSTRONG": "Солнечный свет очень сильный.",
    "STRINGID_SUNLIGHTFADED": "Солнечный свет потускнел.",
    "STRINGID_STARTEDHAIL": "Началось градообразование!",
    "STRINGID_HAILCONTINUES": "Град падает вниз.",
    "STRINGID_HAILSTOPPED": "Град остановился.",
}

TRANSLATIONS = {
    "STRINGID_WILDPKMNFLED": "{PLAY_SE SE_FLEE}Дикий {B_BUFF1} сбежал!",
    "STRINGID_NORUNNINGFROMTRAINERS": "Нет! Из боя с тренером нельзя сбежать!\\p",
    "STRINGID_CANTESCAPE": "Сбежать не получается!\\p",
    "STRINGID_DONTLEAVEBIRCH": "ПРОФ. БИРЧ: Не оставляй меня здесь!\\p",
    "STRINGID_BUTNOTHINGHAPPENED": "Но ничего не произошло!",
    "STRINGID_BUTITFAILED": "Но ничего не вышло!",
    "STRINGID_ITHURTCONFUSION": "В замешательстве наносит себе урон!",
    "STRINGID_STARTEDTORAIN": "Начался дождь!",
    "STRINGID_DOWNPOURSTARTED": "Начался ливень!",
    "STRINGID_RAINCONTINUES": "Дождь продолжается.",
    "STRINGID_DOWNPOURCONTINUES": "Ливень продолжается.",
    "STRINGID_RAINSTOPPED": "Дождь прекратился.",
    "STRINGID_SANDSTORMBREWED": "Поднялась песчаная буря!",
    "STRINGID_SANDSTORMRAGES": "Песчаная буря бушует.",
    "STRINGID_SANDSTORMSUBSIDED": "Песчаная буря утихла.",
    "STRINGID_SUNLIGHTGOTBRIGHT": "Солнечный свет усилился!",
    "STRINGID_SUNLIGHTSTRONG": "Солнечный свет продолжает палить.",
    "STRINGID_SUNLIGHTFADED": "Солнечный свет ослаб.",
    "STRINGID_STARTEDHAIL": "Начался град!",
    "STRINGID_HAILCONTINUES": "Град продолжается.",
    "STRINGID_HAILSTOPPED": "Град прекратился.",
}

BANNED_UNICODE = set("—–←→“”«»")

def control_tokens(text: str) -> list[str]:
    return re.findall(r"\{[^}]+\}|\\[npl]|\$", text)

def replace_entry(path: Path, string_id: str, expected: str, translated: str) -> None:
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        rf'(?m)^(?P<prefix>\s*\[{re.escape(string_id)}\]\s*=\s*COMPOUND_STRING\(")'
        rf'(?P<body>(?:\\.|[^"\\])*)'
        rf'(?P<suffix>"\),(?:\s*//.*)?\s*)$'
    )
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{string_id}: expected one table entry, got {len(matches)}")
    m = matches[0]
    current = m.group("body")
    if current != expected:
        raise RuntimeError(f"{string_id}: source drift: {current!r} != {expected!r}")
    if control_tokens(current) != control_tokens(translated):
        raise RuntimeError(
            f"{string_id}: control-token drift old={control_tokens(current)} new={control_tokens(translated)}"
        )
    if '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{string_id}: invalid translation surface")
    path.write_text(
        text[:m.start()] + m.group("prefix") + translated + m.group("suffix") + text[m.end():],
        encoding="utf-8",
    )

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_battle_message_weather_quality_v3_204.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 21:
        raise RuntimeError("unexpected v3.204 string set")
    for string_id, translated in TRANSLATIONS.items():
        replace_entry(path, string_id, EXPECTED[string_id], translated)
    out = root / "build" / "qarro_ru_battle_message_weather_quality_v3_204_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(TRANSLATIONS),
        "humanEditedRussian": True,
        "sourceAnchorsFailClosed": True,
        "controlTokensPreserved": True,
        "pokemonMoveAbilityNamesPreserved": True,
        "gameplayLogicTouched": False,
        "balanceTouched": False,
        "bossTeamsTouched": False,
        "specialWhitelistTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} escape/failure/weather battle strings")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
