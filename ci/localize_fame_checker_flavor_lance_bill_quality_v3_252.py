#!/usr/bin/env python3
"""Qarro v3.252: human-quality Fame Checker flavor text for Lance and Bill.

Polishes twelve main Fame Checker entries (six per person). EXPECTED bodies
are exact installed v3.8 handoff surfaces. FireRed colors, fonts and every
line/page control are preserved exactly; any source drift fails closed.

Pokemon species names stay English by project canon (ABRA). Text only:
gameplay, balance, boss teams, whitelist, Ash Bond and Ash Cap stay untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_FAME_CHECKER_FLAVOR_LANCE_BILL_QUALITY_V3_252"
TARGET = Path("data/text/fame_checker_frlg.inc")

EXPECTED = {
    "gFameCheckerFlavorText_Lance0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я возглавляю элитную четверку.\pТы можешь называть меня Лэнсом Драконом.\nТренер.$",
    "gFameCheckerFlavorText_Lance1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Вы знаете, что драконы\nмифический POKeMON.\pИх трудно поймать и поднять,\nНо их полномочия превосходят.\pОни практически неразрушимы.\nС ними не бывает умных.$",
    "gFameCheckerFlavorText_Lance2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Он выступает за справедливость!\nОн классный, но все же страстный!\lОн величайший, Ланс!$",
    "gFameCheckerFlavorText_Lance3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}У нас есть клиент, Лэнс, который\nИногда приходит.\pОн всегда покупает плащи.\pИнтересно, а много ли у него\nИдентичная плащаница дома?$",
    "gFameCheckerFlavorText_Lance4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Дедушка Ланса считается\nБудьте старшим из известного клана\lМастера драконов.$",
    "gFameCheckerFlavorText_Lance5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Из того, что я слышал, Ланс\nКузен, который является руководителем\lГде-то далеко.$",
    "gFameCheckerFlavorText_Bill0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что делает этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}В конце концов, Билл всемирно известен как\nПокеманьяк.\pОн изобрел POKeMON хранение\nСистема на PC тоже.$",
    "gFameCheckerFlavorText_Bill1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}У Билла много POKeMON!\nОн собирает и редкие!$",
    "gFameCheckerFlavorText_Bill2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Каков этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Он мой внук!\pОн всегда любил собирать вещи,\nДаже в детстве!$",
    "gFameCheckerFlavorText_Bill3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый вид POKeMON?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Билл - покеманьяк, поэтому он любит.\nвсех видов.\pПо-видимому, первый, кого он поймал\nбыл ABRA.$",
    "gFameCheckerFlavorText_Bill4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Родной город Билла - Голденрод-Сити.\nГде живут его люди.\pЯ слышал, что это довольно\nПраздничный, шумный город.$",
    "gFameCheckerFlavorText_Bill5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Очевидно, Билл просто не может\nЖелудочное молоко вообще.$",
}

TRANSLATIONS = {
    "gFameCheckerFlavorText_Lance0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Я возглавляю ЭЛИТНУЮ ЧЕТВЁРКУ.\pМожешь звать меня ЛЭНСОМ, ТРЕНЕРОМ\nДРАКОНОВ.$",
    "gFameCheckerFlavorText_Lance1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Ты ведь знаешь, что ДРАКОНЫ -\nмифические ПОКЕМОНЫ.\pИх трудно поймать и вырастить,\nно их сила превосходна.\pОни почти неуязвимы.\nХитростью их не одолеть.$",
    "gFameCheckerFlavorText_Lance2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Он борется за справедливость!\nХладнокровен, но полон страсти!\lОн лучший - ЛЭНС!$",
    "gFameCheckerFlavorText_Lance3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{FONT_FEMALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}К нам иногда заходит\nпокупатель по имени ЛЭНС.\pОн всегда покупает плащи.\pИнтересно, много ли у него дома\nодинаковых плащей?$",
    "gFameCheckerFlavorText_Lance4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Говорят, дедушка ЛЭНСА -\nстарейшина знаменитого клана\lмастеров драконов.$",
    "gFameCheckerFlavorText_Lance5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Слышал, родственник ЛЭНСА\nвозглавляет один из ГИМОВ\lгде-то далеко.$",
    "gFameCheckerFlavorText_Bill0":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Чем занимается этот человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}БИЛЛ всемирно известен как\nПОКЕМАНЬЯК.\pОн также изобрёл СИСТЕМУ ХРАНЕНИЯ\nПОКЕМОНОВ на ПК.$",
    "gFameCheckerFlavorText_Bill1":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}У БИЛЛА полно ПОКЕМОНОВ!\nОн собирает и редких!$",
    "gFameCheckerFlavorText_Bill2":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Что это за человек?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Он мой внук!\pЕщё ребёнком он обожал\nчто-нибудь коллекционировать!$",
    "gFameCheckerFlavorText_Bill3":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Любимый тип ПОКЕМОНОВ?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}БИЛЛ - ПОКЕМАНЬЯК, поэтому любит\nПОКЕМОНОВ всех видов.\pГоворят, первым он поймал\nABRA.$",
    "gFameCheckerFlavorText_Bill4":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Семья и друзья?\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Родной город БИЛЛА - ГОЛДЕНРОД,\nтам до сих пор живёт его семья.\pГоворят, это очень\nшумный и праздничный город.$",
    "gFameCheckerFlavorText_Bill5":
        r"{COLOR BLUE}{SHADOW LIGHT_BLUE}Ходят слухи...\p{FONT_MALE}{COLOR DARK_GRAY}{SHADOW LIGHT_GRAY}Говорят, БИЛЛ вообще\nне переносит молоко.$",
}

BANNED_UNICODE = set("—–←→“”«»…")


def control_tokens(text: str) -> list[str]:
    return re.findall(r"\{[^}]+\}|\\[npl]|\$", text)


def find_entry(text: str, label: str) -> re.Match[str]:
    pattern = re.compile(
        rf'(?m)^(?P<label>{re.escape(label)}::[^\n]*\n)'
        rf'(?P<prefix>\s*\.string ")'
        rf'(?P<body>(?:\\.|[^"\\])*)'
        rf'(?P<suffix>"\s*)$'
    )
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{label}: expected one Fame Checker entry, got {len(matches)}")
    return matches[0]


def replace_entry(text: str, label: str, expected: str, translated: str) -> str:
    match = find_entry(text, label)
    current = match.group("body")
    if current not in (expected, translated):
        raise RuntimeError(
            f"{label}: source drift: {current!r} not in exact expected/final surfaces"
        )
    if control_tokens(expected) != control_tokens(translated):
        raise RuntimeError(
            f"{label}: control-token drift old={control_tokens(expected)} "
            f"new={control_tokens(translated)}"
        )
    if not translated.endswith("$") or "$" in translated[:-1]:
        raise RuntimeError(f"{label}: invalid translated terminator")
    if '"' in translated or set(translated) & BANNED_UNICODE:
        raise RuntimeError(f"{label}: unsupported translated character")
    if "\n" in translated or "\r" in translated:
        raise RuntimeError(f"{label}: physical newline in translation")
    if not re.search(r"[А-Яа-яЁё]", translated):
        raise RuntimeError(f"{label}: expected Cyrillic translation")
    if current == translated:
        return text

    replacement = (
        match.group("label")
        + match.group("prefix")
        + translated
        + match.group("suffix")
    )
    return text[:match.start()] + replacement + text[match.end():]


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: localize_fame_checker_flavor_lance_bill_quality_v3_252.py <upstream-root>"
        )
    if set(EXPECTED) != set(TRANSLATIONS) or len(TRANSLATIONS) != 12:
        raise RuntimeError("unexpected v3.252 Fame Checker flavor set")

    root = Path(sys.argv[1]).resolve()
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError(f"missing target: {TARGET}")

    text = path.read_text(encoding="utf-8")
    for label in EXPECTED:
        text = replace_entry(text, label, EXPECTED[label], TRANSLATIONS[label])

    for label, translated in TRANSLATIONS.items():
        verified = find_entry(text, label).group("body")
        if verified != translated:
            raise RuntimeError(
                f"{label}: post-translation verification failed: "
                f"{verified!r} != {translated!r}"
            )

    path.write_text(text, encoding="utf-8")

    out = root / "build" / "qarro_ru_fame_checker_flavor_lance_bill_quality_v3_252_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "targetFile": str(TARGET),
        "qualityPassStrings": len(TRANSLATIONS),
        "sourceAnchorsExactFromHandoffV38": True,
        "controlTokensPreserved": True,
        "pokemonSpeciesNamesPreservedEnglish": True,
        "postTranslationSurfacesVerified": True,
        "humanEditedRussian": True,
        "gameplayLogicTouched": False,
        "balanceTouched": False,
        "bossTeamsTouched": False,
        "specialWhitelistTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: repolished {len(TRANSLATIONS)} Lance/Bill Fame Checker flavor entries"
    )

    next_script = Path(__file__).with_name("localize_fame_checker_flavor_fuji_giovanni_quality_v3_253.py")
    if not next_script.is_file():
        raise RuntimeError(f"missing chained localization pass: {next_script.name}")
    import subprocess
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
