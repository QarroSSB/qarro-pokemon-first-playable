#!/usr/bin/env python3
"""Qarro v3.95 bulk Russian localization: Kindle Road + Pattern Bush.

Translates all English-only FireRed runtime _Text_ blocks reported by the
current surface audit in two untouched Sevii-area map scripts: 43 + 36 = 79.
Pokemon species, Move and Ability proper names remain English by project canon.
Ash Bond / Ash Cap and gameplay logic are untouched.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKER = "QARRO_RU_KINDLEROAD_PATTERNBUSH_V3_95"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")

FILES = {
    Path("data/maps/OneIsland_KindleRoad_Frlg/scripts.inc"): {
        "OneIsland_KindleRoad_Text_MariaIntro": "Какая чудесная погода!\\nИдеально для боя!$",
        "OneIsland_KindleRoad_Text_MariaDefeat": "Ай-и-и-и!$",
        "OneIsland_KindleRoad_Text_MariaPostBattle": "Только не брызгай мне в лицо!\\nВесь макияж испортишь.$",
        "OneIsland_KindleRoad_Text_AbigailIntro": "Кажется, я начинаю обгорать на солнце...$",
        "OneIsland_KindleRoad_Text_AbigailDefeat": "Ох, какой же ты ужасный.$",
        "OneIsland_KindleRoad_Text_AbigailPostBattle": "Мне нравится твоя кепка.\\nМожет, мне тоже такую носить...$",
        "OneIsland_KindleRoad_Text_FinnIntro": "Отсюда видно, как ГОРА ЭМБЕР\\nвозвышается до самого неба.$",
        "OneIsland_KindleRoad_Text_FinnDefeat": "Ну и крепкий же ты!$",
        "OneIsland_KindleRoad_Text_FinnPostBattle": "Здесь небо кажется\\nпросто бескрайним.$",
        "OneIsland_KindleRoad_Text_GarrettIntro": "Я сделал перерыв в плавании,\\nи тут ты вызываешь меня на бой?$",
        "OneIsland_KindleRoad_Text_GarrettDefeat": "Эй, что за...\\nА ты хорош!$",
        "OneIsland_KindleRoad_Text_GarrettPostBattle": "Не стоит всё время пользоваться SURF.\\nИногда полезно и самому поплавать.$",
        "OneIsland_KindleRoad_Text_TommyIntro": "Стой! Подожди секунду!\\nКажется, у меня клюнула крупная рыбина!$",
        "OneIsland_KindleRoad_Text_TommyDefeat": "Я снова всё потерял...$",
        "OneIsland_KindleRoad_Text_TommyPostBattle": "Мало того что я проиграл,\\nтак ещё и крупная рыбина сорвалась!$",
        "OneIsland_KindleRoad_Text_SharonIntro": "Поможешь мне немного\\nпотренироваться?$",
        "OneIsland_KindleRoad_Text_SharonDefeat": "Ты оказался на голову выше.$",
        "OneIsland_KindleRoad_Text_SharonPostBattle": "Сразу видно, что ты умелый ТРЕНЕР.\\nТы мне нравишься!$",
        "OneIsland_KindleRoad_Text_TanyaIntro": "Не проходит и дня,\\nчтобы мы не тренировались!$",
        "OneIsland_KindleRoad_Text_TanyaDefeat": "Какая же я глупая!$",
        "OneIsland_KindleRoad_Text_TanyaPostBattle": "Теперь я буду тренироваться ещё усерднее!$",
        "OneIsland_KindleRoad_Text_SheaIntro": "Каждое утро перед завтраком\\nя проплываю вокруг этого острова.$",
        "OneIsland_KindleRoad_Text_SheaDefeat": "Фух...\\nФух...$",
        "OneIsland_KindleRoad_Text_SheaPostBattle": "Я проиграл, потому что вымотался\\nпосле всей этой беготни...$",
        "OneIsland_KindleRoad_Text_HughIntro": "Одевайся для боя как следует!\\nСними этот легкомысленный наряд!$",
        "OneIsland_KindleRoad_Text_HughDefeat": "Почему я?!$",
        "OneIsland_KindleRoad_Text_HughPostBattle": "Даже мастера боевых искусств\\nтеперь следят за модой...$",
        "OneIsland_KindleRoad_Text_BryceIntro": "Знаешь, на природе любая еда\\nкажется особенно вкусной.$",
        "OneIsland_KindleRoad_Text_BryceDefeat": "Эх, облом!$",
        "OneIsland_KindleRoad_Text_BrycePostBattle": "Вода в вулканических местах\\nочень вкусная.$",
        "OneIsland_KindleRoad_Text_ClaireIntro": "Мы плотно пообедали.\\nМожет, сразишься с нами для разминки?$",
        "OneIsland_KindleRoad_Text_ClaireDefeat": "Я вся вспотела.$",
        "OneIsland_KindleRoad_Text_ClairePostBattle": "И что теперь делать?\\nЯ опять ужасно проголодалась.$",
        "OneIsland_KindleRoad_Text_KiaIntro": "KIA: Мы со старшим братом -\\nневероятная команда!$",
        "OneIsland_KindleRoad_Text_KiaDefeat": "KIA: Что?!\\nНе могу поверить!$",
        "OneIsland_KindleRoad_Text_KiaPostBattle": "KIA: Как вообще кто-то может\\nбыть лучше моего старшего брата?$",
        "OneIsland_KindleRoad_Text_KiaNotEnoughMons": "KIA: Если хочешь сразиться с нами,\\nвозьми с собой хотя бы двух\\lПОКЕМОНОВ.$",
        "OneIsland_KindleRoad_Text_MikIntro": "MIK: Пока KIA рядом,\\nя ничего не боюсь!$",
        "OneIsland_KindleRoad_Text_MikDefeat": "MIK: Ого!\\nЭто уже слишком!$",
        "OneIsland_KindleRoad_Text_MikPostBattle": "MIK: Как могла наша связка\\nс KIA проиграть?$",
        "OneIsland_KindleRoad_Text_MikNotEnoughMons": "MIK: Эй, хочешь сразиться\\nс нами вдвоём?\\pТогда приведи как минимум\\nдвух ПОКЕМОНОВ.$",
        "OneIsland_KindleRoad_Text_RouteSign": "ДОРОГА КИНДЛ\\pПрямо - к ГОРЕ ЭМБЕР.$",
        "OneIsland_KindleRoad_Text_EmberSpaSign": "Разожги огонь в своём сердце!\\nСПА ЭМБЕР$",
    },
    Path("data/maps/SixIsland_PatternBush_Frlg/scripts.inc"): {
        "SixIsland_PatternBush_Text_BethanyIntro": "Интересно, как ты растишь\\nсвоих ПОКЕМОНОВ?$",
        "SixIsland_PatternBush_Text_BethanyDefeat": "Ты растишь ПОКЕМОНОВ\\nс огромной любовью!$",
        "SixIsland_PatternBush_Text_BethanyPostBattle": "Как мама растила тебя с любовью,\\nтак и ты должен растить\\lсвоих ПОКЕМОНОВ.$",
        "SixIsland_PatternBush_Text_AllisonIntro": "Я стараюсь сохранить здесь\\nестественную экосистему ПОКЕМОНОВ.$",
        "SixIsland_PatternBush_Text_AllisonDefeat": "Ох, для такого юного ТРЕНЕРА\\nты просто невероятен!$",
        "SixIsland_PatternBush_Text_AllisonPostBattle": "Я не говорю, что ПОКЕМОНОВ\\nнельзя ловить.\\pЯ лишь хочу, чтобы люди\\nответственно их растили.$",
        "SixIsland_PatternBush_Text_GarretIntro": "Я поймал ПОКЕМОНА-ЖУКА,\\nкоторый живёт только здесь!$",
        "SixIsland_PatternBush_Text_GarretDefeat": "Хе-хе...\\nПравда же, мой ПОКЕМОН крутой?$",
        "SixIsland_PatternBush_Text_GarretPostBattle": "Рядом с ЛЕСОМ УЗОРОВ есть девушка,\\nкоторая измеряет HERACROSS ТРЕНЕРОВ.$",
        "SixIsland_PatternBush_Text_JonahIntro": "Знаешь, мне просто не по себе,\\nесли я не использую ПОКЕМОНОВ-ЖУКОВ.$",
        "SixIsland_PatternBush_Text_JonahDefeat": "Ничего страшного. Поражения - тоже\\nчасть очарования ПОКЕМОНОВ.$",
        "SixIsland_PatternBush_Text_JonahPostBattle": "Кстати, слово ОЧАРОВАНИЕ странное,\\nесли задуматься.\\pХотя ладно. Главное, что\\nПОКЕМОНЫ-ЖУКИ прекрасны!$",
        "SixIsland_PatternBush_Text_VanceIntro": "Да, да, да!\\nПосмотри, сколько здесь ПОКЕМОНОВ-ЖУКОВ!$",
        "SixIsland_PatternBush_Text_VanceDefeat": "Меня победили, пока я ещё\\nпраздновал!$",
        "SixIsland_PatternBush_Text_VancePostBattle": "В следующий раз приведу сюда\\nмладшего брата.$",
        "SixIsland_PatternBush_Text_NashIntro": "Смотри, смотри! На земле\\nкакие-то забавные узоры.$",
        "SixIsland_PatternBush_Text_NashDefeat": "Просто супер!$",
        "SixIsland_PatternBush_Text_NashPostBattle": "Эти забавные узоры на земле...\\pОни похожи на узоры\\nна одежде моего дедушки.$",
        "SixIsland_PatternBush_Text_CordellIntro": "Наверняка думаешь, что я\\nобычный парень, да?$",
        "SixIsland_PatternBush_Text_CordellDefeat": "Наверняка теперь думаешь,\\nчто я слабак, да?$",
        "SixIsland_PatternBush_Text_CordellPostBattle": "Вы, городские, всегда ходите\\nтакие нарядные, в ярких кепках...\\pМожет, отдашь мне свою?$",
        "SixIsland_PatternBush_Text_DaliaIntro": "Сделай глубокий вдох.\\nРазве воздух не чудесный?$",
        "SixIsland_PatternBush_Text_DaliaDefeat": "Если хочешь, я научу тебя\\nправильно дышать.$",
        "SixIsland_PatternBush_Text_DaliaPostBattle": "Сначала выдохни.\\nВыпусти весь воздух.\\pКогда больше не сможешь выдыхать,\\nвдохни чистый воздух!\\pПравда освежает?$",
        "SixIsland_PatternBush_Text_JoanaIntro": "Я обожаю ПОКЕМОНОВ-ЖУКОВ.\\nПоэтому всё время прихожу сюда.\\pНеужели я единственная такая девушка?$",
        "SixIsland_PatternBush_Text_JoanaDefeat": "Я проиграла, но всё равно смеюсь.\\nНеужели я единственная такая девушка?$",
        "SixIsland_PatternBush_Text_JoanaPostBattle": "Я и дальше буду собирать\\nПОКЕМОНОВ-ЖУКОВ.\\pНеужели я единственная такая девушка?$",
        "SixIsland_PatternBush_Text_RileyIntro": "Отличное место.\\nПоставлю палатку здесь.$",
        "SixIsland_PatternBush_Text_RileyDefeat": "Сдался...$",
        "SixIsland_PatternBush_Text_RileyPostBattle": "Буду наблюдать здесь\\nза ночным небом.$",
        "SixIsland_PatternBush_Text_MarcyIntro": "Фу!\\nКажется, меня ужалил жук!$",
        "SixIsland_PatternBush_Text_MarcyDefeat": "Это был не жук.\\nЯ просто поцарапала голень о траву.$",
        "SixIsland_PatternBush_Text_MarcyPostBattle": "Такая маленькая царапина...\\nДа её и слюны хватит залечить!$",
        "SixIsland_PatternBush_Text_LaytonIntro": "Ты заметил здесь\\nчто-нибудь странное?$",
        "SixIsland_PatternBush_Text_LaytonDefeat": "Ты хорошо посмотрел\\nсебе под ноги?$",
        "SixIsland_PatternBush_Text_LaytonPostBattle": "В ЛЕСУ УЗОРОВ есть места,\\nгде трава совсем не растёт.\\pЧто могло вызвать\\nтакое явление?$",
    },
}


def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")


def asm_quote(text: str) -> str:
    return text.replace('"', '\\"')


def replace_block(text: str, label: str, translated: str) -> str:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        die(f"{label}: expected exactly one label, got {len(matches)}")
    match = matches[0]
    next_label = LABEL_RE.search(text, match.end())
    end = next_label.start() if next_label else len(text)
    old = text[match.start():end]
    if re.search(r"[А-Яа-яЁё]", old):
        die(f"{label}: block already contains Cyrillic; refusing to overwrite")
    block = f'{label}::\n\t.string "{asm_quote(translated)}"\n\n'
    return text[:match.start()] + block + text[end:]


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    total = 0
    changed = []
    for rel, translations in FILES.items():
        path = root / rel
        if not path.is_file():
            die(f"missing FireRed map script {rel}")
        text = path.read_text(encoding="utf-8")
        for label, translated in translations.items():
            text = replace_block(text, label, translated)
            total += 1
        path.write_text(text, encoding="utf-8")
        changed.append(str(rel))
    if total != 79:
        die(f"expected 79 translated blocks, got {total}")
    out = root / "build/qarro_ru_kindleroad_patternbush_v3_95_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "translatedRuntimeBlocks": total,
        "changedFiles": changed,
        "pokemonMoveAbilityProperNamesStayEnglish": True,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {total} runtime blocks across Kindle Road + Pattern Bush")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
