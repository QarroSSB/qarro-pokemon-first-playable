#!/usr/bin/env python3
"""Localize the first Professor Oak lab / starter sequence in FireRed.

This pass is deliberately scoped to the player's first lab visit: rival/Oak
starter dialogue, starter choice, the first rival battle, and immediate Oak
follow-up. Species proper names remain English. Ash Bond and Ash Cap are not
referenced or changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "QARRO_RU_OAK_LAB_STARTER_V3_5"

BLOCKS = {
    "PalletTown_ProfessorOaksLab_Text_RivalGrampsIsntAround": (
        (
            r"{RIVAL}: What, it's only {PLAYER}?\n",
            r"Gramps isn't around.$",
        ),
        (
            r"{RIVAL}: А, это всего лишь {PLAYER}?\n",
            r"Дедушки здесь нет.$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_RivalFedUpWithWaiting": (
        (
            r"{RIVAL}: Gramps!\n",
            r"I'm fed up with waiting!$",
        ),
        (
            r"{RIVAL}: Дедушка!\n",
            r"Мне надоело ждать!$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_RivalNoFairWhatAboutMe": (
        (
            r"{RIVAL}: Hey! Gramps! No fair!\n",
            r"What about me?$",
        ),
        (
            r"{RIVAL}: Эй! Дедушка! Нечестно!\n",
            r"А как же я?$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_RivalGoChoosePlayer": (
        (
            r"{RIVAL}: Heh, I don't need to be\n",
            r"greedy like you. I'm mature!\p",
            r"Go ahead and choose, {PLAYER}!$",
        ),
        (
            r"{RIVAL}: Хех, я не такой жадный,\n",
            r"как ты. Я уже взрослый!\p",
            r"Выбирай, {PLAYER}!$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_RivalIllTakeThisOneThen": (
        (r"{RIVAL}: I'll take this one, then!$",),
        (r"{RIVAL}: Тогда я возьму этого!$",),
    ),
    "PalletTown_ProfessorOaksLab_Text_RivalReceivedMonFromOak": (
        (
            r"{RIVAL} received the {STR_VAR_1}\n",
            r"from PROF. OAK!$",
        ),
        (
            r"{RIVAL} получил {STR_VAR_1}\n",
            r"от ПРОФ. ОУКА!$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_RivalMyMonLooksTougher": (
        (
            r"{RIVAL}: My POKéMON looks a lot\n",
            r"tougher than yours.$",
        ),
        (
            r"{RIVAL}: Мой ПОКЕМОН выглядит\n",
            r"намного сильнее твоего.$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_RivalLetsCheckOutMons": (
        (
            r"{RIVAL}: Wait, {PLAYER}!\n",
            r"Let's check out our POKéMON!\p",
            r"Come on, I'll take you on!$",
        ),
        (
            r"{RIVAL}: Стой, {PLAYER}!\n",
            r"Проверим наших ПОКЕМОНОВ!\p",
            r"Давай, я вызываю тебя!$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_RivalDefeat": (
        (
            r"WHAT?\n",
            r"Unbelievable!\l",
            r"I picked the wrong POKéMON!$",
        ),
        (
            r"ЧТО?\n",
            r"Не может быть!\l",
            r"Я выбрал не того ПОКЕМОНА!$",
        ),
    ),
    "Text_RivalVictory": (
        (
            r"{RIVAL}: Yeah!\n",
            r"Am I great or what?$",
        ),
        (
            r"{RIVAL}: Да!\n",
            r"Ну разве я не крут?$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_RivalGoToughenMyMon": (
        (
            r"{RIVAL}: Okay! I'll make my\n",
            r"POKéMON battle to toughen it up!\p",
            r"{PLAYER}! Gramps!\n",
            r"Smell you later!$",
        ),
        (
            r"{RIVAL}: Ладно! Буду сражаться,\n",
            r"чтобы мой ПОКЕМОН стал сильнее!\p",
            r"{PLAYER}! Дедушка!\n",
            r"Ещё увидимся!$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_OakThreeMonsChooseOne": (
        (
            r"OAK: {RIVAL}?\n",
            r"Let me think…\p",
            r"Oh, that's right, I told you to\n",
            r"come! Just wait!\p",
            r"Here, {PLAYER}.\p",
            r"There are three POKéMON here.\p",
            r"Haha!\p",
            r"The POKéMON are held inside\n",
            r"these POKé BALLS.\p",
            r"When I was young, I was a serious\n",
            r"POKéMON TRAINER.\p",
            r"But now, in my old age, I have\n",
            r"only these three left.\p",
            r"You can have one.\n",
            r"Go on, choose!$",
        ),
        (
            r"ОУК: {RIVAL}?\n",
            r"Дай подумать...\p",
            r"Ах да, я же просил тебя прийти!\n",
            r"Подожди немного!\p",
            r"А теперь, {PLAYER}.\p",
            r"Здесь три ПОКЕМОНА.\p",
            r"Ха-ха!\p",
            r"Они находятся внутри\n",
            r"этих ПОКЕБОЛОВ.\p",
            r"В молодости я был серьёзным\n",
            r"ТРЕНЕРОМ ПОКЕМОНОВ.\p",
            r"Но теперь я стар, и у меня\n",
            r"остались только эти трое.\p",
            r"Можешь взять одного.\n",
            r"Выбирай!$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_OakBePatientRival": (
        (
            r"OAK: Be patient, {RIVAL}.\n",
            r"You can have one, too!$",
        ),
        (
            r"ОУК: Потерпи, {RIVAL}.\n",
            r"Ты тоже получишь одного!$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_OakWhichOneWillYouChoose": (
        (
            r"OAK: Now, {PLAYER}.\p",
            r"Inside those three POKé BALLS are\n",
            r"POKéMON.\p",
            r"Which one will you choose for\n",
            r"yourself?$",
        ),
        (
            r"ОУК: Итак, {PLAYER}.\p",
            r"В этих трёх ПОКЕБОЛАХ\n",
            r"находятся ПОКЕМОНЫ.\p",
            r"Кого из них ты выберешь\n",
            r"себе?$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_OakHeyDontGoAwayYet": (
        (
            r"OAK: Hey!\n",
            r"Don't go away yet!$",
        ),
        (
            r"ОУК: Эй!\n",
            r"Пока не уходи!$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_OakChoosingCharmander": (
        (
            r"Ah! CHARMANDER is your choice.\n",
            r"You should raise it patiently.\p",
            r"So, {PLAYER}, you're claiming the\n",
            r"FIRE POKéMON CHARMANDER?$",
        ),
        (
            r"А! Ты выбираешь CHARMANDER.\n",
            r"Расти с ним терпеливо.\p",
            r"Итак, {PLAYER}, ты берёшь\n",
            r"огненного ПОКЕМОНА CHARMANDER?$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_OakChoosingSquirtle": (
        (
            r"Hm! SQUIRTLE is your choice.\n",
            r"It's one worth raising.\p",
            r"So, {PLAYER}, you've decided on the\n",
            r"WATER POKéMON SQUIRTLE?$",
        ),
        (
            r"Хм! Ты выбираешь SQUIRTLE.\n",
            r"Его стоит вырастить.\p",
            r"Итак, {PLAYER}, ты берёшь\n",
            r"водного ПОКЕМОНА SQUIRTLE?$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_OakChoosingBulbasaur": (
        (
            r"I see! BULBASAUR is your choice.\n",
            r"It's very easy to raise.\p",
            r"So, {PLAYER}, you want to go with\n",
            r"the GRASS POKéMON BULBASAUR?$",
        ),
        (
            r"Понятно! Ты выбираешь BULBASAUR.\n",
            r"Его легко выращивать.\p",
            r"Итак, {PLAYER}, ты берёшь\n",
            r"травяного ПОКЕМОНА BULBASAUR?$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_OakThisMonIsEnergetic": (
        (
            r"This POKéMON is really quite\n",
            r"energetic!$",
        ),
        (
            r"Этот ПОКЕМОН и правда\n",
            r"очень энергичный!$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_ReceivedMonFromOak": (
        (
            r"{PLAYER} received the {STR_VAR_1}\n",
            r"from PROF. OAK!$",
        ),
        (
            r"{PLAYER} получил {STR_VAR_1}\n",
            r"от ПРОФ. ОУКА!$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_OakCanReachNextTownWithMon": (
        (
            r"OAK: If a wild POKéMON appears,\n",
            r"your POKéMON can battle it.\p",
            r"With it at your side, you should be\n",
            r"able to reach the next town.$",
        ),
        (
            r"ОУК: Если встретишь дикого ПОКЕМОНА,\n",
            r"твой ПОКЕМОН сможет сразиться с ним.\p",
            r"С таким спутником ты сможешь\n",
            r"добраться до следующего города.$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_OakBattleMonForItToGrow": (
        (
            r"OAK: {PLAYER}, raise your young\n",
            r"POKéMON by making it battle.\p",
            r"It has to battle for it to grow.$",
        ),
        (
            r"ОУК: {PLAYER}, тренируй своего\n",
            r"ПОКЕМОНА в сражениях.\p",
            r"Чтобы расти, ему нужно сражаться.$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_ThoseArePokeBalls": (
        (
            r"Those are POKé BALLS.\n",
            r"They contain POKéMON!$",
        ),
        (
            r"Это ПОКЕБОЛЫ.\n",
            r"В них находятся ПОКЕМОНЫ!$",
        ),
    ),
    "PalletTown_ProfessorOaksLab_Text_OaksLastMon": (
        (r"That's PROF. OAK's last POKéMON.$",),
        (r"Это последний ПОКЕМОН ПРОФ. ОУКА.$",),
    ),
}


def render_block(label: str, lines: tuple[str, ...]) -> str:
    return label + "::\n" + "\n".join(f'\t.string "{line}"' for line in lines)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve()
    path = root / "data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc"
    if not path.exists():
        raise RuntimeError(f"missing Oak lab source: {path}")

    text = path.read_text(encoding="utf-8")
    changed = 0
    for label, (english, russian) in BLOCKS.items():
        old = render_block(label, english)
        new = render_block(label, russian)
        old_count = text.count(old)
        new_count = text.count(new)
        if old_count == 1 and new_count == 0:
            text = text.replace(old, new, 1)
            changed += 1
            print(f"[ru-oak-lab] {label}: localized")
        elif old_count == 0 and new_count == 1:
            print(f"[ru-oak-lab] {label}: already localized")
        else:
            raise RuntimeError(
                f"{label}: fail-closed source mismatch old={old_count} new={new_count}"
            )

    path.write_text(text, encoding="utf-8")
    patched = path.read_text(encoding="utf-8")
    forbidden = (
        "I'm fed up with waiting!",
        "There are three POKéMON here.",
        "CHARMANDER is your choice.",
        "Let's check out our POKéMON!",
        "I picked the wrong POKéMON!",
    )
    for phrase in forbidden:
        if phrase in patched:
            raise RuntimeError(f"starter-scene English phrase remained: {phrase!r}")

    audit = {
        "marker": MARKER,
        "starterSceneBlocksLocalized": len(BLOCKS),
        "blocksChangedThisRun": changed,
        "speciesProperNamesEnglish": True,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }
    out = root / "build/qarro_ru_oak_lab_starter_v3_5_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"[{MARKER}] PASS: {len(BLOCKS)} first-visit Oak lab blocks localized; "
        "species names/Ash untouched"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
