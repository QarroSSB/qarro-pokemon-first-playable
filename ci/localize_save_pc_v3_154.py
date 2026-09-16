#!/usr/bin/env python3
"""Qarro v3.154: fail-closed Save / PC / PC-transfer Russian localization.

Closes the remaining English runtime text in three small isolated system files.
Every block is matched exactly after the established accent normalizer, and the
ordered FireRed text escapes plus {...} tokens must remain identical.
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
    "data/text/save.inc": [
        (
            "gText_ConfirmSave",
            '''gText_ConfirmSave::\n\t.string "Would you like to save the game?$"''',
            '''gText_ConfirmSave::\n\t.string "Сохранить игру?$"''',
        ),
        (
            "gText_AlreadySavedFile",
            '''gText_AlreadySavedFile::\n\t.string "There is already a saved file.\\n"\n\t.string "Is it okay to overwrite it?$"''',
            '''gText_AlreadySavedFile::\n\t.string "Файл уже сохранен.\\n"\n\t.string "Перезаписать его?$"''',
        ),
        (
            "gText_SavingDontTurnOff",
            '''gText_SavingDontTurnOff::\n\t.string "SAVING…\\n"\n\t.string "DON'T TURN OFF THE POWER.$"''',
            '''gText_SavingDontTurnOff::\n\t.string "СОХРАНЕНИЕ...\\n"\n\t.string "НЕ ВЫКЛЮЧАЙТЕ ПИТАНИЕ.$"''',
        ),
        (
            "gText_PlayerSavedGame",
            '''gText_PlayerSavedGame::\n\t.string "{PLAYER} saved the game.$"''',
            '''gText_PlayerSavedGame::\n\t.string "{PLAYER} сохранил игру.$"''',
        ),
        (
            "gText_DifferentSaveFile",
            '''gText_DifferentSaveFile::\n\t.string "WARNING!\\p"\n\t.string "There is a different game file that\\n"\n\t.string "is already saved.\\p"\n\t.string "If you save now, the other file's\\n"\n\t.string "adventure, including items and\\l"\n\t.string "POKeMON, will be entirely lost.\\p"\n\t.string "Are you sure you want to save now\\n"\n\t.string "and overwrite the other save file?$"''',
            '''gText_DifferentSaveFile::\n\t.string "ВНИМАНИЕ!\\p"\n\t.string "Уже есть другой файл сохранения.\\n"\n\t.string "Он уже записан.\\p"\n\t.string "Если сохранить сейчас, другое\\n"\n\t.string "приключение, предметы и\\l"\n\t.string "ПОКЕМОНЫ будут потеряны.\\p"\n\t.string "Сохранить сейчас и перезаписать\\n"\n\t.string "другой файл?$"''',
        ),
        (
            "gText_SaveError",
            '''gText_SaveError::\n\t.string "Save error.\\p"\n\t.string "Please exchange the\\n"\n\t.string "backup memory.$"''',
            '''gText_SaveError::\n\t.string "Ошибка сохранения.\\p"\n\t.string "Проверьте резервную\\n"\n\t.string "память.$"''',
        ),
        (
            "gText_SavingDontTurnOffPower",
            '''gText_SavingDontTurnOffPower::\n\t.string "SAVING…\\n"\n\t.string "DON'T TURN OFF THE POWER.$"''',
            '''gText_SavingDontTurnOffPower::\n\t.string "СОХРАНЕНИЕ...\\n"\n\t.string "НЕ ВЫКЛЮЧАЙТЕ ПИТАНИЕ.$"''',
        ),
    ],
    "data/text/pc.inc": [
        (
            "Text_BootUpPC",
            '''Text_BootUpPC:\n\t.string "{PLAYER} booted up the PC.$"''',
            '''Text_BootUpPC:\n\t.string "{PLAYER} включил ПК.$"''',
        ),
        (
            "gText_WhichPCShouldBeAccessed",
            '''gText_WhichPCShouldBeAccessed::\n\t.string "Which PC should be accessed?$"''',
            '''gText_WhichPCShouldBeAccessed::\n\t.string "К какому ПК подключиться?$"''',
        ),
        (
            "gText_AccessedSomeonesPC",
            '''gText_AccessedSomeonesPC::\n\t.string "Accessed SOMEONE'S PC.$"''',
            '''gText_AccessedSomeonesPC::\n\t.string "Открыт ЧУЖОЙ ПК.$"''',
        ),
        (
            "gText_StorageSystemOpened",
            '''gText_StorageSystemOpened::\n\t.string "POKeMON Storage System opened.$"''',
            '''gText_StorageSystemOpened::\n\t.string "Открыто хранилище ПОКЕМОНОВ.$"''',
        ),
        (
            "gText_AccessedPlayersPC",
            '''gText_AccessedPlayersPC::\n\t.string "Accessed {PLAYER}'s PC.$"''',
            '''gText_AccessedPlayersPC::\n\t.string "Открыт ПК {PLAYER}.$"''',
        ),
        (
            "gText_AccessedLanettesPC",
            '''gText_AccessedLanettesPC::\n\t.string "Accessed LANETTE's PC.$"''',
            '''gText_AccessedLanettesPC::\n\t.string "Открыт ПК LANETTE.$"''',
        ),
        (
            "gText_AccessedBillsPC",
            '''gText_AccessedBillsPC::\n\t.string "Accessed BILL's PC.$"''',
            '''gText_AccessedBillsPC::\n\t.string "Открыт ПК BILL.$"''',
        ),
    ],
    "data/text/pc_transfer.inc": [
        (
            "gText_PkmnTransferredSomeonesPC",
            '''gText_PkmnTransferredSomeonesPC::\n\t.string "{STR_VAR_2} was transferred to\\n"\n\t.string "SOMEONE'S PC.\\p"\n\t.string "It was placed in \\n"\n\t.string "BOX “{STR_VAR_1}.”$"''',
            '''gText_PkmnTransferredSomeonesPC::\n\t.string "{STR_VAR_2} отправлен в\\n"\n\t.string "ЧУЖОЙ ПК.\\p"\n\t.string "Помещен в \\n"\n\t.string "БОКС {STR_VAR_1}.$"''',
        ),
        (
            "gText_PkmnTransferredLanettesPC",
            '''gText_PkmnTransferredLanettesPC::\n\t.string "{STR_VAR_2} was transferred to\\n"\n#if IS_FRLG\n\t.string "BILL'S PC.\\p"\n#else\n\t.string "LANETTE'S PC.\\p"\n#endif\n\t.string "It was placed in \\n"\n\t.string "BOX “{STR_VAR_1}.”$"''',
            '''gText_PkmnTransferredLanettesPC::\n\t.string "{STR_VAR_2} отправлен в\\n"\n#if IS_FRLG\n\t.string "ПК BILL.\\p"\n#else\n\t.string "ПК LANETTE.\\p"\n#endif\n\t.string "Помещен в \\n"\n\t.string "БОКС {STR_VAR_1}.$"''',
        ),
        (
            "gText_PkmnTransferredSomeonesPCBoxFull",
            '''gText_PkmnTransferredSomeonesPCBoxFull::\n\t.string "BOX “{STR_VAR_3}” on\\n"\n\t.string "SOMEONE'S PC was full.\\p"\n\t.string "{STR_VAR_2} was transferred to\\n"\n\t.string "BOX “{STR_VAR_1}.”$"''',
            '''gText_PkmnTransferredSomeonesPCBoxFull::\n\t.string "БОКС {STR_VAR_3} в\\n"\n\t.string "ЧУЖОМ ПК заполнен.\\p"\n\t.string "{STR_VAR_2} отправлен в\\n"\n\t.string "БОКС {STR_VAR_1}.$"''',
        ),
        (
            "gText_PkmnTransferredLanettesPCBoxFull",
            '''gText_PkmnTransferredLanettesPCBoxFull::\n\t.string "BOX “{STR_VAR_3}” on\\n"\n#if IS_FRLG\n\t.string "BILL'S PC was full.\\p"\n#else\n\t.string "LANETTE'S PC was full.\\p"\n#endif\n\t.string "{STR_VAR_2} was transferred to\\n"\n\t.string "BOX “{STR_VAR_1}.”$"''',
            '''gText_PkmnTransferredLanettesPCBoxFull::\n\t.string "БОКС {STR_VAR_3} в\\n"\n#if IS_FRLG\n\t.string "ПК BILL заполнен.\\p"\n#else\n\t.string "ПК LANETTE заполнен.\\p"\n#endif\n\t.string "{STR_VAR_2} отправлен в\\n"\n\t.string "БОКС {STR_VAR_1}.$"''',
        ),
        (
            "gText_PkmnSentToPCAfterCatch",
            '''gText_PkmnSentToPCAfterCatch::\n\t.string "{STR_VAR_2} was sent to\\n"\n\t.string "{B_PC_CREATOR_NAME} PC.\\p"\n\t.string "It was placed in \\n"\n\t.string "BOX “{STR_VAR_1}”.$"''',
            '''gText_PkmnSentToPCAfterCatch::\n\t.string "{STR_VAR_2} отправлен в\\n"\n\t.string "ПК {B_PC_CREATOR_NAME}.\\p"\n\t.string "Помещен в \\n"\n\t.string "БОКС {STR_VAR_1}.$"''',
        ),
        (
            "gText_PlayerObtainedTheMon",
            '''gText_PlayerObtainedTheMon::\n\t.string "{PLAYER} obtained\\n"\n\t.string "the {STR_VAR_1}!$"''',
            '''gText_PlayerObtainedTheMon::\n\t.string "{PLAYER} получает\\n"\n\t.string "{STR_VAR_1}!$"''',
        ),
        (
            "gText_NoMoreRoomForPokemon",
            '''gText_NoMoreRoomForPokemon::\n\t.string "There's no more room for POKeMON!\\p"\n\t.string "The POKeMON BOXES are full and\\n"\n\t.string "can't accept any more!$"''',
            '''gText_NoMoreRoomForPokemon::\n\t.string "Больше нет места для ПОКЕМОНОВ!\\p"\n\t.string "БОКСЫ ПОКЕМОНОВ заполнены и\\n"\n\t.string "больше никого не вместят!$"''',
        ),
        (
            "gText_NicknameThisPokemon",
            '''gText_NicknameThisPokemon::\n\t.string "Do you want to give a nickname to\\n"\n\t.string "this {STR_VAR_1}?$"''',
            '''gText_NicknameThisPokemon::\n\t.string "Дать прозвище\\n"\n\t.string "{STR_VAR_1}?$"''',
        ),
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
    old_count = text.count(old)
    new_count = text.count(new)
    if old_count == 1 and new_count == 0:
        return text.replace(old, new, 1), 1
    if old_count == 0 and new_count == 1:
        raise RuntimeError(f"{label}: already localized unexpectedly; fail closed")
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
            print(f"[QARRO_RU_SAVE_PC_V3_154] {label}: localized")
        if text == before:
            raise RuntimeError(f"{rel}: no changes made")
        path.write_text(text, encoding="utf-8")
        print(f"[QARRO_RU_SAVE_PC_V3_154] {rel}: translated {len(blocks)} blocks")

    if total != 22:
        raise RuntimeError(f"expected 22 translated blocks, got {total}")
    print("[QARRO_RU_SAVE_PC_V3_154] PASS: 22 Save/PC/PC-transfer blocks localized; exact controls/tokens preserved; gameplay/Ash untouched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
