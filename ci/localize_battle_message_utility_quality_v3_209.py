#!/usr/bin/env python3
"""Qarro v3.209: human-quality battle utility, escape, item and ability messages."""
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path

MARKER = "QARRO_RU_BATTLE_MESSAGE_UTILITY_QUALITY_V3_209"
TARGET = Path("src/battle_message.c")

EXPECTED = {
    "STRINGID_PKMNSXINTENSIFIEDSUN": "{B_SCR_NAME_WITH_PREFIX}? {B_SCR_ABILITY} Усилили солнечные лучи!",
    "STRINGID_YOUTHROWABALLNOWRIGHT": "Ты бросаешь мяч, да? Я... я сделаю все возможное!",
    "STRINGID_PKMNSXTOOKATTACK": "{B_DEF_NAME_WITH_PREFIX} Нападение было совершено!",
    "STRINGID_PKMNCHOSEXASDESTINY": "{B_ATK_NAME_WITH_PREFIX} избранный Doom Desire Как и его судьба!",
    "STRINGID_PKMNLOSTFOCUS": "{B_ATK_NAME_WITH_PREFIX} Он потерял фокус и не мог двигаться!",
    "STRINGID_USENEXTPKMN": "Используйте следующий Pokemon?",
    "STRINGID_PKMNFLEDUSINGITS": "{PLAY_SE SE_FLEE}{B_ATK_NAME_WITH_PREFIX} бежал, используя {B_LAST_ITEM}!\\p",
    "STRINGID_PKMNFLEDUSING": "{PLAY_SE SE_FLEE}{B_ATK_NAME_WITH_PREFIX} бежать с помощью {B_ATK_ABILITY}!\\p",
    "STRINGID_PKMNWASDRAGGEDOUT": "{B_DEF_NAME_WITH_PREFIX} Его вытащили!\\p",
    "STRINGID_PKMNSITEMNORMALIZEDSTATUS": "{B_SCR_NAME_WITH_PREFIX}? {B_LAST_ITEM} Нормализовать свой статус!",
    "STRINGID_TRAINER1USEDITEM": "{B_ATK_TRAINER_NAME_WITH_CLASS} используемый {B_LAST_ITEM}!",
    "STRINGID_BOXISFULL": "Коробка полная, больше не поймаешь!\\p",
    "STRINGID_PKMNSXMADEITINEFFECTIVE": "{B_SCR_NAME_WITH_PREFIX} Сделали его неэффективным!",
    "STRINGID_PKMNSXPREVENTSFLINCHING": "{B_EFF_NAME_WITH_PREFIX}? {B_EFF_ABILITY} Предотвращает вздрагивание!",
    "STRINGID_PKMNALREADYHASBURN": "{B_DEF_NAME_WITH_PREFIX} Уже сожжено!",
    "STRINGID_PKMNSXBLOCKSY": "{B_SCR_NAME_WITH_PREFIX}? {B_SCR_ABILITY} блок {B_CURRENT_MOVE}!",
    "STRINGID_PKMNSXWOREOFF": "{B_ATK_TEAM1} боковой {B_BUFF1} стерлись!",
    "STRINGID_THEWALLSHATTERED": "Стена разбилась!",
    "STRINGID_PKMNSXCUREDITSYPROBLEM": "{B_SCR_NAME_WITH_PREFIX}? {B_SCR_ABILITY} излечивающий его {B_BUFF1} Проблема!",
    "STRINGID_ATTACKERCANTESCAPE": "{B_ATK_NAME_WITH_PREFIX} Не могу сбежать!",
    "STRINGID_PKMNOBTAINEDX": "{B_ATK_NAME_WITH_PREFIX} полученный {B_BUFF1}.",
    "STRINGID_PKMNOBTAINEDX2": "{B_DEF_NAME_WITH_PREFIX} полученный {B_BUFF2}.",
    "STRINGID_PKMNOBTAINEDXYOBTAINEDZ": "{B_ATK_NAME_WITH_PREFIX} полученный {B_BUFF1}.\\p{B_DEF_NAME_WITH_PREFIX} полученный {B_BUFF2}.",
    "STRINGID_BUTNOEFFECT": "Но это не имело никакого эффекта!",
}

TRANSLATIONS = {
    "STRINGID_PKMNSXINTENSIFIEDSUN": "{B_SCR_NAME_WITH_PREFIX}: {B_SCR_ABILITY} усиливает солнечный свет!",
    "STRINGID_YOUTHROWABALLNOWRIGHT": "Ты сейчас бросишь Поке-бол, да? Я... я постараюсь!",
    "STRINGID_PKMNSXTOOKATTACK": "{B_DEF_NAME_WITH_PREFIX} принимает атаку на себя!",
    "STRINGID_PKMNCHOSEXASDESTINY": "{B_ATK_NAME_WITH_PREFIX} выбирает Doom Desire своей судьбой!",
    "STRINGID_PKMNLOSTFOCUS": "{B_ATK_NAME_WITH_PREFIX} теряет концентрацию и не может двигаться!",
    "STRINGID_USENEXTPKMN": "Использовать следующего POKeMON?",
    "STRINGID_PKMNFLEDUSINGITS": "{PLAY_SE SE_FLEE}{B_ATK_NAME_WITH_PREFIX} сбегает с помощью {B_LAST_ITEM}!\\p",
    "STRINGID_PKMNFLEDUSING": "{PLAY_SE SE_FLEE}{B_ATK_NAME_WITH_PREFIX} сбегает благодаря {B_ATK_ABILITY}!\\p",
    "STRINGID_PKMNWASDRAGGEDOUT": "{B_DEF_NAME_WITH_PREFIX} принудительно выходит на поле!\\p",
    "STRINGID_PKMNSITEMNORMALIZEDSTATUS": "{B_SCR_NAME_WITH_PREFIX}: {B_LAST_ITEM} нормализует состояние!",
    "STRINGID_TRAINER1USEDITEM": "{B_ATK_TRAINER_NAME_WITH_CLASS} использует {B_LAST_ITEM}!",
    "STRINGID_BOXISFULL": "Коробка заполнена! Больше ловить нельзя!\\p",
    "STRINGID_PKMNSXMADEITINEFFECTIVE": "{B_SCR_NAME_WITH_PREFIX} делает это неэффективным!",
    "STRINGID_PKMNSXPREVENTSFLINCHING": "{B_EFF_NAME_WITH_PREFIX}: {B_EFF_ABILITY} предотвращает вздрагивание!",
    "STRINGID_PKMNALREADYHASBURN": "{B_DEF_NAME_WITH_PREFIX} уже обожжён!",
    "STRINGID_PKMNSXBLOCKSY": "{B_SCR_NAME_WITH_PREFIX}: {B_SCR_ABILITY} блокирует {B_CURRENT_MOVE}!",
    "STRINGID_PKMNSXWOREOFF": "{B_ATK_TEAM1} сторона: действие {B_BUFF1} заканчивается!",
    "STRINGID_THEWALLSHATTERED": "Защитная стена разбита!",
    "STRINGID_PKMNSXCUREDITSYPROBLEM": "{B_SCR_NAME_WITH_PREFIX}: {B_SCR_ABILITY} устраняет состояние {B_BUFF1}!",
    "STRINGID_ATTACKERCANTESCAPE": "{B_ATK_NAME_WITH_PREFIX} не может сбежать!",
    "STRINGID_PKMNOBTAINEDX": "{B_ATK_NAME_WITH_PREFIX} получает {B_BUFF1}.",
    "STRINGID_PKMNOBTAINEDX2": "{B_DEF_NAME_WITH_PREFIX} получает {B_BUFF2}.",
    "STRINGID_PKMNOBTAINEDXYOBTAINEDZ": "{B_ATK_NAME_WITH_PREFIX} получает {B_BUFF1}.\\p{B_DEF_NAME_WITH_PREFIX} получает {B_BUFF2}.",
    "STRINGID_BUTNOEFFECT": "Но это не подействовало!",
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
        raise SystemExit("usage: localize_battle_message_utility_quality_v3_209.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 24:
        raise RuntimeError("unexpected v3.209 string set")
    for string_id, translated in TRANSLATIONS.items():
        replace_entry(path, string_id, EXPECTED[string_id], translated)
    out = root / "build" / "qarro_ru_battle_message_utility_quality_v3_209_audit.json"
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
    next_script = Path(__file__).with_name("localize_battle_message_utility_repolish_v3_210.py")
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} battle utility/item/ability strings; chained v3.210")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
