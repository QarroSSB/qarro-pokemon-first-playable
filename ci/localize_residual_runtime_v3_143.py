#!/usr/bin/env python3
"""Qarro v3.143: close verified ordinary RU residuals plus Pallet Daisy text.

Built from fresh RU runtime audit #244 after v3.140-142. Translates 84 ordinary
unique text labels plus the conditional Daisy grooming result label whose three
audit branches share one label. Expected audit reduction: 87 blocks, 96 -> 9.
Five Japanese-runtime entries, three pure STR_VAR_1 dynamic entries and the
canonical Mew cry/name entry are intentionally left for dedicated assessment.
Pokemon species, Move and Ability names remain English by project canon.
Gameplay/trainer/reward/inventory/flag logic and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations
import base64,json,re,subprocess,sys,zlib
from pathlib import Path
MARKER="QARRO_RU_RESIDUAL_RUNTIME_V3_143"
LABEL_RE=re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
FILES=json.loads(zlib.decompress(base64.b85decode('c-pO6>uwWS5`L8q+MgyU24+V2gPhn-JUExN15s8;*1<lBTiD%JcRRsCNVyCP2$lqv%rIe+ET9>7HLE2z56=A+PQSuD$yU`lj@x#(?Pcdre5-TnUiDRV9$d;Xhg~VMl6_^86$;#$G8c?YN}p#1d(<r3JQKGHb64!FrI#GLUpKOs1|M7sAf4j(olH`{$H(}TIbxY+am+L>4PJ^y66u*iO>Dc1q9*o4)m;v04<?h5nON#!-<>;#*bqD7NQ0ku#AgjC&cq&ksEQMJwg1kYlK7;#OYr5cs1ePv*m0NK=RoN`6X)>dGJJ3!!?!Q`@w%VI8GNd`Pw;CvsEHGC3g-`R;ALClFoa*90M#;zL}%U;+e45N2sXsJ_z7M&H8@vQr}y!qeRt7a6`#c^a6Tm2Jj~$QRSoEg@*J;LzpUK&)1^>HvyHJzBF%YRw``}yYF>H7ubMb^Ux;0I)m_%yWnczxL#RL%R5}(lvLaY#S(yc19)Y&%7+Ll?nW+S~?MNv>!K%C1@JR@y2g)P({Wqx@GC(U-@fV;aW09K8;;nU6bUI&|Hp_(^C^^a;K4X^C=2$tK2aUm$C;k2X8r(&k(DcVBF-UTzxqkzl&;#_%8Ce$;B;CP1a1eFcmfnEKSwZvo`4kSoFBEV~p!>1=9M4}EQ<Kc4xqwAijfPPj!%3R+sLhyZanxl?oNDe0+D}~w;YQY6_S}u}so0`a4RNZXO6mkeCHVKT^71jJ6xv`H4t<uMBztrdJ8FW=kgU@XdCo|IS=^2|pa2N(iG!01SHK@izC99rNk!ce84_eXMWUUC6}<`OF4uiS@dk+umI0-9-DlDUOL!Q<Q2Med;SPv=ku1_prE$}Vv!Y(mnKi9Dc~EACJ9TG(VV>4ip=z=Re}R?CRH`MQ$&pe)Ip7^?g~rCBqscREIq4(zsdCR5=?i|xiqTbp1VoW}&%VvA$|x(9Di^Y&aQhG&t6+~BhLDW%Q!-w2ECA&RiT*tbjYa7}DselKe5f+0E?*T3ZB5=s6>wc94M~lGh-Ba)ss-)}Frk1&&-WBt<DBOrMuqx-Zp@)7n=*<pD^8^lHB9Z+dbtED?14(a?MA(vgB9H;;w&WT&ZLyGOr1l<pdVEO=x$?snpr5)t<sb!16~?gdb)<MGEW<^&=e$6G_u)iDn?cMjdHvSx*dQSQ33eqDaUYQFS7l)tUEkz>D<T_8vbv%8*X2ebw!ntDi)e0jl72S{g4FPrntl8IR@Gt%(l<)vWqF%aHOU}L7en;6Ac3sY&NcEdBPYsr}QHCG^r*R;k}sJOO*X*D9(Ak^-JTZ7P%*5Ymvel`b}5+3^T)_fQlHgxjAW_!={+1LHqb5zra#;fJu8%e)rv#3t?oWNms%V@uT=fY;_fYm`~^RY<|L^GQUv|-+Fg!y&Kxc!;lAN#r1ifunWw{Wm4QWEoa2E<~VT31mmr4XGpY({HVDQ)orL7rfxVY<+j{M)KVqFqELXEKzjCc>rmM#aBGI!W0fS!Q9!;{?YHXw6>^~_4#EGg#SS%#GxYsF`hrpu*!2hNKMnogO0v5Z3*^mr)4YY6q#G?35j7=jPR>|^*n6Zf1U8#fL`hg`6rj2I3=}P5P4We}epq)ZnMv~=FPg?MH{hGhK-?b!cc3THzSZaE3YAiMb`~W2HZd}ioSD28j}r`D!5lb;EI!A#eXXL%`^K1I>!y(z3X-6mOeQK{(CvibSf<JkGRNN`6{;G+5p2#_)(FT^fQAAuOUyGP%4a#FHu?iL_{UUv>u8L^zT*`nPved?RJmR0bUI=foKB@6#Rhy;ZX+TFlX<;R&`Vwxi;(J%`VdHB(Oi|@$5MHKjZGssL6sA$P8U(G_ae&mI*QNc!3-e8SY&u~;%00REf49^hp$*EAUC@33-`h=tm41SD-FHhLUJF-aEHqCOjh=DY~)Y`T9{7dEnd$oKYrfdRe6C{X$`TtgdHyz3KUy6Gzn1A!tcZfF!zR7la1z_I?pNDc!$bO+l^5(SH>8PPDF1_kfCZ|o|>q2G0?SM40KKLC>vRC1Yh83XhSd;QTxHhc}{Ub{Tt$?O#n7KYe9x%whx=7N|rgQDFozZ#{;sH<snZv*3;q9$ap%2P4pw!ZAYB;p)vi;z}c+HiqeF3X6RY~?{+e23TDi4E6!|ZxNKQatYmrE7Hhz6Q)~g-myM>4bpkO9!43pBt<v1qEj_0*sbg^K@*yK>(k0F;b77nnIlV<oq$gvM)WozV-r(RrsL|&cjGd0RTpUFkzL)dKWt#oqO{>_$yufnGGf`e*mQw^%q#c;rf}Gjqh!lid^MH(C6vQR~0u5lLe+S}h0kWX1*b*<{i?@&_--Cj$!0emw`l(Gmt6bnp(~(LsK%y2R>0mGr^MpE902R=3;5kC%2oMcIo#3ATHOaEKTyM6Fu4-g!GplYG>@Kr9RFoDHRRT=-oHVodc&-jDs43Np2!4QBo%(gi_X^c^02s&;xCUn4690hL_w@P(;b8N;wk2M5Zn;-`>bP~^4_T}N@zJo^2lu-^g}49%u1Z|=l#CV%x+JX^y;rP>!^`b;C}ox%em#?hmwXI5JTtQXS?5bAJBAJ@(T0KFQ~=Sll<T{Ii3hZK*}37z|0@`?tzP)I68=H_zs|&<hIMD(LiY!8|0Xldd*R+f_y2QG^LcL61K(o0!7Uh30C4*EfB<5W!~0Dn&l#oOD@c-c$d`3U!Z*+gAO!yjx$+51Dt^03zf$Uiy4)XSmTop;nU=Q)IGf|rwjFwV>+7&-<ZxY}my0&`@!75wx&4F$t~U*HAvVvgij!B?233B*6{Yx(2HL(8>j5~U7aZ0M!=@@QBYE@x5dkppDHY*8@~B*O982I0UEZI0xCe|AZh|;TR%Djf+80xQRc;QJ$@q<3Ber(AW?5D>$@ktUTksU5Z6*6Y9_<UB>5?Yk3pUR?p!i^FrO$%hS_*N2L4W#auydah(rrUXNw~_$Q7jq~CiqL>M<-EP`L0QG{qU`!iE%{l8}4%$8gb*Y?>nnC#=s8z+NtEaQqP%C9)R6=B07<ZjQ{@Q@*t+(nY(hCRy8ZKWpq5A)}6);A-U5&z>?D5rBm2wol!jpQ$F;qfHv1orB)w+ZNd$|d_>@U<6_%_E5m*HbOyfMq?(4pce-t$wP)7nH88g-gP1s-;CL|dY^RcVLC?(*?w(9UM+kOrfMe0YM*xs~Tzs2bxKj4sbk!f~`VoE^&laH5z&M%M{Svoy1fZBQy#TG?!)j-qu%}FONOplu)r+<o`$jcDw$H6`m<K!HJ<rc-foSmp*X0}}!QPhmNlQ+oV#!#-uh$NI)xo{Z6vQD;BL!R?r#V7p?+e`Mb}sc__fYD;R;4~~7MTYhZ@G`;;!D)(tJ%+3GTPgmPk4lTjiY*>$-^AkaF)kO-o0MO^Ts{3@qP!6-JxQ!+wR)idKSi;O3GxppsA>Zgzit7=x$Hz|InB~aB{%a%M%=N-6e(S{cag&(9fG1T1$OV^MD_MPjWU_<~Us!OJD&zFiASm%Y6sCH(6j68s_9S-Tkg#n~2;TY&^Q|JVk_inj-2Cu4wPC9#^e5o>Vm+g!@eo>WQj3EgwNryVRhhEMGjk!S;{O=sr_`EV-+`s5Ts&V&VF5IalD0V`I0Lcwk-piy+~e7EO#KV^dR|w>DRM+1jXj8Lbq&OPj_%Z@W1Vy7aeeJ@vP10sZYAZ3p-80Rrw0e<Sd-r2Nq7j;pO>och!C;6T&Z-M+hMIUDXty|9-<5Gd~qM#DXT(R!G$0{2gU_2l%3*6@$z^F?3Q`hC?kMl8;aNfz*Az>iKY-dVO#@kGx{M6OVhpU7GKj20lfm=r#^0w$Ng00PXYWqtszXrYqOk={ov&XDOZG%>xWJ;Yn_ZyGyj{-A%7Ak6K5O$w&QmJSJj-ox8p#m{)sr%is-Jn0U^J2cF8T4Ec!p9P*{#Ptmni#>V_TI*mTyr!Fdh~^8_@?1eHgl>E!QE!Yw0SD1@Vfm1Qe58egg~HLkn@mLW1-iHIhyI6E)D+J(6(8RPQh1<)RhubPS2tL}bMHsFl~d)cjXYiA5LuSrF6-fc0Sa-YzW')).decode("utf-8"))
EXPECTED_GENERIC=84
EXPECTED_AUDIT_REDUCTION=87
EXPECTED_PRE_BLOCKS=96
EXPECTED_POST_BLOCKS=9
PALLET="data/maps/PalletTown_RivalsHouse_Frlg/scripts.inc"
SPECIAL_LABEL="PalletTown_RivalsHouse_Text_ThereYouGoAllDone"
SPECIAL_BLOCK='PalletTown_RivalsHouse_Text_ThereYouGoAllDone::\n#ifdef BUGFIX @ The localizers missed what should be a textcolor change in the localizations.\n\t.string "{COLOR DARK_GRAY}{STR_VAR_1} выглядит очень довольным.\\p"\n\t.string "{COLOR RED}DAISY: Вот и все! Готово.\\n"\n#else @ In the JP games, gender-based text used a different font instead of different colors.\n\t.string "{FONT_NORMAL}{STR_VAR_1} выглядит очень довольным.\\p"\n\t.string "{FONT_FEMALE}DAISY: Вот и все! Готово.\\n"\n#endif\n\t.string "Видишь? Выглядит отлично!\\p"\n\t.string "Хи-хи...\\n"\n\t.string "Какой милый ПОКЕМОН.$"\n'

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
    safe=tr.replace('"','\\"')
    return text[:start]+f'{label}::\n\t.string "{safe}"\n\n'+text[end:]
def validate_written(rel,text):
    for n,line in enumerate(text.splitlines(),1):
        if '.string "' in line and line.count('"')<2: die(f"{rel}:{n}: broken string")
    if re.search(r"\\\\[npl]",text): die(f"{rel}: doubled runtime escape")
def patch_special(root):
    path=root/PALLET
    text=path.read_text(encoding="utf-8")
    start,end,old=bounds(text,SPECIAL_LABEL)
    if "#ifdef BUGFIX" not in old or "#else" not in old or "#endif" not in old:
        die("Pallet special label lost expected BUGFIX conditional")
    if old.count("looks dreamily content") != 2:
        die("Pallet special label expected two conditional English branches")
    if "See? Doesn't it look nice?" not in old:
        die("Pallet special label common tail anchor missing")
    if re.search(r"[А-Яа-яЁё]",old):
        die("Pallet special label already Cyrillic")
    new=text[:start]+SPECIAL_BLOCK+"\n"+text[end:]
    validate_written(Path(PALLET),new)
    path.write_text(new,encoding="utf-8")
def main():
    if len(sys.argv)!=2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>",file=sys.stderr); return 2
    root=Path(sys.argv[1]).resolve(); total=0; by_file={}; labels=[]
    for rel,patches in FILES.items():
        path=root/rel
        if not path.is_file(): die(f"missing target: {rel}")
        text=path.read_text(encoding="utf-8")
        for label,tr in patches.items():
            validate(label,tr); text=replace(text,label,tr); labels.append(label)
        validate_written(Path(rel),text); path.write_text(text,encoding="utf-8")
        by_file[rel]=len(patches); total+=len(patches)
    if total!=EXPECTED_GENERIC: die(f"expected {EXPECTED_GENERIC} generic labels, got {total}")
    patch_special(root)
    out=root/"build"/"qarro_ru_residual_runtime_v3_143_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({
        "marker":MARKER,
        "sourceAudit":"RU runtime #244",
        "expectedPreEnglishOnlyBlocks":EXPECTED_PRE_BLOCKS,
        "expectedPostEnglishOnlyBlocks":EXPECTED_POST_BLOCKS,
        "expectedAuditReduction":EXPECTED_AUDIT_REDUCTION,
        "translatedGenericLabelCount":total,
        "translatedConditionalLabelCount":1,
        "translatedFileCount":len(set(by_file)|{PALLET}),
        "translatedByFile":by_file,
        "translatedLabels":labels+[SPECIAL_LABEL],
        "deferredJapaneseRuntimeEntries":5,
        "deferredPureDynamicStrVarEntries":3,
        "deferredCanonicalMewEntry":1,
        "pokemonSpeciesNamesRemainEnglish":True,
        "moveNamesRemainEnglish":True,
        "abilityNamesRemainEnglish":True,
        "gameplayLogicTouched":False,
        "trainerDataTouched":False,
        "rewardInventoryFlagLogicTouched":False,
        "ashBondTouched":False,
        "ashCapTouched":False
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: translated {total} ordinary labels + Pallet conditional block; expected audit {EXPECTED_PRE_BLOCKS} -> {EXPECTED_POST_BLOCKS}")
    next_script = Path(__file__).resolve().with_name("localize_residual_runtime_v3_144.py")
    if not next_script.is_file():
        die(f"missing chained localization pass: {next_script.name}")
    subprocess.run([sys.executable, str(next_script), str(root)], check=True)
    print(f"[{MARKER}] CHAIN PASS: applied {next_script.name}")
    return 0
if __name__=="__main__": raise SystemExit(main())
