#!/usr/bin/env python3
"""Qarro v3.137: translate 50 verified residual FireRed runtime blocks.

Targets exact English-only labels from fresh RU audit #236 at v3.136 candidate
cbe0567814584271aea6bebd12024ab24b18a93e (396 blocks / 119 files).
PalletTown_RivalsHouse and Japanese audit false positives are intentionally
excluded for dedicated handling. Pokemon species, Move names and Ability names
remain English. Gameplay/trainer/reward/inventory/flag logic and Ash Bond/Ash Cap
are untouched.
"""
from __future__ import annotations
import base64,json,re,sys,zlib
from pathlib import Path
MARKER="QARRO_RU_RESIDUAL_RUNTIME_V3_137"
LABEL_RE=re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
FILES=json.loads(zlib.decompress(base64.b85decode('c-qZcdv6n07XK<YX#X_nLLa;0ACx%GgWANh4Tu#|G;3e*D9(&EGlsedDUYS08x|-fZGaFG=u7H$NgSJ)#CE>I^*7q{xHEC=v6D)>QdOl1<2&Q?{GH!9XYQWK8J_XcoKbW?%H$m>r`&>J<z|w$<IRjag<BuFS;s7T?yzZP&s?~Brsq&be&Nl;ZcC@^<xT5WrsP;MH(m0^ZD&-v-kA$$)HmvhdahomRkf*p73~GJqiX8C+Exdu9uaC=sF!L(ZK*eK;wAj|<i-t4HPv?e0i4)wFSH+u_E&JrfoiD_Le&L)SW}huJp8|^>Z*a)hi}{{s;BVqnoxW2?0vY{Y%jyda2r44KKwBcKMz!E=uc-NeRRp>4QqD7wsV$r-BEK^I_`vRNmS&w_9A}!F@1)IhXqLAgb&(FBys&B%D>URA3<F~164sCcR--s_R^40?*u#tBm`C9z+rny?V>S2$j2bpy-0^olJ=~ev#o?-xu$K+oF5N$O4q4#<E+VLc_(38W2T$6!9OxLWlfaIhGkqTS+@$L&@;9qO0V`Wh)+?XM<B`LVN~H;km>{cfGfaF{{fewQyvRYzoBYiO1MdFli|OGo0dpLu)9zd0gibOSDK(2Jg$9Tz(+fD|2$lN58v8kFSo#vE9lnOU`4d)I{bb$++~M!dc?9MYL>F?x$~h`=sv^VEElAcv|Vr1@H|%fHO2$V3*G_+!6DDsM<_*A%U5qNwjYAl=)Nk7Nlx9OSVQR>tWX0L0Xx9mcmukyOA|2Gx>`dU)zK(53TZeBM#9q+rx3CgGU);YMr{~lGgKM4bX=7;?G*uj*d`ec1W8v%WA9LEG}|lqkK^)esHa1y%Nxp{9WcWqK|VMD0hU>D!B43i-TM>#yn+nfRI7brG-Kb94hlRVLW47;PFh;7OczbZ^xP}OjGcf;&71NjYW7ZmxU1lqHT71lLyCQm#^XGGK-u!Ry@>8wg0!wvxI$VjgYPP2#R}`iYJeFQIzkik_ZQG+l`I`9TGW`689V71Wx%m9Su`9^=As38(=eT~mhTWV0EDTb<qzTcX#E2=AP2%8<~?4mK^nAB#zPhZ(h4IVE{bS8Ha;?yx(+G=dVw<V1a%0gf+4eoPEmW{WlU5-K(<KkhP2^tf|LEVut^J}oRV%)W<7VpbP9gl1o9uClpq*bZ}FJ>58;~{Xy^7rivDjX8+JK;NCFIgkOlFq!f{;1v_O=Fe;^pcpH&3!-yvk$wt8grZT$b1@mOGY)`v;E<jPM@EQ$IUDK?RZTy>|cQRz4sM!FilBG^RdSJCk3SFB7}$prsWO$yU@fT|mi0k71r>N)E65)xu-SP+0MBL=mXE(*xWZA2r~txATV&?Cb^<jhkktaqyxH*QNSCmnEw#X_G8)h+DYk#f^FJ3TrT)XCSKUoP;^qoi94!6Pb!q|zQi(+lub>n#2cYwALfHH2}LOFHv=%7k(Arej-C(<?(<70X$}b4lucm2=<?q-dg?mRU!7E-JQ;LQu@8eS}Z2_6kY-HmC%(3k(KT(*C{1=GqXZ^N&<Bc2phC>=RfV(38Fb{lRDZfL?T&9{Ca~@eZ<^kn(sTfQ_L6G20P%CkAfkS<?HOEMzG&yTbRGpFFH4)3}yj0DA*haM+Sc-++QuJmhC!4bw5Gi*<tc;C8=owilobgE8PvuyUPl2r04Mu@IF`sUQvZE%`K@HiVsH>L875e#``_<azMxn(5{3l9x%K6@I4RBt%+70D(dd7!whpm;LI50rP-^7>UqQP;JMiCgQP7hJ)geEs61hReUd~E$y#C^GqTn<_*XE8>Ali47>+0>TwA73HW2DNz+lo^b*Fbbb&6WJu^Ey;@BlC$7E>}O7J?E_!SuZi9in$ViHB_afBe9(Y=ibYF#53CSYsgy%o(eYCcZY=<o;TJYlk>?Ch+I!hvk5k~LcLVuou<Cu(@vJW9Cge+5M){6h!g3knMYoJx<JBpk}*6FSi4s4>ypZx8?S1N{S>3>?E46cl5;n^JifRqGAJf|1i0qwz8-Ew4XW8hC>?N={A!r5|_fx$#mq@0vy@DFK1*V_u?!kGRYb2LAv!^#Vx68e|I^;1z!Il)5fVxDD|21|;9AAk00WR;kHN7em@VvFb!HCm#!<R29O)1`|l|Wcxn4wc7$I$Q$|TOd5XWW0vO_RyI63Ll5e%%ye9@JPj?3;pE0jp3lOXK6?RYw3nbdeg}!QNL-H^zK&Qs<a8q_+CtB&4-vv5;sU$)AnF_;hF8$Dp=x|Ka~WF2Q>f8>@Q<a&UuGbUypy%)I`_v?;;)1gCo9o)?hm6x+WbP7-wCM1R?_hD;h-IIj+D4$WDDi4p3t8zP^*q41Y|{$`<QqzTpZG=kAhMb!vP+pVAX2*RS8v$2qN5AtXB~CnxtBT`mcw?sxz^8EIFOZa7}M$EbmK6#!8k8%~V!qO3>aGPNXH>=luzd=Z;)1-MS?`e=O4ym#<7r#4@DZI`NEo-C;3Mq1V76?Ipof4gE*RO>oBZ7*<vsRXFzeBA(sBc7$+$XaK$spwc17NSiU+@-jAn_yqKvQQNV2ULhTB7N9#=^uvjP_&|Gi5ewVINFpYp)2Yj`6si6__Y^=Ig?1)-N!KV+^QiTtuw15gX`2RO{X|UX&0<mJpaQ!iZn|K5Nyq$B5+nWvs>csQ0*VURhK3Gctp*Mz7IdGwEhw@Mi4j+5B3DOQtLPO}Zv|rw<1Vx}*yk?7?`S9xt2h9_s<unEsqml!o=(x);KHpcLj(GQfgGvpRN$z%ZO@K)iE<n`A$w?x2-^aPvV(@+WAq>@i|GLP!KqejKf-G?6WnKn02>e`s`C_+=6^!{Mk6V5JY^!gy}_+($CJBto3@TMq2WQ;bBLQc<4bv^Xj@n9Le{YCX)6ucRvt6T<l?8CK?f8>%Q#fxCYnZ`k9oX;4eWc&tzg2}UP2dBv(%s*n#XwzfolamKOna@Y0AO*%itl1fzj}aCzI6u&=dgB7=fp^5@ctkH)-Z1K>f^UpGL3u6l?C3Eblmeg1QgL>Ocko-bNB4H68stmJu5HR}d`ySxyxk4*W+?+S>o38-YQB+n<5Bh?Kzj!R;Kh*#6bH5AbJ12*S`D<NSL|J-Ij_U{A#z2i~AnmWDTVGgdG?Ic}F69CeMtCAJWI937@1?>8WaYw8VkSx_B+hTMEZoN<%-fzBzCb~tAFo=(gLW&3ug9lPUp+`R3_WE>n3HEv6qd4>mY|I?&g+_>Y~))Z8F8x?tSR&AfvL*92ZGvMMCVOP-@VLq6EqgN?->*!C~OkmKVDGqf4w7MrNAs|DP<J@Nh0Ot4!-k^L@EEuLWnfUX05FCGrv%Zky@$199Qdp+S^^m(T8mRMdK(l_;pnQ7m_vLWx12-uVy=y=<06zBc6J5@R`}^aX0f7@Y{$6%Ws}D8lf0~003d&SMdTD!3LSGj*XXSOf<o7Bh%@QwZ0*|~?&(%+AgSxguqF&fF^K2Zkl83#U2&$2wV$;x<Co=r7MeQA`bIW>pgu}r75E{m__E9}-|8&rH;ph-ghm33<vTV|D)1D)(TV6h6C+ypjx>kQ;^g$#>qLb5~$MoWgAfSb_Ivz|eP?CUWse-SP%;`)jc6lN*i425hD+qwybgW7S+4Vc#R*-ZWqY+{o7}`BK2YIi(7V6Zak2$MsM;4?BTBf8&3qDlsB{htzG~anHv|3HVc3Rr`EvEkoRxpUeT}_XxR0wIG^d1w61DjiF0+XQ1H)&49Z9aqox)s?CFxvP2R<Ij4lkyG(Bcb3#c`ke<ar_7?Y8rC^cpNc$CcG={2ed09yxt_9@&p5|MwJ3|{F>_m?<r^`-9c_pekP#-UBOYvA`!1JS>TVfXLu!<EEr|!T;r+uYxQsSAKH{|LcMqa(EPlMG@XSGeod|Oz<3Shg`*b&kr^L0;Geu);hpQ+1#veub#)|uFCy+H<0IE&se31knNB@iN=xAH`ElFfIVxcu6Q>QTBX0z+m2e>gzu%(ZYt*w~PE;AGpfsu<;Aa!ZIo}gEd`lzMSHx&(cD@Dozn~|*@kft1(^wzG*Lk%w2Ng2yL6G+w6Q6Jk>scyFCnbxrkbuicoQU5n73cz}o4%5ar9>*0jKzI6jB8)o9QxBIB=$QP8fbzZB20_sA5|l$T{Ifk$iamG3_{;9Ja~(I?ssjGFWGquYHD|rNkmlph*^FIhWoqBR<O~C=xr}DWPg!|B#}F74RNjB@)hA;e4bi2e@{YtufDzX;0~I7HCrC>E}OUV-jq9TSf1f}W|o#t+-p<`gKE4nBrX)77WY@WvBJD>5&-aak0+2FLtq?-(n#_VqC?1v>5kpW$HV*Kt~0#br!q4YH7puaV@sUS2oVTTr;x#I(S06rMudh_^a3*VN50fV9*8FF>nQ*g67H7iy@jrsH8#!UY~IFnjaN_L=pUboqkr7V(a#@`znA`69*GTx1hq^pK_%iJ=&+{$A_#Jb1%GRZ`tnpgJ~f^ZpU1A#<ay9HpF8%=>8W^fQlz8P$=F4qp3qAkiyR_s#~rjCMSEaLZef;aWrSJc(|wBe4IDz_F0jT6ucQ1J{0_utr+5eAGac==<CKARVe^U%EKweHY%kCK>jvl8QP2dW%6~}(R}#dVpn>CZr{53Z4Xqzuy15J1-S{WHJwfYRy0AmzC?14GPAhBL^oJq;Gf_E*Sy=2!13~Gf0h*Q(oop`+_a{!LYR3kh_utXcA6$Z?mQetbWqBix1H3wSv}p?XZ0#Zidgx0tXVrJ=Efhd()n4-U<!g;lesm%O-s5#iljkxEdc0J*7}myo(!YPvTkfc1x^B7m4VwURh?G)ZAfxX<{~c~dFg)~tDx5L;yM`T3AD$pA^kV5%>CBl0(>`(I7kW^Scp&s9p{E2ay=LHCF5?(EXp@~pxdUG7%;W%b-UeYNbkIB$cY(XlTpdZxoV&+wg8A<W0b!-aKiFY6yWS5e2DhHScd>t4cDl$LaGrFXwi4xQMj797K}I7J(kS?)9cdTWyv3t8O$5_1;nVUKBQVkqiwwepDRd7FL4wT@E<zXRb-b0(G5)#pU8|D5Gn_t$^;B3o(gpT1Zo2p;;?b*Kdj3R1QH(*{syFGCf&+Sgh5&-zqB!0u(ts3BZ*$Q@9(nJ-1jd#&')).decode("utf-8"))
EXPECTED_TOTAL=50
EXPECTED_PRE_BLOCKS=396
EXPECTED_POST_BLOCKS=346

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
def validate_written(rel,text):
    for n,line in enumerate(text.splitlines(),1):
        if '.string "' in line and line.count('"')<2: die(f"{rel}:{n}: broken string")
    if re.search(r"\\\\[npl]",text): die(f"{rel}: doubled runtime escape")
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
    if total!=EXPECTED_TOTAL: die(f"expected {EXPECTED_TOTAL} blocks, got {total}")
    out=root/"build"/"qarro_ru_residual_runtime_v3_137_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({
        "marker":MARKER,
        "sourceAudit":"RU runtime #236 / v3.136 candidate / cbe0567814584271aea6bebd12024ab24b18a93e",
        "expectedPreEnglishOnlyBlocks":EXPECTED_PRE_BLOCKS,
        "expectedPostEnglishOnlyBlocks":EXPECTED_POST_BLOCKS,
        "translatedBlockCount":total,
        "translatedFileCount":len(by_file),
        "translatedByFile":by_file,
        "translatedLabels":labels,
        "palletRivalsHouseDeferred":True,
        "japaneseAuditFalsePositivesDeferred":True,
        "pokemonSpeciesNamesRemainEnglish":True,
        "moveNamesRemainEnglish":True,
        "abilityNamesRemainEnglish":True,
        "gameplayLogicTouched":False,
        "trainerDataTouched":False,
        "rewardInventoryFlagLogicTouched":False,
        "ashBondTouched":False,
        "ashCapTouched":False
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: localized {total} residual runtime blocks in {len(by_file)} files; Pallet/Japanese/gameplay/trainer/Ash untouched")
    return 0
if __name__=="__main__": raise SystemExit(main())
