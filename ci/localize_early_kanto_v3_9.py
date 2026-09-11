#!/usr/bin/env python3
"""Qarro v3.10 early-Kanto Russian localization continuation.

Runs the exact verified v3.9 early-Kanto localization from build #265, then
continues the playable route through Route 2 and Viridian Forest. The new pass
is fail-closed: every untouched English block must match exactly once.

Pokemon species, Move and Ability proper names remain English. Ash Bond / Ash
Cap code is not referenced or changed.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "efd18a1123d7e91ab6e857d19b1ed197a4fde3ef"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_9"
MARKER = "QARRO_RU_EARLY_KANTO_V3_10"
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
    "data/maps/Route2_Frlg/scripts.inc": {
        "Route2_Text_RouteSign": (
            (r"ROUTE 2\n", r"VIRIDIAN CITY - PEWTER CITY$"),
            (r"МАРШРУТ 2\n", r"ВИРИДИАН-СИТИ - ПЬЮТЕР-СИТИ$"),
        ),
        "Route2_Text_DiglettsCave": (
            (r"DIGLETT'S CAVE$",),
            (r"ПЕЩЕРА DIGLETT$",),
        ),
    },
    "data/maps/ViridianForest_Frlg/scripts.inc": {
        "ViridianForest_Text_FriendsItchingToBattle": (
            (
                r"I came here with some friends to\n",
                r"catch us some BUG POKéMON!\p",
                r"They're all itching to get into\n",
                r"some POKéMON battles!$",
            ),
            (
                r"Я пришёл сюда с друзьями\n",
                r"ловить ПОКЕМОНОВ-НАСЕКОМЫХ!\p",
                r"Им всем не терпится\n",
                r"сразиться в ПОКЕМОН-боях!$",
            ),
        ),
        "ViridianForest_Text_RickIntro": (
            (r"Hey! You have POKéMON!\n", r"Come on!\l", r"Let's battle 'em!$"),
            (r"Эй! У тебя есть ПОКЕМОНЫ!\n", r"Ну же!\l", r"Давай сразимся!$"),
        ),
        "ViridianForest_Text_RickDefeat": (
            (r"No!\nCATERPIE can't hack it!$",),
            (r"Нет!\nCATERPIE не справился!$",),
        ),
        "ViridianForest_Text_RickPostBattle": (
            (r"Ssh! You'll scare the bugs away.\n", r"Another time, okay?$"),
            (r"Тсс! Ты распугаешь насекомых.\n", r"В другой раз, ладно?$"),
        ),
        "ViridianForest_Text_DougIntro": (
            (r"Yo!\n", r"You can't jam out if you're a\l", r"POKéMON TRAINER!$"),
            (r"Йо!\n", r"Если ты ТРЕНЕР ПОКЕМОНОВ,\l", r"от боя не отвертишься!$"),
        ),
        "ViridianForest_Text_DougDefeat": (
            (r"Huh?\n", r"I ran out of POKéMON!$"),
            (r"Что?\n", r"У меня кончились ПОКЕМОНЫ!$"),
        ),
        "ViridianForest_Text_DougPostBattle": (
            (r"That totally stinks! I'm going to\n", r"catch some stronger ones!$"),
            (r"Вот отстой! Пойду ловить\n", r"кого-нибудь посильнее!$"),
        ),
        "ViridianForest_Text_SammyIntro": (
            (r"Hey, wait up!\n", r"What's the hurry? Why the rush?$"),
            (r"Эй, погоди!\n", r"Куда ты так спешишь?$"),
        ),
        "ViridianForest_Text_SammyDefeat": (
            (r"I give!\n", r"You're good at this!$"),
            (r"Сдаюсь!\n", r"У тебя отлично получается!$"),
        ),
        "ViridianForest_Text_SammyPostBattle": (
            (
                r"Sometimes, you can find stuff on\n",
                r"the ground.\p",
                r"I'm looking for the stuff I\n",
                r"dropped. Can you help me?$",
            ),
            (
                r"Иногда на земле можно найти\n",
                r"разные вещи.\p",
                r"Я ищу то, что потерял.\n",
                r"Поможешь мне?$",
            ),
        ),
        "ViridianForest_Text_AnthonyIntro": (
            (r"I might be little, but I won't like\n", r"it if you go easy on me!$"),
            (r"Я хоть и маленький, но не смей\n", r"мне поддаваться!$"),
        ),
        "ViridianForest_Text_AnthonyDefeat": (
            (r"Oh, boo.\n", r"Nothing went right.$"),
            (r"Эх...\n", r"Всё пошло не так.$"),
        ),
        "ViridianForest_Text_AnthonyPostBattle": (
            (r"I lost some of my allowance…$",),
            (r"Я лишился карманных денег...$",),
        ),
        "ViridianForest_Text_CharlieIntro": (
            (r"Did you know that POKéMON evolve?$",),
            (r"ПОКЕМОНЫ умеют эволюционировать?$",),
        ),
        "ViridianForest_Text_CharlieDefeat": (
            (r"Oh!\n", r"I lost!$"),
            (r"Ох!\n", r"Я проиграл!$"),
        ),
        "ViridianForest_Text_CharliePostBattle": (
            (r"BUG POKéMON evolve quickly.\n", r"They're a lot of fun!$"),
            (r"ПОКЕМОНЫ-НАСЕКОМЫЕ быстро\n", r"эволюционируют. С ними весело!$"),
        ),
        "ViridianForest_Text_RanOutOfPokeBalls": (
            (
                r"I was throwing POKé BALLS to\n",
                r"catch POKéMON, and I ran out.\p",
                r"That's why you can never have too\n",
                r"many POKé BALLS.$",
            ),
            (
                r"Я ловил ПОКЕМОНОВ ПОКЕБОЛАМИ,\n",
                r"но они у меня закончились.\p",
                r"Вот почему ПОКЕБОЛОВ никогда\n",
                r"не бывает слишком много.$",
            ),
        ),
        "ViridianForest_Text_AvoidGrassyAreasWhenWeak": (
            (
                r"TRAINER TIPS\p",
                r"If your POKéMON are weak and you\n",
                r"want to avoid battles, stay away\l",
                r"from grassy areas!$",
            ),
            (
                r"СОВЕТЫ ТРЕНЕРА\p",
                r"Если ПОКЕМОНЫ ослабли и ты\n",
                r"хочешь избежать боёв, держись\l",
                r"подальше от высокой травы!$",
            ),
        ),
        "ViridianForest_Text_UseAntidoteForPoison": (
            (r"For poison, use ANTIDOTE!\n", r"Get it at POKéMON MARTS!$"),
            (r"От яда - ПРОТИВОЯДИЕ!\n", r"Купи его в ПОКЕ-МАРКЕТЕ!$"),
        ),
        "ViridianForest_Text_ContactOakViaPCToRatePokedex": (
            (r"TRAINER TIPS\p", r"Contact PROF. OAK via a PC to\n", r"get your POKéDEX evaluated!$"),
            (r"СОВЕТЫ ТРЕНЕРА\p", r"Свяжись с ПРОФ. ОУКОМ через ПК,\n", r"чтобы он оценил твой ПОКЕДЕКС!$"),
        ),
        "ViridianForest_Text_CantCatchOwnedMons": (
            (
                r"TRAINER TIPS\p",
                r"You can't catch a POKéMON that\n",
                r"belongs to someone else.\p",
                r"Throw POKé BALLS only at wild\n",
                r"POKéMON to catch them!$",
            ),
            (
                r"СОВЕТЫ ТРЕНЕРА\p",
                r"Нельзя поймать ПОКЕМОНА,\n",
                r"который принадлежит другому.\p",
                r"Бросай ПОКЕБОЛЫ только\n",
                r"в диких ПОКЕМОНОВ!$",
            ),
        ),
        "ViridianForest_Text_WeakenMonsBeforeCapture": (
            (
                r"TRAINER TIPS\p",
                r"Weaken POKéMON before attempting\n",
                r"capture!\p",
                r"When healthy, they may escape!$",
            ),
            (
                r"СОВЕТЫ ТРЕНЕРА\p",
                r"Ослабь ПОКЕМОНА перед тем,\n",
                r"как пытаться его поймать!\p",
                r"Здоровый ПОКЕМОН может сбежать!$",
            ),
        ),
        "ViridianForest_Text_LeavingViridianForest": (
            (r"LEAVING VIRIDIAN FOREST\n", r"PEWTER CITY AHEAD$"),
            (r"ВЫХОД ИЗ ВИРИДИАНСКОГО ЛЕСА\n", r"ВПЕРЕДИ ПЬЮТЕР-СИТИ$"),
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
        "__name__": "qarro_ru_early_kanto_v39_base",
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
    if audit.get("marker") != BASE_MARKER or audit.get("selectedBlocksLocalized") != 64:
        raise RuntimeError(
            "base localization audit drift: expected marker "
            f"{BASE_MARKER!r} and 64 blocks, got "
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
        print(f"[ru-early-v310] {rel}: {changed}/{len(blocks)} blocks changed")

    expected_new = 25
    if sum(len(v) for v in PATCHES.values()) != expected_new:
        raise RuntimeError("Route 2 / Viridian Forest localization scope drift")
    if changed_total != expected_new:
        raise RuntimeError(
            f"fresh pinned checkout should change all {expected_new} new blocks; got {changed_total}"
        )

    audit["previousMarker"] = BASE_MARKER
    audit["marker"] = MARKER
    audit["selectedBlocksLocalized"] = 64 + expected_new
    audit["blocksChangedThisRun"] = int(audit.get("blocksChangedThisRun", 0)) + changed_total
    audit["route2Localized"] = True
    audit["viridianForestLocalized"] = True
    audit["viridianForestTrainerDialogueLocalized"] = True
    audit["viridianForestTrainerTipsLocalized"] = True
    audit["pokemonSpeciesProperNamesEnglish"] = True
    audit["moveProperNamesEnglish"] = True
    audit["abilityProperNamesEnglish"] = True
    audit["ashBondTouched"] = False
    audit["ashCapTouched"] = False
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: base 64 + {expected_new} Route 2/Forest blocks = "
        f"{audit['selectedBlocksLocalized']} localized blocks"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
