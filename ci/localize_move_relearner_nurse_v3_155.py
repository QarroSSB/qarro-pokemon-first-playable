#!/usr/bin/env python3
"""Qarro v3.155: fail-closed Move Relearner + Pokemon Center nurse localization.

Closes the remaining English runtime text in two isolated system text files.
Every block is matched exactly against pinned Expansion 1.17.0 source. Ordered
FireRed text escapes, {...} tokens and terminators must remain identical.
Pokemon/Move/Ability proper names, trainer/gameplay logic, rewards, flags,
Ash Bond and Ash Cap are untouched.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TOKEN_RE = re.compile(r"\{[^{}]+\}")
ESCAPE_RE = re.compile(r"\\[npl]")

TARGETS = {
    "data/text/move_relearner.inc": [
        ("MoveRelearner_Text_WouldLearnNewMoves", '''MoveRelearner_Text_WouldLearnNewMoves:\n\t.string "Hi, I'm the Move Relearner.\\n"\n\t.string "Would you like to learn new moves?$"''', '''MoveRelearner_Text_WouldLearnNewMoves:\n\t.string "Я УЧИТЕЛЬ ПРИЕМОВ.\\n"\n\t.string "Хотите изучить новые приемы?$"'''),
        ("MoveRelearner_Text_LevelUpMoves", '''MoveRelearner_Text_LevelUpMoves:\n\t.string "Level Up Moves$"''', '''MoveRelearner_Text_LevelUpMoves:\n\t.string "Приемы за уровень$"'''),
        ("MoveRelearner_Text_EggMoves", '''MoveRelearner_Text_EggMoves:\n\t.string "Egg Moves$"''', '''MoveRelearner_Text_EggMoves:\n\t.string "Наследуемые приемы$"'''),
        ("MoveRelearner_Text_TMMoves", '''MoveRelearner_Text_TMMoves:\n\t.string "TM Moves$"''', '''MoveRelearner_Text_TMMoves:\n\t.string "Приемы ТМ$"'''),
        ("MoveRelearner_Text_TutormoveMoves", '''MoveRelearner_Text_TutormoveMoves:\n\t.string "Tutor Moves$"''', '''MoveRelearner_Text_TutormoveMoves:\n\t.string "Приемы учителя$"'''),
        ("MoveRelearner_Text_SeeYa", '''MoveRelearner_Text_SeeYa:\n\t.string "See ya!$"''', '''MoveRelearner_Text_SeeYa:\n\t.string "До встречи!$"'''),
        ("MoveRelearner_Text_AnythingElse", '''MoveRelearner_Text_AnythingElse:\n\t.string "Is there anything else I may do for you?$"''', '''MoveRelearner_Text_AnythingElse:\n\t.string "Могу сделать что-нибудь еще?$"'''),
        ("MoveRelearner_Text_ChoosePkmn", '''MoveRelearner_Text_ChoosePkmn:\n\t.string "Please choose your Pokémon.$"''', '''MoveRelearner_Text_ChoosePkmn:\n\t.string "Выберите ПОКЕМОНА.$"'''),
        ("MoveRelearner_Text_HaveNoPkmn", '''MoveRelearner_Text_HaveNoPkmn:\n\t.string "You have no Pokémon.$"''', '''MoveRelearner_Text_HaveNoPkmn:\n\t.string "У вас нет ПОКЕМОНОВ.$"'''),
        ("MoveRelearner_Text_CantTeachMoveToEgg", '''MoveRelearner_Text_CantTeachMoveToEgg:\n\t.string "Sorry…\\n"\n\t.string "But an Egg can't learn moves.$"''', '''MoveRelearner_Text_CantTeachMoveToEgg:\n\t.string "Извините...\\n"\n\t.string "Но ЯЙЦО не может учить приемы.$"'''),
        ("MoveRelearner_Text_CantTeachMoveToPkmn", '''MoveRelearner_Text_CantTeachMoveToPkmn:\n\t.string "Sorry…\\p"\n\t.string "It doesn't appear as if I have any move\\n"\n\t.string "I can teach that Pokémon.$"''', '''MoveRelearner_Text_CantTeachMoveToPkmn:\n\t.string "Извините...\\p"\n\t.string "Похоже, я не могу обучить этого\\n"\n\t.string "ПОКЕМОНА ни одному приему.$"'''),
        ("MoveRelearner_Text_LevelUpMoveLWR", '''MoveRelearner_Text_LevelUpMoveLWR::\n\t.string "level up move$"''', '''MoveRelearner_Text_LevelUpMoveLWR::\n\t.string "прием за уровень$"'''),
        ("MoveRelearner_Text_EggMoveLWR", '''MoveRelearner_Text_EggMoveLWR::\n\t.string "egg move$"''', '''MoveRelearner_Text_EggMoveLWR::\n\t.string "наследуемый прием$"'''),
        ("MoveRelearner_Text_TMMoveLWR", '''MoveRelearner_Text_TMMoveLWR::\n\t.string "TM move$"''', '''MoveRelearner_Text_TMMoveLWR::\n\t.string "прием ТМ$"'''),
        ("MoveRelearner_Text_TutorMoveLWR", '''MoveRelearner_Text_TutorMoveLWR::\n\t.string "tutor move$"''', '''MoveRelearner_Text_TutorMoveLWR::\n\t.string "прием учителя$"'''),
        ("MoveRelearner_Text_MoveLWR", '''MoveRelearner_Text_MoveLWR::\n\t.string "move$"''', '''MoveRelearner_Text_MoveLWR::\n\t.string "прием$"'''),
        ("MoveRelearner_Text_WhichXmoveShouldTeach", '''MoveRelearner_Text_WhichXmoveShouldTeach:\n\t.string "Which {STR_VAR_3} should I teach?$"''', '''MoveRelearner_Text_WhichXmoveShouldTeach:\n\t.string "Какой {STR_VAR_3} обучить?$"'''),
        ("MoveRelearner_Text_ThankYouComeAgain", '''MoveRelearner_Text_ThankYouComeAgain:\n\t.string "Thank you for using our services.\\n"\n\t.string "Please come again!$"''', '''MoveRelearner_Text_ThankYouComeAgain:\n\t.string "Спасибо за обращение.\\n"\n\t.string "Приходите еще!$"'''),
    ],
    "data/text/pkmn_center_nurse.inc": [
        ("gText_WouldYouLikeToRestYourPkmn", '''gText_WouldYouLikeToRestYourPkmn::\n\t.string "Hello, and welcome to\\n"\n\t.string "the POKéMON CENTER.\\p"\n\t.string "We restore your tired POKéMON\\n"\n\t.string "to full health.\\p"\n\t.string "Would you like to rest your POKéMON?$"''', '''gText_WouldYouLikeToRestYourPkmn::\n\t.string "Здравствуйте! Добро пожаловать\\n"\n\t.string "в ЦЕНТР ПОКЕМОНОВ.\\p"\n\t.string "Мы восстановим здоровье ваших\\n"\n\t.string "ПОКЕМОНОВ.\\p"\n\t.string "Хотите дать им отдохнуть?$"'''),
        ("gText_IllTakeYourPkmn", '''gText_IllTakeYourPkmn::\n\t.string "Okay, I'll take your POKéMON\\n"\n\t.string "for a few seconds.$"''', '''gText_IllTakeYourPkmn::\n\t.string "Хорошо, я заберу ваших ПОКЕМОНОВ\\n"\n\t.string "на несколько секунд.$"'''),
        ("gText_RestoredPkmnToFullHealth", '''gText_RestoredPkmnToFullHealth::\n\t.string "Thank you for waiting.\\p"\n\t.string "We've restored your POKéMON\\n"\n\t.string "to full health.$"''', '''gText_RestoredPkmnToFullHealth::\n\t.string "Спасибо за ожидание.\\p"\n\t.string "Ваши ПОКЕМОНЫ снова\\n"\n\t.string "полностью здоровы.$"'''),
        ("gText_WeHopeToSeeYouAgain", '''gText_WeHopeToSeeYouAgain::\n\t.string "We hope to see you again!$"''', '''gText_WeHopeToSeeYouAgain::\n\t.string "Ждем вас снова!$"'''),
        ("gText_WelcomeCutShort", '''gText_WelcomeCutShort::\n\t.string "Hello, and welcome to\\n"\n\t.string "the POKéMON CENTER.\\p"\n\t.string "We restore your tired POKéMON\\n"\n\t.string "to full health.\\p"\n\t.string "Would you like to…$"''', '''gText_WelcomeCutShort::\n\t.string "Здравствуйте! Добро пожаловать\\n"\n\t.string "в ЦЕНТР ПОКЕМОНОВ.\\p"\n\t.string "Мы восстановим здоровье ваших\\n"\n\t.string "ПОКЕМОНОВ.\\p"\n\t.string "Хотите...$"'''),
        ("gText_NoticesGoldCard", '''gText_NoticesGoldCard::\n\t.string "Th-that card…\\n"\n\t.string "Could it be… The GOLD CARD?!\\p"\n\t.string "Oh, the gold color is brilliant!\\n"\n\t.string "The four stars seem to sparkle!\\p"\n\t.string "I've seen several TRAINERS with\\n"\n\t.string "a SILVER CARD before, but, {PLAYER},\\l"\n\t.string "you're the first TRAINER I've ever\\l"\n\t.string "seen with a GOLD CARD!\\p"\n\t.string "Okay, {PLAYER}, please allow me\\n"\n\t.string "the honor of resting your POKéMON!$"''', '''gText_NoticesGoldCard::\n\t.string "Э-эта карта...\\n"\n\t.string "Неужели... ЗОЛОТАЯ КАРТА?!\\p"\n\t.string "Как ярко сияет золото!\\n"\n\t.string "И все четыре звезды сверкают!\\p"\n\t.string "Я встречала ТРЕНЕРОВ с\\n"\n\t.string "СЕРЕБРЯНОЙ КАРТОЙ, но, {PLAYER},\\l"\n\t.string "вы первый ТРЕНЕР с ЗОЛОТОЙ\\l"\n\t.string "КАРТОЙ, которого я вижу!\\p"\n\t.string "{PLAYER}, позвольте мне с честью\\n"\n\t.string "восстановить ваших ПОКЕМОНОВ!$"'''),
        ("gText_YouWantTheUsual", '''gText_YouWantTheUsual::\n\t.string "I'm delighted to see you, {PLAYER}!\\n"\n\t.string "You want the usual, am I right?$"''', '''gText_YouWantTheUsual::\n\t.string "{PLAYER}, рада снова вас видеть!\\n"\n\t.string "Как обычно, верно?$"'''),
        ("gText_IllTakeYourPkmn2", '''gText_IllTakeYourPkmn2::\n\t.string "Okay, I'll take your POKéMON\\n"\n\t.string "for a few seconds.$"''', '''gText_IllTakeYourPkmn2::\n\t.string "Хорошо, я заберу ваших ПОКЕМОНОВ\\n"\n\t.string "на несколько секунд.$"'''),
        ("gText_ThankYouForWaiting", '''gText_ThankYouForWaiting::\n\t.string "Thank you for waiting.$"''', '''gText_ThankYouForWaiting::\n\t.string "Спасибо за ожидание.$"'''),
        ("gText_WeHopeToSeeYouAgain2", '''gText_WeHopeToSeeYouAgain2::\n\t.string "We hope to see you again!$"''', '''gText_WeHopeToSeeYouAgain2::\n\t.string "Ждем вас снова!$"'''),
    ],
}


def tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text)


def escapes(text: str) -> list[str]:
    return ESCAPE_RE.findall(text)


def patch_block(text: str, label: str, old: str, new: str) -> tuple[str, int]:
    if tokens(old) != tokens(new):
        raise RuntimeError(f"{label}: token contract changed: {tokens(old)} -> {tokens(new)}")
    if escapes(old) != escapes(new):
        raise RuntimeError(f"{label}: FireRed escape contract changed: {escapes(old)} -> {escapes(new)}")
    if old.count("$") != new.count("$"):
        raise RuntimeError(f"{label}: terminator contract changed")
    old_count, new_count = text.count(old), text.count(new)
    if old_count == 1 and new_count == 0:
        return text.replace(old, new, 1), 1
    if old_count == 0 and new_count == 1:
        return text, 1
    raise RuntimeError(f"{label}: source drift old={old_count} new={new_count}")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    total = 0
    for rel, blocks in TARGETS.items():
        path = root / rel
        if not path.is_file():
            raise RuntimeError(f"missing target file: {path}")
        text = path.read_text(encoding="utf-8")
        before = text
        for label, old, new in blocks:
            text, changed = patch_block(text, label, old, new)
            total += changed
            print(f"[QARRO_RU_RELEARNER_NURSE_V3_155] {label}: localized")
        # Idempotent replay is valid when exact targets already equal replacements.

        path.write_text(text, encoding="utf-8")
        print(f"[QARRO_RU_RELEARNER_NURSE_V3_155] {rel}: translated {len(blocks)} blocks")
    if total != 28:
        raise RuntimeError(f"expected 28 translated blocks, got {total}")
    print("[QARRO_RU_RELEARNER_NURSE_V3_155] PASS: 28 Move Relearner/Pokemon Center nurse blocks localized; exact controls/tokens preserved; gameplay/Ash untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
