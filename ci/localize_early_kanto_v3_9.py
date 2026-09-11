#!/usr/bin/env python3
"""Qarro v3.11 early-Kanto Russian localization continuation.

Runs the exact verified v3.10 pass (Route 2 + Viridian Forest) and continues
through the first Kanto Gym: every Pewter Gym / Brock text block is localized.
The pass is fail-closed: each untouched English block must match exactly once.

Pokemon species, Move and Ability proper names remain English. Gameplay,
trainer data, Ash Bond and Ash Cap are not modified.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BASE_COMMIT = "71d6547a4293eafd75355e5fbd70a55816bb4c98"
BASE_PATH = "ci/localize_early_kanto_v3_9.py"
BASE_MARKER = "QARRO_RU_EARLY_KANTO_V3_10"
MARKER = "QARRO_RU_EARLY_KANTO_V3_11"
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
    "data/maps/PewterCity_Gym_Frlg/scripts.inc": {
        "PewterCity_Gym_Text_BrockIntro": (
            (
                r"So, you're here. I'm BROCK.\n",
                r"I'm PEWTER's GYM LEADER.\p",
                r"My rock-hard willpower is evident\n",
                r"even in my POKéMON.\p",
                r"My POKéMON are all rock hard, and\n",
                r"have true-grit determination.\p",
                r"That's right - my POKéMON are all\n",
                r"the ROCK type!\p",
                r"Fuhaha! You're going to challenge\n",
                r"me knowing that you'll lose?\p",
                r"That's the TRAINER's honor that\n",
                r"compels you to challenge me.\p",
                r"Fine, then!\n",
                r"Show me your best!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$",
            ),
            (
                r"Итак, ты пришёл. Я BROCK.\n",
                r"Я ЛИДЕР ГИМА ПЬЮТЕР-СИТИ.\p",
                r"Моя воля тверда, как камень,\n",
                r"как и мои ПОКЕМОНЫ.\p",
                r"Мои ПОКЕМОНЫ крепки как скала\n",
                r"и никогда не сдаются.\p",
                r"Верно - все они каменного типа!\p",
                r"Ха-ха! Ты всё равно бросаешь\n",
                r"мне вызов, зная, что проиграешь?\p",
                r"Такова честь ТРЕНЕРА -\n",
                r"принять этот вызов.\p",
                r"Хорошо!\n",
                r"Покажи всё, на что способен!{PLAY_BGM}{MUS_RG_ENCOUNTER_GYM_LEADER}$",
            ),
        ),
        "PewterCity_Gym_Text_BrockDefeat": (
            (
                r"I took you for granted, and so\n",
                r"I lost.\p",
                r"As proof of your victory, I confer\n",
                r"on you this…the official POKéMON\l",
                r"LEAGUE BOULDERBADGE.\p",
                r"{FONT_NORMAL}{PLAYER} received the BOULDERBADGE\n",
                r"from BROCK!{PAUSE_MUSIC}{PLAY_BGM}{MUS_OBTAIN_BADGE}{PAUSE 0xFE}{PAUSE 0x56}{RESUME_MUSIC}\p",
                r"{FONT_MALE}Just having the BOULDERBADGE makes\n",
                r"your POKéMON more powerful.\p",
                r"It also enables the use of the\n",
                r"move FLASH outside of battle.\p",
                r"Of course, a POKéMON must know the\n",
                r"move FLASH to use it.$",
            ),
            (
                r"Я недооценил тебя и проиграл.\p",
                r"В знак победы я вручаю тебе\n",
                r"официальный КАМЕННЫЙ ЗНАЧОК\l",
                r"ЛИГИ ПОКЕМОНОВ.\p",
                r"{FONT_NORMAL}{PLAYER} получил КАМЕННЫЙ ЗНАЧОК\n",
                r"от BROCK!{PAUSE_MUSIC}{PLAY_BGM}{MUS_OBTAIN_BADGE}{PAUSE 0xFE}{PAUSE 0x56}{RESUME_MUSIC}\p",
                r"{FONT_MALE}КАМЕННЫЙ ЗНАЧОК усиливает\n",
                r"твоих ПОКЕМОНОВ.\p",
                r"Он также позволяет применять\n",
                r"FLASH вне боя.\p",
                r"Конечно, ПОКЕМОН должен знать\n",
                r"FLASH, чтобы использовать его.$",
            ),
        ),
        "PewterCity_Gym_Text_TakeThisWithYou": (
            (r"Wait!\n", r"Take this with you.$"),
            (r"Постой!\n", r"Возьми это с собой.$"),
        ),
        "PewterCity_Gym_Text_ReceivedTM39FromBrock": (
            (r"{PLAYER} received TM39\n", r"from BROCK.$"),
            (r"{PLAYER} получил ТМ39\n", r"от BROCK.$"),
        ),
        "PewterCity_Gym_Text_ExplainTM39": (
            (
                r"A TM, Technical Machine, contains a\n",
                r"technique for POKéMON.\p",
                r"Using a TM teaches the move it\n",
                r"contains to a POKéMON.\p",
                r"A TM is good for only one use.\p",
                r"So, when you use one, pick the\n",
                r"POKéMON carefully.\p",
                r"Anyways…\n",
                r"TM39 contains ROCK TOMB.\p",
                r"It hurls boulders at the foe and\n",
                r"lowers its SPEED.$",
            ),
            (
                r"ТМ, Техническая Машина,\n",
                r"содержит приём для ПОКЕМОНОВ.\p",
                r"Использование ТМ обучает\n",
                r"ПОКЕМОНА указанному приёму.\p",
                r"ТМ используется только один раз.\p",
                r"Поэтому выбирай ПОКЕМОНА\n",
                r"внимательно.\p",
                r"В общем...\n",
                r"ТМ39 содержит ROCK TOMB.\p",
                r"Он обрушивает камни на врага\n",
                r"и снижает его СКОРОСТЬ.$",
            ),
        ),
        "PewterCity_Gym_Text_BrockPostBattle": (
            (
                r"There are all kinds of TRAINERS in\n",
                r"this huge world of ours.\p",
                r"You appear to be very gifted as a\n",
                r"POKéMON TRAINER.\p",
                r"So let me make a suggestion.\p",
                r"Go to the GYM in CERULEAN and test\n",
                r"your abilities.$",
            ),
            (
                r"В нашем огромном мире много\n",
                r"разных ТРЕНЕРОВ.\p",
                r"Похоже, у тебя настоящий талант\n",
                r"ТРЕНЕРА ПОКЕМОНОВ.\p",
                r"Вот мой совет.\p",
                r"Иди в ГИМ ЦЕРУЛИН-СИТИ и\n",
                r"проверь свои силы.$",
            ),
        ),
        "PewterCity_Gym_Text_DontHaveRoomForThis": (
            (r"You don't have room for this.$",),
            (r"В СУМКЕ нет места для этого.$",),
        ),
        "PewterCity_Gym_Text_LiamIntro": (
            (r"Stop right there, kid!\p", r"You're ten thousand light-years \n", r"from facing BROCK!$"),
            (r"Стой, малыш!\p", r"До BROCK тебе ещё десять тысяч\n", r"световых лет!$"),
        ),
        "PewterCity_Gym_Text_LiamDefeat": (
            (r"Darn!\p", r"Light-years isn't time…\n", r"It measures distance!$"),
            (r"Чёрт!\p", r"Световой год - это не время...\n", r"Это единица расстояния!$"),
        ),
        "PewterCity_Gym_Text_LiamPostBattle": (
            (r"You're pretty hot.\n", r"…But not as hot as BROCK!$"),
            (r"Ты силён.\n", r"...Но до BROCK тебе далеко!$"),
        ),
        "PewterCity_Gym_Text_LetMeTakeYouToTheTop": (
            (
                r"Hiya!\n",
                r"Do you want to dream big?\p",
                r"Do you dare to dream of becoming\n",
                r"the POKéMON champ?\p",
                r"I'm no TRAINER, but I can advise\n",
                r"you on how to win.\p",
                r"Let me take you to the top!$",
            ),
            (
                r"Привет!\n",
                r"Хочешь мечтать по-крупному?\p",
                r"Готов стать ЧЕМПИОНОМ\n",
                r"ПОКЕМОНОВ?\p",
                r"Я не ТРЕНЕР, но могу подсказать,\n",
                r"как побеждать.\p",
                r"Позволь провести тебя к вершине!$",
            ),
        ),
        "PewterCity_Gym_Text_LetsGetHappening": (
            (r"All right!\n", r"Let's get happening!$"),
            (r"Отлично!\n", r"Тогда начинаем!$"),
        ),
        "PewterCity_Gym_Text_TryDifferentPartyOrders": (
            (
                r"The first POKéMON out in a match is\n",
                r"at the left of the POKéMON LIST.\p",
                r"By changing the order of POKéMON,\n",
                r"you may gain an advantage.\p",
                r"Try different orders to suit your\n",
                r"opponent's party.$",
            ),
            (
                r"Первым в бой выходит ПОКЕМОН\n",
                r"слева в СПИСКЕ ПОКЕМОНОВ.\p",
                r"Меняя порядок ПОКЕМОНОВ,\n",
                r"можно получить преимущество.\p",
                r"Подбирай порядок под команду\n",
                r"соперника.$",
            ),
        ),
        "PewterCity_Gym_Text_ItsFreeLetsGetHappening": (
            (r"It's a free service!\n", r"Let's get happening!$"),
            (r"Это бесплатно!\n", r"Тогда начинаем!$"),
        ),
        "PewterCity_Gym_Text_YoureChampMaterial": (
            (r"Just as I thought!\n", r"You're POKéMON champ material!$"),
            (r"Так я и думал!\n", r"У тебя задатки ЧЕМПИОНА!$"),
        ),
        "PewterCity_Gym_Text_GymStatue": (
            (r"PEWTER POKéMON GYM\n", r"LEADER: BROCK\p", r"WINNING TRAINERS:\n", r"{RIVAL}$"),
            (r"ПОКЕМОН-ГИМ ПЬЮТЕР-СИТИ\n", r"ЛИДЕР: BROCK\p", r"ПОБЕДИВШИЕ ТРЕНЕРЫ:\n", r"{RIVAL}$"),
        ),
        "PewterCity_Gym_Text_GymStatuePlayerWon": (
            (r"PEWTER POKéMON GYM\n", r"LEADER: BROCK\p", r"WINNING TRAINERS:\n", r"{RIVAL}, {PLAYER}$"),
            (r"ПОКЕМОН-ГИМ ПЬЮТЕР-СИТИ\n", r"ЛИДЕР: BROCK\p", r"ПОБЕДИВШИЕ ТРЕНЕРЫ:\n", r"{RIVAL}, {PLAYER}$"),
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
        "__name__": "qarro_ru_early_kanto_v310_base",
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
    if audit.get("marker") != BASE_MARKER or audit.get("selectedBlocksLocalized") != 89:
        raise RuntimeError(
            "base localization audit drift: expected marker "
            f"{BASE_MARKER!r} and 89 blocks, got "
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
        print(f"[ru-early-v311] {rel}: {changed}/{len(blocks)} blocks changed")

    expected_new = 17
    if sum(len(v) for v in PATCHES.values()) != expected_new:
        raise RuntimeError("Pewter Gym localization scope drift")
    if changed_total != expected_new:
        raise RuntimeError(
            f"fresh pinned checkout should change all {expected_new} new blocks; got {changed_total}"
        )

    audit["previousMarker"] = BASE_MARKER
    audit["marker"] = MARKER
    audit["selectedBlocksLocalized"] = 89 + expected_new
    audit["blocksChangedThisRun"] = int(audit.get("blocksChangedThisRun", 0)) + changed_total
    audit["pewterGymLocalized"] = True
    audit["brockDialogueLocalized"] = True
    audit["pewterGymAdviceLocalized"] = True
    audit["pokemonSpeciesNamesEnglish"] = True
    audit["moveNamesEnglish"] = ["FLASH", "ROCK TOMB"]
    audit["abilityNamesEnglish"] = True
    audit["gameplayTouched"] = False
    audit["trainerDataTouched"] = False
    audit["ashBondTouched"] = False
    audit["ashCapTouched"] = False
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"[{MARKER}] PASS: base {BASE_MARKER} preserved; "
        f"localized {changed_total} Pewter Gym/Brock blocks; total={audit['selectedBlocksLocalized']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
