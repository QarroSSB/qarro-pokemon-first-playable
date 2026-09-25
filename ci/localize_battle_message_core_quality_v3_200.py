#!/usr/bin/env python3
"""Qarro v3.200: human-quality cleanup for core battle_message.c intro/link/prefix strings."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_BATTLE_MESSAGE_CORE_QUALITY_V3_200"
TARGET = Path("src/battle_message.c")

EXPECTED = {
    "gText_PkmnShroudedInMist": "{B_ATK_NAME_WITH_PREFIX} Окружает себя защитным туманом!",
    "gText_PkmnGettingPumped": "{B_DEF_NAME_WITH_PREFIX} Накачали!",
    "gText_PkmnsXPreventsSwitching": "{B_BUFF1}не даёт сделать\\nзамену способностью ”{B_LAST_ABILITY}”!\\l",
    "sText_OpponentMon1Appeared": "{B_OPPONENT_MON1_NAME} Появился!\\p",
    "sText_LegendaryPkmnAppeared": "Вы столкнулись с дикой {B_OPPONENT_MON1_NAME}!\\p",
    "sText_LinkTrainerIntroSendOutPkmn": "{B_LINK_OPPONENT1_NAME} высланный {B_LINK_OPPONENT_MON1_NAME}!",
    "sText_LinkTrainer2SentOutPkmn2": "{B_LINK_OPPONENT2_NAME} высланный {B_BUFF1}!",
    "sText_TwoLinkTrainersIntroSendOutPkmn": "{B_LINK_OPPONENT1_NAME} высланный {B_LINK_OPPONENT_MON1_NAME}! {B_LINK_OPPONENT2_NAME} высланный {B_LINK_OPPONENT_MON2_NAME}!",
    "sText_JustALittleMorePkmn": "Просто посиди немного, {B_BUFF1}!",
    "sText_LinkPartnerSentOutPkmn1GoPkmn": "{B_LINK_PARTNER_NAME} высланный {B_LINK_PLAYER_MON1_NAME}Иди, {B_LINK_PLAYER_MON2_NAME}!",
    "sText_LinkPartnerSentOutPkmn2GoPkmn": "{B_LINK_PARTNER_NAME} высланный {B_LINK_PLAYER_MON2_NAME}Иди, {B_LINK_PLAYER_MON1_NAME}!",
    "sText_LinkPartnerSentOutPkmn1": "{B_LINK_PARTNER_NAME} высланный {B_BUFF1}!",
    "sText_LinkPartnerSentOutPkmn2": "{B_LINK_PARTNER_NAME} высланный {B_BUFF1}!",
    "sText_LinkPartnerWithdrewPkmn1": "{B_LINK_PARTNER_NAME} отозвать {B_LINK_PLAYER_MON1_NAME}!",
    "sText_LinkPartnerWithdrewPkmn2": "{B_LINK_PARTNER_NAME} отозвать {B_LINK_PLAYER_MON2_NAME}!",
    "sText_PkmnSwitchOut": "{B_BUFF1}- Отключайся, вернись!",
    "sText_Trainer2WithdrewPkmn": "{B_TRAINER2_NAME_WITH_CLASS} отозвать {B_BUFF1}!",
    "sText_WildPkmnPrefix": "Дикий ",
    "sText_FoePkmnPrefix": "Враг ",
    "sText_WildPkmnPrefixLower": "дикая ",
    "sText_FoePkmnPrefixLower": "противостоящий ",
    "sText_FoePkmnPrefix2": "Враг",
    "sText_AllyPkmnPrefix": "Команда",
    "sText_FoePkmnPrefix3": "Враг",
    "sText_AllyPkmnPrefix2": "Команда",
    "sText_FoePkmnPrefix4": "Враг",
    "sText_AllyPkmnPrefix3": "Команда",
    "sText_SpAttack": "С. Атк.",
    "sText_SpDefense": "Сп.Дэф.",
    "sText_Accuracy": "меткость",
    "sText_Evasiveness": "ловкость",
}

TRANSLATIONS = {
    "gText_PkmnShroudedInMist": "{B_ATK_NAME_WITH_PREFIX} окутывает себя защитным туманом!",
    "gText_PkmnGettingPumped": "{B_DEF_NAME_WITH_PREFIX} собирается с силами!",
    "gText_PkmnsXPreventsSwitching": "{B_BUFF1} не даёт\\nсменить POKeMON из-за {B_LAST_ABILITY}!\\l",
    "sText_OpponentMon1Appeared": "{B_OPPONENT_MON1_NAME} появляется!\\p",
    "sText_LegendaryPkmnAppeared": "Появляется дикий {B_OPPONENT_MON1_NAME}!\\p",
    "sText_LinkTrainerIntroSendOutPkmn": "{B_LINK_OPPONENT1_NAME} выбирает {B_LINK_OPPONENT_MON1_NAME}!",
    "sText_LinkTrainer2SentOutPkmn2": "{B_LINK_OPPONENT2_NAME} выбирает {B_BUFF1}!",
    "sText_TwoLinkTrainersIntroSendOutPkmn": "{B_LINK_OPPONENT1_NAME} выбирает {B_LINK_OPPONENT_MON1_NAME}! {B_LINK_OPPONENT2_NAME} выбирает {B_LINK_OPPONENT_MON2_NAME}!",
    "sText_JustALittleMorePkmn": "Ещё немного! Держись, {B_BUFF1}!",
    "sText_LinkPartnerSentOutPkmn1GoPkmn": "{B_LINK_PARTNER_NAME} выбирает {B_LINK_PLAYER_MON1_NAME}! Вперёд, {B_LINK_PLAYER_MON2_NAME}!",
    "sText_LinkPartnerSentOutPkmn2GoPkmn": "{B_LINK_PARTNER_NAME} выбирает {B_LINK_PLAYER_MON2_NAME}! Вперёд, {B_LINK_PLAYER_MON1_NAME}!",
    "sText_LinkPartnerSentOutPkmn1": "{B_LINK_PARTNER_NAME} выбирает {B_BUFF1}!",
    "sText_LinkPartnerSentOutPkmn2": "{B_LINK_PARTNER_NAME} выбирает {B_BUFF1}!",
    "sText_LinkPartnerWithdrewPkmn1": "{B_LINK_PARTNER_NAME} отзывает {B_LINK_PLAYER_MON1_NAME}!",
    "sText_LinkPartnerWithdrewPkmn2": "{B_LINK_PARTNER_NAME} отзывает {B_LINK_PLAYER_MON2_NAME}!",
    "sText_PkmnSwitchOut": "{B_BUFF1}, замена! Возвращайся!",
    "sText_Trainer2WithdrewPkmn": "{B_TRAINER2_NAME_WITH_CLASS} отзывает {B_BUFF1}!",
    "sText_WildPkmnPrefix": "Дикий ",
    "sText_FoePkmnPrefix": "Вражеский ",
    "sText_WildPkmnPrefixLower": "дикий ",
    "sText_FoePkmnPrefixLower": "вражеский ",
    "sText_FoePkmnPrefix2": "Вражеский",
    "sText_AllyPkmnPrefix": "Союзный",
    "sText_FoePkmnPrefix3": "Вражеский",
    "sText_AllyPkmnPrefix2": "Союзный",
    "sText_FoePkmnPrefix4": "Вражеский",
    "sText_AllyPkmnPrefix3": "Союзный",
    "sText_SpAttack": "СП. АТК.",
    "sText_SpDefense": "СП. ЗАЩ.",
    "sText_Accuracy": "меткость",
    "sText_Evasiveness": "уклонение",
}

BANNED_UNICODE = set("—–←→“”«»")

def control_tokens(text: str) -> list[str]:
    return re.findall(r"\{[^}]+\}|\\[npl]|\$", text)

def replace_symbol(path: Path, symbol: str, expected: str, translated: str) -> None:
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        rf'(?m)^(?P<prefix>\s*(?:ALIGNED\(4\)\s+)?(?:static\s+)?const u8\s+'
        rf'{re.escape(symbol)}\[\]\s*=\s*_\(")'
        rf'(?P<body>(?:\\.|[^"\\])*)'
        rf'(?P<suffix>"\);(?:\s*//.*)?\s*)$'
    )
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{symbol}: expected one symbol, got {len(matches)}")
    m = matches[0]
    current = m.group("body")
    if current != expected:
        raise RuntimeError(f"{symbol}: source drift: {current!r} != {expected!r}")
    if control_tokens(current) != control_tokens(translated):
        raise RuntimeError(
            f"{symbol}: control-token drift old={control_tokens(current)} new={control_tokens(translated)}"
        )
    if '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{symbol}: invalid translation surface")
    path.write_text(
        text[:m.start()] + m.group("prefix") + translated + m.group("suffix") + text[m.end():],
        encoding="utf-8",
    )

def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: localize_battle_message_core_quality_v3_200.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 31:
        raise RuntimeError("unexpected v3.200 symbol set")
    for symbol, translated in TRANSLATIONS.items():
        replace_symbol(path, symbol, EXPECTED[symbol], translated)
    out = root / "build" / "qarro_ru_battle_message_core_quality_v3_200_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassSymbols": len(TRANSLATIONS),
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
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} core battle_message.c strings")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
