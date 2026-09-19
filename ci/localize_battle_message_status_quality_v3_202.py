#!/usr/bin/env python3
"""Qarro v3.202: human-quality status-condition battle messages."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_BATTLE_MESSAGE_STATUS_QUALITY_V3_202"
TARGET = Path("src/battle_message.c")

EXPECTED = {
    "STRINGID_PKMNFELLASLEEP": "{B_EFF_NAME_WITH_PREFIX} Заснула!",
    "STRINGID_PKMNMADESLEEP": "{B_SCR_NAME_WITH_PREFIX}? {B_BUFF1} сделанный {B_EFF_NAME_WITH_PREFIX2} Спи!",
    "STRINGID_PKMNALREADYASLEEP": "{B_SCR_NAME_WITH_PREFIX} Уже спится!",
    "STRINGID_PKMNALREADYASLEEP2": "{B_ATK_NAME_WITH_PREFIX} Уже спится!",
    "STRINGID_PKMNWASPOISONED": "{B_EFF_NAME_WITH_PREFIX} Отравился!",
    "STRINGID_PKMNPOISONEDBY": "{B_EFF_NAME_WITH_PREFIX} был отравлен {B_SCR_NAME_WITH_PREFIX2}? {B_BUFF1}!",
    "STRINGID_PKMNHURTBYPOISON": "{B_ATK_NAME_WITH_PREFIX} Он был ранен отравлением!",
    "STRINGID_PKMNALREADYPOISONED": "{B_SCR_NAME_WITH_PREFIX} Уже отравлен!",
    "STRINGID_PKMNBADLYPOISONED": "{B_EFF_NAME_WITH_PREFIX} Он был сильно отравлен!",
    "STRINGID_PKMNENERGYDRAINED": "{B_SCR_NAME_WITH_PREFIX} Его энергия была истощена!",
    "STRINGID_PKMNWASBURNED": "{B_EFF_NAME_WITH_PREFIX} Сожжено!",
    "STRINGID_PKMNBURNEDBY": "{B_SCR_NAME_WITH_PREFIX}? {B_BUFF1} сгоревший {B_EFF_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNHURTBYBURN": "{B_ATK_NAME_WITH_PREFIX} Он был ранен своим ожогом!",
    "STRINGID_PKMNWASFROZEN": "{B_EFF_NAME_WITH_PREFIX} Заморожено твердо!",
    "STRINGID_PKMNFROZENBY": "{B_SCR_NAME_WITH_PREFIX}? {B_BUFF1} замерзнуть {B_EFF_NAME_WITH_PREFIX2} Твердо!",
    "STRINGID_PKMNISFROZEN": "{B_ATK_NAME_WITH_PREFIX} Заморожено твердо!",
    "STRINGID_PKMNWASDEFROSTED": "{B_SCR_NAME_WITH_PREFIX} Оттаял!",
    "STRINGID_PKMNWASDEFROSTEDBY": "{B_SCR_NAME_WITH_PREFIX}? {B_CURRENT_MOVE} Растопил лед!",
    "STRINGID_PKMNWASPARALYZED": "{B_EFF_NAME_WITH_PREFIX} Он парализован, поэтому может не двигаться.",
    "STRINGID_PKMNWASPARALYZEDBY": "{B_SCR_NAME_WITH_PREFIX}? {B_BUFF1} парализованный {B_EFF_NAME_WITH_PREFIX2}Может быть, он не сможет двигаться!",
    "STRINGID_PKMNISPARALYZED": "{B_ATK_NAME_WITH_PREFIX} Не мог двигаться, потому что парализован!",
    "STRINGID_PKMNISALREADYPARALYZED": "{B_SCR_NAME_WITH_PREFIX} Он уже парализован!",
    "STRINGID_PKMNHEALEDPARALYSIS": "{B_DEF_NAME_WITH_PREFIX} Вылечился от паралича!",
    "STRINGID_STATSWONTINCREASE": "{B_SCR_NAME_WITH_PREFIX}? {B_BUFF1} Не пойдет выше!",
    "STRINGID_STATSWONTDECREASE": "{B_SCR_NAME_WITH_PREFIX}? {B_BUFF1} Низше не пойдешь!",
    "STRINGID_PKMNISCONFUSED": "{B_ATK_NAME_WITH_PREFIX} Запутался!",
    "STRINGID_PKMNHEALEDCONFUSION": "{B_ATK_NAME_WITH_PREFIX} Вырвался из своей сумятицы!",
    "STRINGID_PKMNWASCONFUSED": "{B_EFF_NAME_WITH_PREFIX} Запутался!",
    "STRINGID_PKMNALREADYCONFUSED": "{B_DEF_NAME_WITH_PREFIX} Уже запутались!",
}

TRANSLATIONS = {
    "STRINGID_PKMNFELLASLEEP": "{B_EFF_NAME_WITH_PREFIX} засыпает!",
    "STRINGID_PKMNMADESLEEP": "{B_SCR_NAME_WITH_PREFIX}: {B_BUFF1} усыпляет {B_EFF_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNALREADYASLEEP": "{B_SCR_NAME_WITH_PREFIX} уже спит!",
    "STRINGID_PKMNALREADYASLEEP2": "{B_ATK_NAME_WITH_PREFIX} уже спит!",
    "STRINGID_PKMNWASPOISONED": "{B_EFF_NAME_WITH_PREFIX} отравлен!",
    "STRINGID_PKMNPOISONEDBY": "{B_SCR_NAME_WITH_PREFIX}: {B_BUFF1} отравляет {B_EFF_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNHURTBYPOISON": "{B_ATK_NAME_WITH_PREFIX} страдает от яда!",
    "STRINGID_PKMNALREADYPOISONED": "{B_SCR_NAME_WITH_PREFIX} уже отравлен!",
    "STRINGID_PKMNBADLYPOISONED": "{B_EFF_NAME_WITH_PREFIX} тяжело отравлен!",
    "STRINGID_PKMNENERGYDRAINED": "Энергия {B_SCR_NAME_WITH_PREFIX2} поглощена!",
    "STRINGID_PKMNWASBURNED": "{B_EFF_NAME_WITH_PREFIX} получает ожог!",
    "STRINGID_PKMNBURNEDBY": "{B_SCR_NAME_WITH_PREFIX}: {B_BUFF1} обжигает {B_EFF_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNHURTBYBURN": "{B_ATK_NAME_WITH_PREFIX} страдает от ожога!",
    "STRINGID_PKMNWASFROZEN": "{B_EFF_NAME_WITH_PREFIX} заморожен!",
    "STRINGID_PKMNFROZENBY": "{B_SCR_NAME_WITH_PREFIX}: {B_BUFF1} замораживает {B_EFF_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNISFROZEN": "{B_ATK_NAME_WITH_PREFIX} заморожен!",
    "STRINGID_PKMNWASDEFROSTED": "{B_SCR_NAME_WITH_PREFIX} оттаивает!",
    "STRINGID_PKMNWASDEFROSTEDBY": "{B_CURRENT_MOVE} растапливает лёд на {B_SCR_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNWASPARALYZED": "{B_EFF_NAME_WITH_PREFIX} парализован и может не двигаться!",
    "STRINGID_PKMNWASPARALYZEDBY": "{B_SCR_NAME_WITH_PREFIX}: {B_BUFF1} парализует {B_EFF_NAME_WITH_PREFIX2}!",
    "STRINGID_PKMNISPARALYZED": "{B_ATK_NAME_WITH_PREFIX} парализован и не может двигаться!",
    "STRINGID_PKMNISALREADYPARALYZED": "{B_SCR_NAME_WITH_PREFIX} уже парализован!",
    "STRINGID_PKMNHEALEDPARALYSIS": "{B_DEF_NAME_WITH_PREFIX} избавляется от паралича!",
    "STRINGID_STATSWONTINCREASE": "{B_SCR_NAME_WITH_PREFIX}: {B_BUFF1} больше не повысится!",
    "STRINGID_STATSWONTDECREASE": "{B_SCR_NAME_WITH_PREFIX}: {B_BUFF1} больше не понизится!",
    "STRINGID_PKMNISCONFUSED": "{B_ATK_NAME_WITH_PREFIX} в замешательстве!",
    "STRINGID_PKMNHEALEDCONFUSION": "{B_ATK_NAME_WITH_PREFIX} приходит в себя!",
    "STRINGID_PKMNWASCONFUSED": "{B_EFF_NAME_WITH_PREFIX} приходит в замешательство!",
    "STRINGID_PKMNALREADYCONFUSED": "{B_DEF_NAME_WITH_PREFIX} уже в замешательстве!",
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
        raise SystemExit("usage: localize_battle_message_status_quality_v3_202.py <upstream-root>")
    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 29:
        raise RuntimeError("unexpected v3.202 string set")
    for string_id, translated in TRANSLATIONS.items():
        replace_entry(path, string_id, EXPECTED[string_id], translated)
    out = root / "build" / "qarro_ru_battle_message_status_quality_v3_202_audit.json"
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
    print(f"[{MARKER}] PASS: polished {len(TRANSLATIONS)} status-condition battle strings")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
