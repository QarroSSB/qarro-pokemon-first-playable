#!/usr/bin/env python3
"""Qarro v3.144: translate the five remaining Japanese runtime dialogue blocks.

Built from RU audit #246 after v3.143. The remaining nine audit entries consist
of five actual Japanese runtime messages, three pure STR_VAR_1 dynamic buffers,
and the canonical Mew cry/name. This pass translates only the five real dialogue
messages and intentionally leaves the four non-dialogue/canon entries untouched.
Expected audit surface: 9 -> 4 blocks.
"""
from __future__ import annotations
import base64,json,re,sys,zlib
from pathlib import Path
MARKER="QARRO_RU_RESIDUAL_RUNTIME_V3_144"
LABEL_RE=re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
FILES=json.loads(zlib.decompress(base64.b85decode('c-nnaQES>z6#gsM(8sKzkG_Z#g@S{kqc9Lc(4b+OND{|}2vr%~=r;SX!6@s-9Al45of%p+{R`**qkZ=#t~y-7nB?TU=X~FH&gm(2-P4n8z2hd2?WacDwn~QH=o(tSskb|(ZMkLJZfixS)kwNE$Lx6Sp=s5WOi#HF|JZo$X(wjQvz-@8M(LH0PI9GwhS7KOAMlstCm8)?bW0&!Q$RDC(=t)5c6!I9+>=7NuQFO8zUE`bhj;*p(OUe40Ee`sfDic_afGfY1c;wY08%a~M1_z681Pg2O+GF8fRC$Hi*6AJk#SB_M!!S_nxjU{Po|pyf5T|b=$fC4BC6zxlvA1MUCfA&6C&eAP^9WW>8o3omhG-*q|<xt+kBH&m2}T2o6q#teV(aoV~?!-k@2^n0-;krpg<M+ea6pZOd5i)U_OXlUT1~A_u|9~p#TO5piqTtEuOaAp2>JXHx$Zp6Id7db;?Jy5RNh!{F;KqR$C7gbyt~GRcYGYRz0tKwPwX`8;>w1I|_dY&RIrZ!1fGPR(!<p+suF{KNI!~#Amvs5A+H5E4s*TbxaJ?0!MsW2<5Sih~YndsZ?^7WoYT5mbV?ptlQ4s7VUxEY1-4No%T$kA&DEJLJzF;Ay3#E#>69%@DdO>JB(B;`3R?8QGh&X<X_+M2_}e{6z=aGwp2<h=&o0=JV&=`hL$S+fB5!brM!oF<H#*`TP>mOZXu&32(eI@H4vWS9V76SzM&hJbRqXk?k48&5ajxQ08x%VzW')).decode("utf-8"))
EXPECTED_TOTAL=5
EXPECTED_PRE_BLOCKS=9
EXPECTED_POST_BLOCKS=4

def die(msg): raise SystemExit(f"[{MARKER}] ERROR: {msg}")
def validate(label,tr):
    if not tr.endswith("$"): die(f"{label}: missing $")
    if "\n" in tr or "\r" in tr: die(f"{label}: physical newline")
    if any(c in tr for c in ("—","–","“","”","’","…","«","»")): die(f"{label}: unsupported punctuation")
    if "\\\\" in tr: die(f"{label}: doubled runtime backslash")
    if not re.search(r"[А-Яа-яЁё]",tr): die(f"{label}: expected Cyrillic")
    for seg in re.split(r"\\[npl]",tr[:-1]):
        if len(seg)>35: die(f"{label}: segment too long {len(seg)}: {seg!r}")
def bounds(text,label):
    ms=list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$",text))
    if len(ms)!=1: die(f"{label}: expected one label, got {len(ms)}")
    start=ms[0].start(); nxt=LABEL_RE.search(text,ms[0].end()); end=nxt.start() if nxt else len(text)
    return start,end,text[start:end]
def replace(text,label,tr):
    start,end,old=bounds(text,label)
    if re.search(r"[А-Яа-яЁё]",old): die(f"{label}: already Cyrillic")
    if ".string " not in old: die(f"{label}: not text block")
    safe=tr.replace('"','\\\"')
    return text[:start]+f'{label}::\n\t.string "{safe}"\n\n'+text[end:]
def main():
    if len(sys.argv)!=2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>",file=sys.stderr); return 2
    root=Path(sys.argv[1]).resolve(); total=0; labels=[]; by_file={}
    for rel,patches in FILES.items():
        path=root/rel
        if not path.is_file(): die(f"missing target: {rel}")
        text=path.read_text(encoding="utf-8")
        for label,tr in patches.items():
            validate(label,tr); text=replace(text,label,tr); labels.append(label)
        path.write_text(text,encoding="utf-8"); total+=len(patches); by_file[rel]=len(patches)
    if total!=EXPECTED_TOTAL: die(f"expected {EXPECTED_TOTAL} labels, got {total}")
    out=root/"build"/"qarro_ru_residual_runtime_v3_144_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({
      "marker":MARKER,
      "sourceAudit":"RU runtime #246",
      "expectedPreEnglishOnlyBlocks":EXPECTED_PRE_BLOCKS,
      "expectedPostEnglishOnlyBlocks":EXPECTED_POST_BLOCKS,
      "translatedLabels":labels,
      "translatedByFile":by_file,
      "pureDynamicStrVarEntriesLeft":3,
      "canonicalMewEntryLeft":1,
      "gameplayLogicTouched":False,
      "trainerDataTouched":False,
      "rewardInventoryFlagLogicTouched":False,
      "ashBondTouched":False,
      "ashCapTouched":False
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {total} Japanese runtime dialogue blocks; expected audit {EXPECTED_PRE_BLOCKS} -> {EXPECTED_POST_BLOCKS}")
    return 0
if __name__=="__main__": raise SystemExit(main())
