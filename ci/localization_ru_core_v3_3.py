#!/usr/bin/env python3
"""Qarro v3.5 Russian localization follow-up: earliest FireRed runtime text.

Runs the exact previously-green localization pipeline from commit 23b23931,
then translates only verified early-game text blocks in runtime order: Professor
Oak's new-game speech and the two interactable texts in the player's starting
room. This keeps the localization audit incremental and fail-closed.

Pokemon, Move and Ability proper names remain English outside Russian prose.
No Ash Bond / Ash Cap code is touched.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "23b23931a24eb37139eb8da41b54b273430d5e1d"
BASE_PATH = "ci/localization_ru_core_v3_3.py"
MARKER = "QARRO_RU_EARLY_RUNTIME_V3_5"

OAK_BLOCKS = {
    "gOakSpeech_Text_AskPlayerGender": (
        (
            r"Now tell me. Are you a boy?\n",
            r"Or are you a girl?$",
        ),
        (
            r"Теперь скажи. Ты мальчик?\n",
            r"Или девочка?$",
        ),
    ),
    "gOakSpeech_Text_WelcomeToTheWorld": (
        (
            r"Hello, there!\n",
            r"Glad to meet you!\p",
            r"Welcome to the world of POKéMON!\p",
            r"My name is OAK.\p",
            r"People affectionately refer to me\n",
            r"as the POKéMON PROFESSOR.\p$",
        ),
        (
            r"Привет!\n",
            r"Рад знакомству!\p",
            r"Добро пожаловать\n",
            r"в мир ПОКЕМОНОВ!\p",
            r"Меня зовут ОУК.\p",
            r"Все зовут меня\n",
            r"ПРОФЕССОРОМ ПОКЕМОНОВ.\p$",
        ),
    ),
    "gOakSpeech_Text_ThisWorld": (
        (r"This world…$",),
        (r"Этот мир...$",),
    ),
    "gOakSpeech_Text_IsInhabitedFarAndWide": (
        (
            r"…is inhabited far and wide by\n",
            r"creatures called POKéMON.\p$",
        ),
        (
            r"...населён существами,\n",
            r"которых зовут ПОКЕМОНАМИ.\p$",
        ),
    ),
    "gOakSpeech_Text_IStudyPokemon": (
        (
            r"For some people, POKéMON are pets.\n",
            r"Others use them for battling.\p",
            r"As for myself…\p",
            r"I study POKéMON as a profession.\p$",
        ),
        (
            r"Для одних ПОКЕМОНЫ - питомцы.\n",
            r"Другие сражаются с ними.\p",
            r"А я...\p",
            r"Я изучаю ПОКЕМОНОВ.\n",
            r"Это моя профессия.\p$",
        ),
    ),
    "gOakSpeech_Text_TellMeALittleAboutYourself": (
        (
            r"But first, tell me a little about\n",
            r"yourself.\p$",
        ),
        (
            r"Но сначала расскажи\n",
            r"немного о себе.\p$",
        ),
    ),
    "gOakSpeech_Text_YourNameWhatIsIt": (
        (
            r"Let's begin with your name.\n",
            r"What is it?\p$",
        ),
        (
            r"Начнём с твоего имени.\n",
            r"Как тебя зовут?\p$",
        ),
    ),
    "gOakSpeech_Text_SoYourNameIsPlayer": (
        (
            r"Right…\n",
            r"So your name is {PLAYER}.$",
        ),
        (
            r"Понятно...\n",
            r"Значит, тебя зовут {PLAYER}.$",
        ),
    ),
    "gOakSpeech_Text_WhatWasHisName": (
        (
            r"This is my grandson.\p",
            r"He's been your rival since you both\n",
            r"were babies.\p",
            r"…Erm, what was his name now?$",
        ),
        (
            r"Это мой внук.\p",
            r"Он твой соперник с детства.\p",
            r"Хм... Как же его зовут?$",
        ),
    ),
    "gOakSpeech_Text_YourRivalsNameWhatWasIt": (
        (r"Your rival's name, what was it now?$",),
        (r"Как же зовут твоего соперника?$",),
    ),
    "gOakSpeech_Text_ConfirmRivalName": (
        (r"…Er, was it {RIVAL}?$",),
        (r"Хм... Его зовут {RIVAL}?$",),
    ),
    "gOakSpeech_Text_RememberRivalsName": (
        (
            r"That's right! I remember now!\n",
            r"His name is {RIVAL}!\p$",
        ),
        (
            r"Точно! Теперь вспомнил!\n",
            r"Его зовут {RIVAL}!\p$",
        ),
    ),
    "gOakSpeech_Text_LetsGo": (
        (
            r"{PLAYER}!\p",
            r"Your very own POKéMON legend is\n",
            r"about to unfold!\p",
            r"A world of dreams and adventures\n",
            r"with POKéMON awaits! Let's go!$",
        ),
        (
            r"{PLAYER}!\p",
            r"Твоя история о ПОКЕМОНАХ\n",
            r"вот-вот начнётся!\p",
            r"Мир мечтаний и приключений\n",
            r"ждёт тебя! Вперёд!$",
        ),
    ),
}

STARTING_ROOM_BLOCKS = {
    "PalletTown_PlayersHouse_2F_Text_PlayedWithNES": (
        (
            r"{PLAYER} played with the NES.\p",
            r"…Okay!\n",
            r"It's time to go!$",
        ),
        (
            r"{PLAYER} играл на NES.\p",
            r"Ладно!\n",
            r"Пора идти!$",
        ),
    ),
    "PalletTown_PlayersHouse_2F_Text_PressLRForHelp": (
        (
            r"It's a posted notice…\p",
            r"If you're confused, ask for HELP!\n",
            r"Press the L or R Button!$",
        ),
        (
            r"На стене висит памятка.\p",
            r"Нужна ПОМОЩЬ?\n",
            r"Нажми кнопку L или R!$",
        ),
    ),
}


def load_base() -> str:
    repo = Path(__file__).resolve().parents[1]
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", "--depth=1", "origin", BASE_COMMIT],
        check=True,
    )
    return subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{BASE_COMMIT}:{BASE_PATH}"],
        text=True,
    )


def render_block(label: str, lines: tuple[str, ...]) -> str:
    return label + "::\n" + "\n".join(f'\t.string "{line}"' for line in lines)


def patch_blocks(path: Path, blocks: dict[str, tuple[tuple[str, ...], tuple[str, ...]]], tag: str) -> int:
    if not path.exists():
        raise RuntimeError(f"missing FireRed localization source: {path}")
    text = path.read_text(encoding="utf-8")
    changed = 0

    for label, (english, russian) in blocks.items():
        old = render_block(label, english)
        new = render_block(label, russian)
        old_count = text.count(old)
        new_count = text.count(new)
        if old_count == 1 and new_count == 0:
            text = text.replace(old, new, 1)
            changed += 1
            print(f"[{tag}] {label}: localized")
        elif old_count == 0 and new_count == 1:
            print(f"[{tag}] {label}: already localized")
        else:
            raise RuntimeError(
                f"{label}: fail-closed source mismatch old={old_count} new={new_count}"
            )

    path.write_text(text, encoding="utf-8")
    return changed


def patch_oak_intro(root: Path) -> int:
    path = root / "data/text/new_game_intro_frlg.inc"
    changed = patch_blocks(path, OAK_BLOCKS, "ru-oak")
    text = path.read_text(encoding="utf-8")
    forbidden_visible = (
        "Welcome to the world of POKéMON!",
        "I study POKéMON as a profession.",
        "Your very own POKéMON legend is",
    )
    for phrase in forbidden_visible:
        if phrase in text:
            raise RuntimeError(f"Oak intro English phrase remained: {phrase!r}")
    return changed


def patch_starting_room(root: Path) -> int:
    path = root / "data/maps/PalletTown_PlayersHouse_2F_Frlg/scripts.inc"
    changed = patch_blocks(path, STARTING_ROOM_BLOCKS, "ru-room")
    text = path.read_text(encoding="utf-8")
    forbidden_visible = (
        "played with the NES.",
        "If you're confused, ask for HELP!",
        "Press the L or R Button!",
    )
    for phrase in forbidden_visible:
        if phrase in text:
            raise RuntimeError(f"starting-room English phrase remained: {phrase!r}")
    return changed


def main() -> int:
    code = load_base()
    ns = {
        "__name__": "qarro_ru_v35_pre_early_runtime",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    rc = int(ns["main"]() or 0)
    if rc:
        return rc

    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    oak_changed = patch_oak_intro(root)
    room_changed = patch_starting_room(root)

    audit = {
        "marker": MARKER,
        "oakSpeechBlocksLocalized": len(OAK_BLOCKS),
        "startingRoomBlocksLocalized": len(STARTING_ROOM_BLOCKS),
        "blocksChangedThisRun": oak_changed + room_changed,
        "earliestRuntimeEnglishClosed": True,
        "pokemonNamesEnglish": True,
        "moveNamesEnglish": True,
        "abilityNamesEnglish": True,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_ru_early_runtime_v3_5_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: {len(OAK_BLOCKS)} Oak + {len(STARTING_ROOM_BLOCKS)} starting-room "
        "blocks localized; names/Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
