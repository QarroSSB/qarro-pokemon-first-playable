#!/usr/bin/env python3
"""Qarro v3.13 early-Kanto Russian localization: Pallet starting-zone completion.

Runs the exact CI-verified v3.12 pass (through Route 3), then closes the
remaining user-facing text in Pallet Town exterior plus the player's house
1F/2F. The pass is fail-closed: every untouched English block must match
exactly once.

Pokemon species, Move and Ability proper names remain English. Gameplay,
trainer data, Ash Bond and Ash Cap are not modified.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "c39a990197cf866dfde92836c041de2c630c3b89"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_12"
MARKER = "QARRO_RU_EARLY_KANTO_V3_13"
AUDIT_REL = Path("build/qarro_ru_early_kanto_v3_9_audit.json")


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


PATCHES = {
    "data/maps/PalletTown_Frlg/scripts.inc": {
        "PalletTown_Text_OakDontGoOut": (
            (r"OAK: Hey! Wait!\n", r"Don't go out!$"),
            (r"ОУК: Эй! Стой!\n", r"Не выходи из города!$"),
        ),
        "PalletTown_Text_OakGrassUnsafeNeedMon": (
            (
                r"OAK: It's unsafe!\n",
                r"Wild POKéMON live in tall grass!\p",
                r"You need your own POKéMON for\n",
                r"your protection.\p",
                r"I know!\n",
                r"Here, come with me!$",
            ),
            (
                r"ОУК: Это опасно!\n",
                r"В высокой траве живут дикие\n",
                r"ПОКЕМОНЫ!\p",
                r"Тебе нужен свой ПОКЕМОН\n",
                r"для защиты.\p",
                r"Знаю!\n",
                r"Иди за мной!$",
            ),
        ),
        "PalletTown_Text_RaisingMonsToo": (
            (
                r"I'm raising POKéMON, too.\p",
                r"When they get strong, they can\n",
                r"protect me.$",
            ),
            (
                r"Я тоже выращиваю ПОКЕМОНОВ.\p",
                r"Когда они станут сильнее,\n",
                r"они смогут меня защитить.$",
            ),
        ),
        "PalletTown_Text_CanStoreItemsAndMonsInPC": (
            (
                r"Technology is incredible!\p",
                r"You can now store and recall items\n",
                r"and POKéMON as data via PC.$",
            ),
            (
                r"Технологии потрясают!\p",
                r"Теперь предметы и ПОКЕМОНОВ\n",
                r"можно хранить в ПК как данные.$",
            ),
        ),
        "PalletTown_Text_OakPokemonResearchLab": (
            (r"OAK POKéMON RESEARCH LAB$",),
            (r"ЛАБОРАТОРИЯ ПОКЕМОНОВ ОУКА$",),
        ),
        "PalletTown_Text_PlayersHouse": (
            (r"{PLAYER}'s house$",),
            (r"Дом {PLAYER}$",),
        ),
        "PalletTown_Text_RivalsHouse": (
            (r"{RIVAL}'s house$",),
            (r"Дом {RIVAL}$",),
        ),
        "PalletTown_Text_TownSign": (
            (r"PALLET TOWN\n", r"Shades of your journey await!$"),
            (r"ПАЛЛЕТ-ТАУН\n", r"Здесь начинается твой путь!$"),
        ),
        "PalletTown_Text_OakLetMeSeePokedex": (
            (
                r"OAK: Ah, {PLAYER}!\n",
                r"You're back, are you?\p",
                r"How much have you filled in your\n",
                r"POKéDEX?\p",
                r"May I see it?\p",
                r"Let's see…$",
            ),
            (
                r"ОУК: А, {PLAYER}!\n",
                r"Ты вернулся?\p",
                r"Насколько ты заполнил\n",
                r"ПОКЕДЕКС?\p",
                r"Можно взглянуть?\p",
                r"Посмотрим...$",
            ),
        ),
        "PalletTown_Text_CaughtXPuttingInHonestEffort": (
            (
                r"You've caught {STR_VAR_2}…\p",
                r"Hm, it looks as if you're putting\n",
                r"in an honest effort.\p",
                r"When you manage to fill it some\n",
                r"more, come show me, please.$",
            ),
            (
                r"Поймано: {STR_VAR_2}...\p",
                r"Хм, вижу, ты честно стараешься.\p",
                r"Когда заполнишь его еще\n",
                r"немного, покажи мне снова.$",
            ),
        ),
        "PalletTown_Text_CaughtXImpressiveFollowMe": (
            (
                r"You've caught… {STR_VAR_2}!?\n",
                r"Now, this is impressive!\p",
                r"There's something I wanted to ask\n",
                r"of you, {PLAYER}.\p",
                r"Come.\n",
                r"Follow me.$",
            ),
            (
                r"Поймано... {STR_VAR_2}!?\n",
                r"Впечатляет!\p",
                r"Я хотел кое о чем тебя\n",
                r"попросить, {PLAYER}.\p",
                r"Идем.\n",
                r"Следуй за мной.$",
            ),
        ),
        "PalletTown_Text_OakYouEnjoyingTraveling": (
            (
                r"OAK: Ah, {PLAYER}!\n",
                r"You seem to be enjoying traveling.\p",
                r"Knowing you, {PLAYER}, I can easily\n",
                r"imagine you going out to even more\l",
                r"exotic locales.\p",
                r"Good for you, good for you.\n",
                r"Hohoho.$",
            ),
            (
                r"ОУК: А, {PLAYER}!\n",
                r"Похоже, путешествия тебе\n",
                r"по душе.\p",
                r"Зная тебя, я уверен:\n",
                r"ты увидишь еще больше\l",
                r"далеких мест.\p",
                r"Так держать!\n",
                r"Хо-хо-хо.$",
            ),
        ),
        "PalletTown_Text_HmmIsThatRight": (
            (r"Hmm…\n", r"Is that right…$"),
            (r"Хм...\n", r"Вот как...$"),
        ),
        "PalletTown_Text_OhLookLook": (
            (r"Oh!\n", r"Look, look!$"),
            (r"О!\n", r"Смотри, смотри!$"),
        ),
        "PalletTown_Text_ReadItReadIt": (
            (r"Read it, read it!$",),
            (r"Прочитай, прочитай!$",),
        ),
        "PalletTown_Text_PressStartToOpenMenu": (
            (r"TRAINER TIPS\p", r"Press START to open the MENU!$"),
            (r"СОВЕТЫ ТРЕНЕРА\p", r"Нажми START, чтобы открыть\n", r"МЕНЮ!$"),
        ),
        "PalletTown_Text_SignsAreUsefulArentThey": (
            (r"Signs are useful, aren't they?$",),
            (r"Таблички полезны, правда?$",),
        ),
        "PalletTown_Text_LookCopiedTrainerTipsSign": (
            (
                r"Look, look!\p",
                r"I copied what it said on one of\n",
                r"those TRAINER TIPS signs!$",
            ),
            (
                r"Смотри, смотри!\p",
                r"Я переписала текст с одной\n",
                r"таблички СОВЕТОВ ТРЕНЕРА!$",
            ),
        ),
        "PalletTown_Text_PressStartToOpenMenuCopy": (
            (r"TRAINER TIPS!\p", r"Press START to open the MENU!$"),
            (r"СОВЕТЫ ТРЕНЕРА!\p", r"Нажми START, чтобы открыть\n", r"МЕНЮ!$"),
        ),
    },
    "data/maps/PalletTown_PlayersHouse_1F_Frlg/scripts.inc": {
        "PalletTown_PlayersHouse_1F_Text_AllBoysLeaveOakLookingForYou": (
            (
                r"MOM: …Right.\n",
                r"All boys leave home someday.\l",
                r"It said so on TV.\p",
                r"Oh, yes. PROF. OAK, next door, was\n",
                r"looking for you.$",
            ),
            (
                r"МАМА: ...Верно.\n",
                r"Когда-нибудь все мальчики\l",
                r"уходят из дома.\p",
                r"Так сказали по ТВ.\p",
                r"А, да. ПРОФ. ОУК по соседству\n",
                r"тебя искал.$",
            ),
        ),
        "PalletTown_PlayersHouse_1F_Text_AllGirlsLeaveOakLookingForYou": (
            (
                r"MOM: …Right.\n",
                r"All girls dream of traveling.\l",
                r"It said so on TV.\p",
                r"Oh, yes. PROF. OAK, next door, was\n",
                r"looking for you.$",
            ),
            (
                r"МАМА: ...Верно.\n",
                r"Все девочки мечтают\l",
                r"о путешествиях.\p",
                r"Так сказали по ТВ.\p",
                r"А, да. ПРОФ. ОУК по соседству\n",
                r"тебя искал.$",
            ),
        ),
        "PalletTown_PlayersHouse_1F_Text_YouShouldTakeQuickRest": (
            (r"MOM: {PLAYER}!\n", r"You should take a quick rest.$"),
            (r"МАМА: {PLAYER}!\n", r"Тебе стоит немного отдохнуть.$"),
        ),
        "PalletTown_PlayersHouse_1F_Text_LookingGreatTakeCare": (
            (
                r"MOM: Oh, good! You and your\n",
                r"POKéMON are looking great.\l",
                r"Take care now!$",
            ),
            (
                r"МАМА: Вот и хорошо! Ты и твои\n",
                r"ПОКЕМОНЫ отлично выглядите.\l",
                r"Береги себя!$",
            ),
        ),
        "PalletTown_PlayersHouse_1F_Text_MovieOnTVFourBoysOnRailroad": (
            (
                r"There's a movie on TV.\n",
                r"Four boys are walking on railroad\l",
                r"tracks.\p",
                r"…I better go, too.$",
            ),
            (
                r"По телевизору идет фильм.\n",
                r"Четверо мальчиков идут вдоль\l",
                r"железной дороги.\p",
                r"...Мне тоже пора идти.$",
            ),
        ),
        "PalletTown_PlayersHouse_1F_Text_MovieOnTVGirlOnBrickRoad": (
            (
                r"There's a movie on TV.\n",
                r"A girl with her hair in pigtails is\l",
                r"walking up a brick road.\p",
                r"…I better go, too.$",
            ),
            (
                r"По телевизору идет фильм.\n",
                r"Девочка с косичками идет\l",
                r"по дороге из кирпича.\p",
                r"...Мне тоже пора идти.$",
            ),
        ),
        "PalletTown_PlayersHouse_1F_Text_OopsWrongSide": (
            (r"Oops, wrong side…$",),
            (r"Ой, не с той стороны...$",),
        ),
    },
    "data/maps/PalletTown_PlayersHouse_2F_Frlg/scripts.inc": {
        "PalletTown_PlayersHouse_2F_Text_PlayedWithNES": (
            (r"{PLAYER} played with the NES.\p", r"…Okay!\n", r"It's time to go!$"),
            (r"{PLAYER} играет в NES.\p", r"...Ладно!\n", r"Пора идти!$"),
        ),
        "PalletTown_PlayersHouse_2F_Text_PressLRForHelp": (
            (
                r"It's a posted notice…\p",
                r"If you're confused, ask for HELP!\n",
                r"Press the L or R Button!$",
            ),
            (
                r"На стене висит записка...\p",
                r"Если запутался, открой ПОМОЩЬ!\n",
                r"Нажми кнопку L или R!$",
            ),
        ),
    },
}


def render_block(label: str, lines: tuple[str, ...]) -> str:
    return label + "::\n" + "".join(f'\t.string "{line}"\n' for line in lines)


def patch_file(path: Path, blocks: dict[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> int:
    text = path.read_text(encoding="utf-8")
    changed = 0
    for label, (old_lines, new_lines) in blocks.items():
        old = render_block(label, old_lines)
        new = render_block(label, new_lines)
        old_count = text.count(old)
        new_count = text.count(new)
        if old_count == 1 and new_count == 0:
            text = text.replace(old, new, 1)
            changed += 1
        elif old_count == 0 and new_count == 1:
            continue
        else:
            raise RuntimeError(
                f"{path}: {label}: expected exactly one untouched or translated block; "
                f"old={old_count}, new={new_count}"
            )
    path.write_text(text, encoding="utf-8")
    return changed


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <pokeemerald-expansion-root>", file=sys.stderr)
        return 2

    code = load_base()
    ns = {
        "__name__": "qarro_ru_early_kanto_v312_base",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(code, f"{BASE_COMMIT}:{BASE_PATH}", "exec"), ns)
    rc = int(ns["main"]() or 0)
    if rc:
        return rc

    root = Path(sys.argv[1]).resolve()
    audit_path = root / AUDIT_REL
    if not audit_path.is_file():
        raise RuntimeError(f"base localization audit missing: {AUDIT_REL}")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("marker") != BASE_MARKER or audit.get("selectedBlocksLocalized") != 132:
        raise RuntimeError(
            "base localization audit drift: expected marker "
            f"{BASE_MARKER!r} and 132 blocks, got "
            f"{audit.get('marker')!r}/{audit.get('selectedBlocksLocalized')!r}"
        )

    changed_total = 0
    for rel, blocks in PATCHES.items():
        path = root / rel
        if not path.is_file():
            raise RuntimeError(f"missing pinned source file: {rel}")
        changed = patch_file(path, blocks)
        changed_total += changed
        audit.setdefault("files", {})[rel] = {
            "selectedBlocks": len(blocks),
            "changedThisRun": changed,
        }
        print(f"[ru-early-v313] {rel}: {changed}/{len(blocks)} blocks changed")

    expected_new = 28
    if sum(len(v) for v in PATCHES.values()) != expected_new:
        raise RuntimeError("Pallet starting-zone localization scope drift")
    if changed_total != expected_new:
        raise RuntimeError(
            f"fresh pinned checkout should change all {expected_new} new blocks; got {changed_total}"
        )

    audit["previousMarker"] = BASE_MARKER
    audit["marker"] = MARKER
    audit["selectedBlocksLocalized"] = 132 + expected_new
    audit["blocksChangedThisRun"] = int(audit.get("blocksChangedThisRun", 0)) + changed_total
    audit["palletTownExteriorLocalized"] = True
    audit["palletPlayersHouseLocalized"] = True
    audit["pokemonSpeciesNamesEnglish"] = True
    audit["moveNamesEnglish"] = True
    audit["abilityNamesEnglish"] = True
    audit["gameplayTouched"] = False
    audit["trainerDataTouched"] = False
    audit["ashBondTouched"] = False
    audit["ashCapTouched"] = False
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: base {BASE_MARKER} preserved; "
        f"localized {changed_total} Pallet starting-zone blocks; "
        f"total={audit['selectedBlocksLocalized']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
