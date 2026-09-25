#!/usr/bin/env python3
"""Qarro v3.208: human-quality miscellaneous battle effects and item/stat messages."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_BATTLE_MESSAGE_MISC_EFFECTS_QUALITY_V3_208"
TARGET = Path("src/battle_message.c")

EXPECTED = {
    "STRINGID_PKMNSXRESTOREDHPALITTLE2": "{B_ATK_NAME_WITH_PREFIX} И ее НР восстановили.",
    "STRINGID_PKMNSXWHIPPEDUPSANDSTORM": "{B_SCR_NAME_WITH_PREFIX}? {B_SCR_ABILITY} Разразилась песчаная буря!",
    "STRINGID_PKMNSXPREVENTSYLOSS": "{B_SCR_NAME_WITH_PREFIX}? {B_BUFF1} Не был понижен!",
    "STRINGID_PKMNSXINFATUATEDY": "{B_ATK_NAME_WITH_PREFIX} Влюбилась!",
    "STRINGID_PKMNSXMADEYINEFFECTIVE": "{B_SCR_NAME_WITH_PREFIX}Невозможно удалить предмет!",
    "STRINGID_ITSUCKEDLIQUIDOOZE": "{B_EFF_NAME_WITH_PREFIX} Высосал жидкий оози!",
    "STRINGID_PKMNTRANSFORMED": "{B_SCR_NAME_WITH_PREFIX} Преобразился!",
    "STRINGID_ELECTRICITYWEAKENED": "Мощность электричества была ослаблена!",
    "STRINGID_FIREWEAKENED": "Сила огня была ослаблена!",
    "STRINGID_PKMNHIDUNDERWATER": "{B_ATK_NAME_WITH_PREFIX} Спрятался под водой!",
    "STRINGID_PKMNSPRANGUP": "{B_ATK_NAME_WITH_PREFIX} Всплыли!",
    "STRINGID_HMMOVESCANTBEFORGOTTEN": "Теперь о его движениях нельзя забывать.\\p",
    "STRINGID_XFOUNDONEY": "{B_ATK_NAME_WITH_PREFIX} Найденный один {B_LAST_ITEM}!",
    "STRINGID_SOOTHINGAROMA": "Успокаивающий аромат пронесся по области!",
    "STRINGID_ITEMSCANTBEUSEDNOW": "Теперь предметы не могут быть использованы.{PAUSE 64}",
    "STRINGID_USINGITEMSTATOFPKMNROSE": "The {B_LAST_ITEM}{B_BUFF2} усиленный {B_SCR_NAME_WITH_PREFIX2}? {B_BUFF1}!",
    "STRINGID_USINGITEMSTATOFPKMNFELL": "The {B_LAST_ITEM}{B_BUFF2} пониженный {B_SCR_NAME_WITH_PREFIX2}? {B_BUFF1}!",
    "STRINGID_PKMNUSEDXTOGETPUMPED": "{B_SCR_NAME_WITH_PREFIX} использованный {B_LAST_ITEM} Чтобы тебя накачали!",
    "STRINGID_PKMNSXMADEYUSELESS": "{B_SCR_NAME_WITH_PREFIX}? {B_SCR_ABILITY} сделанный {B_CURRENT_MOVE} Бесполезно!",
    "STRINGID_PKMNTRAPPEDBYSANDTOMB": "{B_EFF_NAME_WITH_PREFIX} Пойманный в ловушку зыбучим песком!",
}

TRANSLATIONS = {
    "STRINGID_PKMNSXRESTOREDHPALITTLE2": "{B_ATK_NAME_WITH_PREFIX} немного восстанавливает HP.",
    "STRINGID_PKMNSXWHIPPEDUPSANDSTORM": "{B_SCR_NAME_WITH_PREFIX}: {B_SCR_ABILITY} поднимает песчаную бурю!",
    "STRINGID_PKMNSXPREVENTSYLOSS": "{B_SCR_NAME_WITH_PREFIX}: {B_BUFF1} не снижается!",
    "STRINGID_PKMNSXINFATUATEDY": "{B_ATK_NAME_WITH_PREFIX} влюбляется!",
    "STRINGID_PKMNSXMADEYINEFFECTIVE": "{B_SCR_NAME_WITH_PREFIX}: предмет нельзя отнять!",
    "STRINGID_ITSUCKEDLIQUIDOOZE": "{B_EFF_NAME_WITH_PREFIX} поглощает вязкую жидкость!",
    "STRINGID_PKMNTRANSFORMED": "{B_SCR_NAME_WITH_PREFIX} трансформируется!",
    "STRINGID_ELECTRICITYWEAKENED": "Сила электрических атак ослабла!",
    "STRINGID_FIREWEAKENED": "Сила огненных атак ослабла!",
    "STRINGID_PKMNHIDUNDERWATER": "{B_ATK_NAME_WITH_PREFIX} скрывается под водой!",
    "STRINGID_PKMNSPRANGUP": "{B_ATK_NAME_WITH_PREFIX} взмывает вверх!",
    "STRINGID_HMMOVESCANTBEFORGOTTEN": "HM-приёмы сейчас нельзя забыть.\\p",
    "STRINGID_XFOUNDONEY": "{B_ATK_NAME_WITH_PREFIX} находит {B_LAST_ITEM}!",
    "STRINGID_SOOTHINGAROMA": "По полю разносится успокаивающий аромат!",
    "STRINGID_ITEMSCANTBEUSEDNOW": "Сейчас нельзя использовать предметы.{PAUSE 64}",
    "STRINGID_USINGITEMSTATOFPKMNROSE": "{B_LAST_ITEM}{B_BUFF2}: у {B_SCR_NAME_WITH_PREFIX2} повышается {B_BUFF1}!",
    "STRINGID_USINGITEMSTATOFPKMNFELL": "{B_LAST_ITEM}{B_BUFF2}: у {B_SCR_NAME_WITH_PREFIX2} снижается {B_BUFF1}!",
    "STRINGID_PKMNUSEDXTOGETPUMPED": "{B_SCR_NAME_WITH_PREFIX} использует {B_LAST_ITEM} и собирается с силами!",
    "STRINGID_PKMNSXMADEYUSELESS": "{B_SCR_NAME_WITH_PREFIX}: {B_SCR_ABILITY} нейтрализует {B_CURRENT_MOVE}!",
    "STRINGID_PKMNTRAPPEDBYSANDTOMB": "{B_EFF_NAME_WITH_PREFIX} попадает в ловушку зыбучего песка!",
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
        raise SystemExit("usage: localize_battle_message_misc_effects_quality_v3_208.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 20:
        raise RuntimeError("unexpected v3.208 string set")
    for string_id, translated in TRANSLATIONS.items():
        replace_entry(path, string_id, EXPECTED[string_id], translated)
    out = root / "build" / "qarro_ru_battle_message_misc_effects_quality_v3_208_audit.json"
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
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} miscellaneous battle-effect strings")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
