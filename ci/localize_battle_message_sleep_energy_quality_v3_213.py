#!/usr/bin/env python3
"""Qarro v3.213: human-quality sleep, uproar and energy battle messages."""
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_BATTLE_MESSAGE_SLEEP_ENERGY_QUALITY_V3_213"
TARGET = Path("src/battle_message.c")

EXPECTED = {
    "STRINGID_PKMNFASTASLEEP": "{B_ATK_NAME_WITH_PREFIX} Он быстро спит.",
    "STRINGID_PKMNWOKEUP": "{B_ATK_NAME_WITH_PREFIX} Проснулся!",
    "STRINGID_PKMNWOKEUPINUPROAR": "Негодование проснулось {B_EFF_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNCAUSEDUPROAR": "{B_EFF_NAME_WITH_PREFIX} Это вызвало возмущение!",
    "STRINGID_PKMNMAKINGUPROAR": "{B_ATK_NAME_WITH_PREFIX} Это вызывает возмущение!",
    "STRINGID_PKMNCALMEDDOWN": "{B_ATK_NAME_WITH_PREFIX} Успокойтесь.",
    "STRINGID_PKMNSTOCKPILED": "{B_ATK_NAME_WITH_PREFIX} запасной {B_BUFF1}!",
    "STRINGID_PKMNCANTSLEEPINUPROAR2": "Но {B_DEF_NAME_WITH_PREFIX2} Не могу спать в шуме!",
    "STRINGID_UPROARKEPTPKMNAWAKE": "Но шум продолжался {B_DEF_NAME_WITH_PREFIX2} Проснись!",
    "STRINGID_PKMNSTAYEDAWAKEUSING": "{B_DEF_NAME_WITH_PREFIX} Не спите!",
    "STRINGID_PKMNSTORINGENERGY": "{B_ATK_NAME_WITH_PREFIX} Хранит энергию!",
    "STRINGID_PKMNUNLEASHEDENERGY": "{B_ATK_NAME_WITH_PREFIX} Высвободил свою энергию!",
    "STRINGID_PKMNFATIGUECONFUSION": "{B_SCR_NAME_WITH_PREFIX} Запутался из-за усталости!",
    "STRINGID_PLAYERPICKEDUPMONEY": "Ты взял иену{B_BUFF1}!\\p",
    "STRINGID_PKMNUNAFFECTED": "{B_DEF_NAME_WITH_PREFIX} Не затронут!",
    "STRINGID_PKMNTRANSFORMEDINTO": "{B_ATK_NAME_WITH_PREFIX} преобразуясь в {B_BUFF1}!",
}

TRANSLATIONS = {
    "STRINGID_PKMNFASTASLEEP": "{B_ATK_NAME_WITH_PREFIX} крепко спит.",
    "STRINGID_PKMNWOKEUP": "{B_ATK_NAME_WITH_PREFIX} просыпается!",
    "STRINGID_PKMNWOKEUPINUPROAR": "Шум будит {B_EFF_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNCAUSEDUPROAR": "{B_EFF_NAME_WITH_PREFIX} поднимает шум!",
    "STRINGID_PKMNMAKINGUPROAR": "{B_ATK_NAME_WITH_PREFIX} продолжает шуметь!",
    "STRINGID_PKMNCALMEDDOWN": "{B_ATK_NAME_WITH_PREFIX} успокаивается.",
    "STRINGID_PKMNSTOCKPILED": "{B_ATK_NAME_WITH_PREFIX} запасает энергию: {B_BUFF1}!",
    "STRINGID_PKMNCANTSLEEPINUPROAR2": "Но {B_DEF_NAME_WITH_PREFIX2} не может уснуть из-за шума!",
    "STRINGID_UPROARKEPTPKMNAWAKE": "Шум не даёт {B_DEF_NAME_WITH_PREFIX2} уснуть!",
    "STRINGID_PKMNSTAYEDAWAKEUSING": "{B_DEF_NAME_WITH_PREFIX} остаётся бодрствовать!",
    "STRINGID_PKMNSTORINGENERGY": "{B_ATK_NAME_WITH_PREFIX} копит энергию!",
    "STRINGID_PKMNUNLEASHEDENERGY": "{B_ATK_NAME_WITH_PREFIX} высвобождает накопленную энергию!",
    "STRINGID_PKMNFATIGUECONFUSION": "{B_SCR_NAME_WITH_PREFIX} из-за усталости впадает в замешательство!",
    "STRINGID_PLAYERPICKEDUPMONEY": "Подобрано ¥{B_BUFF1}!\\p",
    "STRINGID_PKMNUNAFFECTED": "{B_DEF_NAME_WITH_PREFIX}: без эффекта!",
    "STRINGID_PKMNTRANSFORMEDINTO": "{B_ATK_NAME_WITH_PREFIX} превращается в {B_BUFF1}!",
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
        raise RuntimeError(f"{string_id}: control-token drift old={control_tokens(current)} new={control_tokens(translated)}")
    if '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{string_id}: invalid translation surface")
    path.write_text(text[:m.start()] + m.group("prefix") + translated + m.group("suffix") + text[m.end():], encoding="utf-8")

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_battle_message_sleep_energy_quality_v3_213.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 16:
        raise RuntimeError("unexpected v3.213 string set")
    for string_id, translated in TRANSLATIONS.items():
        replace_entry(path, string_id, EXPECTED[string_id], translated)
    out = root / "build" / "qarro_ru_battle_message_sleep_energy_quality_v3_213_audit.json"
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
    next_script = Path(__file__).with_name("localize_battle_message_final_repolish_v3_214.py")
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} sleep/uproar/energy battle strings; chained v3.214")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
