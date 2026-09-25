#!/usr/bin/env python3
"""Qarro v3.212: human-quality classic battle effects and trapping messages."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_BATTLE_MESSAGE_CLASSIC_EFFECTS_QUALITY_V3_212"
TARGET = Path("src/battle_message.c")

EXPECTED = {
    "STRINGID_PKMNCOVEREDBYVEIL": "{B_ATK_TEAM1} Сторона замаскировалась в мистическую завесу!",
    "STRINGID_PKMNUSEDSAFEGUARD": "{B_SCR_NAME_WITH_PREFIX} Защищается от Safeguard!",
    "STRINGID_PKMNSAFEGUARDEXPIRED": "{B_ATK_TEAM1} Но теперь эта сторона больше не защищена мистической завесой.",
    "STRINGID_PKMNWENTTOSLEEP": "{B_ATK_NAME_WITH_PREFIX} Пошла спать!",
    "STRINGID_PKMNSLEPTHEALTHY": "{B_ATK_NAME_WITH_PREFIX} Спал и восстановил свою НР!",
    "STRINGID_PKMNWHIPPEDWHIRLWIND": "{B_ATK_NAME_WITH_PREFIX} Взрываю вихрь!",
    "STRINGID_PKMNTOOKSUNLIGHT": "{B_ATK_NAME_WITH_PREFIX} Поглощаемый свет!",
    "STRINGID_PKMNLOWEREDHEAD": "{B_ATK_NAME_WITH_PREFIX} Засунули ему в голову!",
    "STRINGID_PKMNFLEWHIGH": "{B_ATK_NAME_WITH_PREFIX} Взлетел высоко!",
    "STRINGID_PKMNDUGHOLE": "{B_ATK_NAME_WITH_PREFIX} Пробирался он под землю!",
    "STRINGID_PKMNSQUEEZEDBYBIND": "{B_EFF_NAME_WITH_PREFIX} был сжат {B_SCR_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNTRAPPEDINVORTEX": "{B_EFF_NAME_WITH_PREFIX} Застрял в вихре!",
    "STRINGID_PKMNWRAPPEDBY": "{B_EFF_NAME_WITH_PREFIX} был завернут {B_SCR_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNCLAMPED": "{B_SCR_NAME_WITH_PREFIX} сжимаясь на {B_EFF_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNHURTBY": "{B_ATK_NAME_WITH_PREFIX} пострадает от {B_BUFF1}!",
    "STRINGID_PKMNFREEDFROM": "{B_ATK_NAME_WITH_PREFIX} освобождается от {B_BUFF1}!",
    "STRINGID_PKMNCRASHED": "{B_ATK_NAME_WITH_PREFIX} Продолжал идти и разбился!",
    "STRINGID_PKMNPROTECTEDBYMIST": "{B_SCR_NAME_WITH_PREFIX} Защищены туманом!",
    "STRINGID_PKMNHITWITHRECOIL": "{B_ATK_NAME_WITH_PREFIX} Повреждён откатом!",
    "STRINGID_PKMNPROTECTEDITSELF2": "{B_ATK_NAME_WITH_PREFIX} Защищать себя!",
    "STRINGID_PKMNBUFFETEDBYSANDSTORM": "{B_ATK_NAME_WITH_PREFIX} И он был охвачен песчаной бурей!",
    "STRINGID_PKMNPELTEDBYHAIL": "{B_ATK_NAME_WITH_PREFIX} И градом озаряет!",
    "STRINGID_PKMNSEEDED": "{B_DEF_NAME_WITH_PREFIX} Он был сеян!",
    "STRINGID_PKMNAVOIDEDATTACK": "{B_DEF_NAME_WITH_PREFIX} Избегать нападения!",
    "STRINGID_BATTLERAVOIDEDATTACK": "{B_SCR_NAME_WITH_PREFIX} Избегать нападения!",
    "STRINGID_PKMNSAPPEDBYLEECHSEED": "{B_SCR_NAME_WITH_PREFIX}Здоровье человека истощается Leech Seed!",
}

TRANSLATIONS = {
    "STRINGID_PKMNCOVEREDBYVEIL": "{B_ATK_TEAM1} сторона окутана мистической завесой!",
    "STRINGID_PKMNUSEDSAFEGUARD": "{B_SCR_NAME_WITH_PREFIX}: действует Safeguard!",
    "STRINGID_PKMNSAFEGUARDEXPIRED": "{B_ATK_TEAM1} сторона больше не защищена мистической завесой!",
    "STRINGID_PKMNWENTTOSLEEP": "{B_ATK_NAME_WITH_PREFIX} засыпает!",
    "STRINGID_PKMNSLEPTHEALTHY": "{B_ATK_NAME_WITH_PREFIX}: сон восстанавливает HP!",
    "STRINGID_PKMNWHIPPEDWHIRLWIND": "{B_ATK_NAME_WITH_PREFIX} поднимает вихрь!",
    "STRINGID_PKMNTOOKSUNLIGHT": "{B_ATK_NAME_WITH_PREFIX} поглощает свет!",
    "STRINGID_PKMNLOWEREDHEAD": "{B_ATK_NAME_WITH_PREFIX} пригибает голову!",
    "STRINGID_PKMNFLEWHIGH": "{B_ATK_NAME_WITH_PREFIX} взмывает высоко!",
    "STRINGID_PKMNDUGHOLE": "{B_ATK_NAME_WITH_PREFIX} скрывается под землёй!",
    "STRINGID_PKMNSQUEEZEDBYBIND": "{B_EFF_NAME_WITH_PREFIX} попадает в захват {B_SCR_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNTRAPPEDINVORTEX": "{B_EFF_NAME_WITH_PREFIX} попадает в вихрь!",
    "STRINGID_PKMNWRAPPEDBY": "{B_EFF_NAME_WITH_PREFIX} попадает в обхват {B_SCR_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNCLAMPED": "{B_SCR_NAME_WITH_PREFIX} крепко зажимает {B_EFF_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNHURTBY": "{B_ATK_NAME_WITH_PREFIX} получает урон от {B_BUFF1}!",
    "STRINGID_PKMNFREEDFROM": "{B_ATK_NAME_WITH_PREFIX} освобождается от {B_BUFF1}!",
    "STRINGID_PKMNCRASHED": "{B_ATK_NAME_WITH_PREFIX} не может остановиться и врезается!",
    "STRINGID_PKMNPROTECTEDBYMIST": "{B_SCR_NAME_WITH_PREFIX} под защитой тумана!",
    "STRINGID_PKMNHITWITHRECOIL": "{B_ATK_NAME_WITH_PREFIX} получает урон от отдачи!",
    "STRINGID_PKMNPROTECTEDITSELF2": "{B_ATK_NAME_WITH_PREFIX} защищается!",
    "STRINGID_PKMNBUFFETEDBYSANDSTORM": "{B_ATK_NAME_WITH_PREFIX} страдает от песчаной бури!",
    "STRINGID_PKMNPELTEDBYHAIL": "{B_ATK_NAME_WITH_PREFIX} страдает от града!",
    "STRINGID_PKMNSEEDED": "{B_DEF_NAME_WITH_PREFIX}: семена пускают корни!",
    "STRINGID_PKMNAVOIDEDATTACK": "{B_DEF_NAME_WITH_PREFIX} уклоняется от атаки!",
    "STRINGID_BATTLERAVOIDEDATTACK": "{B_SCR_NAME_WITH_PREFIX} уклоняется от атаки!",
    "STRINGID_PKMNSAPPEDBYLEECHSEED": "{B_SCR_NAME_WITH_PREFIX} теряет здоровье из-за Leech Seed!",
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
        raise SystemExit("usage: localize_battle_message_classic_effects_quality_v3_212.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 26:
        raise RuntimeError("unexpected v3.212 string set")
    for string_id, translated in TRANSLATIONS.items():
        replace_entry(path, string_id, EXPECTED[string_id], translated)
    out = root / "build" / "qarro_ru_battle_message_classic_effects_quality_v3_212_audit.json"
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
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} classic battle-effect strings")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
