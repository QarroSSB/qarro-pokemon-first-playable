#!/usr/bin/env python3
"""Qarro v3.139: translate 50 verified residual FireRed runtime blocks.

Prepared from fresh RU audit #238 after excluding the 50 labels reserved by
v3.138. Expected effective sequence: v3.138 346 -> 296, then v3.139 296 -> 246.
PalletTown_RivalsHouse and Japanese audit false positives are intentionally
excluded. Pokemon species, Move names and Ability names remain English.
Gameplay/trainer/reward/inventory/flag logic and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations
import base64,json,re,sys,zlib
from pathlib import Path
MARKER="QARRO_RU_RESIDUAL_RUNTIME_V3_139"
LABEL_RE=re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
FILES=json.loads(zlib.decompress(base64.b85decode('c-oa(Yf~Fn68$TKYd-=hT;6=}7ndZ!kOf0Y+ECs~6*ZAAXo}HXc4lOvxLm~}j!A_LjyJ9l{D`sFajKGC#6w011Ak%WAMNSBcl3VX4@T1Hj;6cs>C>nC`u?@7>6@SA&1LVC8AnWdw&`T&CuG4BBlF{~z4(cjajj+F8@8OxwVU^^wJl1Eul)Hb)AQ3-UQGLA`7eb#<`$NHk-c{FTJTd)3QmpSGPnqi!;RoWPzu+>t>NKeBiO~Yqu@9w8NvIYY)q$zjj`$YSn`W6oS+h%1cyO6T*Zn~a2BqG+eUE6zZ0$nXF(bFonzIhfhDEj<knxVJs528C6$Ufj+jrF%f4wj-ps;+l@T2s>b#P@nvg4LnUKyu3&Kqa)3Y*5j_^EkYZni#Dz^^Um<qXNz`u)d6&6;*jqnEp-(9e=C&4*8O|I<*kAq)>o!~WIUl`#dx)r}x4%dzFU-*>`BdD@(N8!dmt6SopaCH3BF6<R<TCNDUvuE8FvvZACQr4nFUi}D@eh*#*`v$Cg6+Fe;r+9rCJTZoh;7RZnZ+{{menr$PaJGU?3BQMX7s26R(@m|GYh=uiedP<+lASGXTcp4x7fol<@m;9^RSr&phjly|F%G|D6wn7mx{5%a!&ZEI5v~uy)bJ6#H(CINU@J&fa1%K}%ZJp9f#8?0E$6gqxW$cGxg_$^nKm8IlFt0dct=0lSFt0X$(-ZKx+{-|g3=J>#{fbXeoyEr11Q^UL2wC=82kei@%^S83eE-%?HN45otL~JC!7q`K1Ro{W_3I=d-7gG`2QP)^BA^LW^TdQ3#2a@&)b4;k8ypQtUkk%14;=>dw#716{P+ied3#|w4SWLpqttLbG5rcsTD&B;TCLRItj}!&TDHE!U0ygZA9-o*t@u8+X-pgBIA2W(-qUw;S7Ic#3!ewRMgMNM*~^=650DSc#hW>loh-)FM&9?{vE}jLUcrQP(@ZhG(ZHz4;6L`XlirFavbwZ)743;4V*H+L<TG)1M)C6DP_L1Z&$rprMtN#Jfi5^a$LG|roBW?J|~m|Za~$0<s&|0C(oIhFDR{6`9hf(iQRo1Ar4Eb#N91-@Lm#k5e7I@x8e5SN1B@y8DZTMS?tEREAyi=<4YG7-=Cd|-5pCl(E9=gctkmD+)t&G^Pk6(^CJ()NKWHpvQWdW)S46H_;qc{oC!R@kfLijey(GzyRT+zW486RsHMoylpF9H<p6dN!4R8(Cd&rwrRoK?#6`{!P8DWRP7-3XL&^dAz60WhJJ&gYnPT_XUKOskMw#sTxq>??7KG`O(QktfV4)Y-%R?@)m%1#Sv*o7>*9VLPM3s^7hG-TSVJHLr5Pty$LouhpJVkF;2Ra*lT^V$}m(jH~Z1kvUi&^RUantv0L1sU}?>}N%ui#n0<1KOms3hh&RgWixUl65IIoM#W!Pq!s%wz2VJUpW}C&Zq#R#oM2i_qH^a&y6St$#>ZHzz!Ts^_y7>g-3$Y9%bJC6S$yzBg)R9X}<AbSCFaM{A~iqamTfheZ1X@<D@Bl((fyT*Ju=j}A2*pV6+=a#^M02bJN?KziKjQ+h>ecz5!l{;l2xXHmH0kbH@P>mqH*=9hTH<6w_a3LNc0-#iQcWXwJ#UGOw`$I4(Qc*@v$g^(Xm{ZJfIAp~Ko!f$vVkJMHWl`ydq2AM=!EQuG2MA?(R$a@pQ70QrH<kGr^ZKEWiA3aw@e3PJ1V`_@xIwxfbCPdtZI9}qy4+Q0tD5VE_=HK-z<e!EzF4YKQUl$5469h!kfm}e^34jb=Q_M`+ruUdD3`eNr!xC=6@+@aD=E{PTos+K3IC~CX!!?6_1K5?GgY2NR4mWi<Ct-!GrcFEKu&k0UA&W^)t*Z*4O}?P)Z_2#heD&!S;`M30e#KHb>H3s!WIZb;QlCd$X-I-^f^&&tIYkcP0yHXX?ziAHq6u2iTCj+tK?lgQb8<c0y491eKD`26X`6LVG3mut77DgqOre2L%|lZMu*S0Wq)FA0iPQ;PQnero7_LbTW~&y)J&0N&0(}R<T5#n@sHUDbuxGbjx#H)ND21S~g$3cpi>YOiu>?z}JtEPXq}wv0w*-?7-LR3V1aQS&aE057R<t)((3)y*Bd?q*L@)Yk_+ANGejgXMbQZm|{5u={3$%Fn5G@zjD?;;;60;=9)fM7`NT_O?FLmuHQ7OkJyr;^c6#NIpS*?%1D+~7^!~DtovWs>S(jwBFdy0psYdqz&j5-}I#^p$Dt6aR~(nq=)@Yjt{8`J;Mo#{W5MWFJwnHLG^I$e6m9?RL6S*UAIATL*@1^kK&uuMWqTfu<z*`{uAepPyr;uFbbg#_x-_?s%bt<)vc3<u-1y$i6-tVU;#K}CmUY;np)-AxK%Pde$G7?p*^oYFsKY`^{ka~~tQn9z7&QR}eIdHc7+bvByhCuQj|>mso6KzEgyl$j;r&!Jr9x{8G!%T?M5e+u$vN|?Zmh;zMrr>lU{VuSz=E_BciEPbSg4?$&6$>N9_w;Gzw!${0uwDa|>SV7)%5N{Vd_aQAyRLgFe`MS1z$EAIpb%81x7hFq#@gov9G+bbnqPq>GxEhuGH{!x$4t*v3mMDaD@|tQj!TYR~Ing>90!+Fhku&ql)1=!i)2>f%xc@imEp@A?WlBEg46D+@cbrv3+^nHG^@A<ZOUi;Tu8+*$LD}luSTwI-ljqE=Xw>Bjl7q%{?Dpi}V#!%u`iGPb3@R-85FZjO$GRcYfn^a3xDFCTOI_+({3_xl-Yh643ZmE|#96>~QY=7Pq^V9-pq0&sdRo>&B-AzYnE5dZn^#ApyJ^!YLSF*`3DeKyYK5s`>`*re>9ViX#0M@pdgfT`B@eZGb!A33E2T;O5KFI4h9pc7j1L4lo+!p_dyY1GC1<Iq?Kc@=Bqm~aQe$@+h_8XdOHQ0E{dm<q^2CbJ8A()i0ot@X)prkG>lzh2d=}Z6d&0%nY0D{27rdN{-S?V0a3!3`ZoC{4@}7e>pRwHj6ByVD-WtKbp}%)%u&B43sv9%UaI>E8`1lz|#I42X>D?Z#+9N2V9|1S&I)2CNFSSQ^cyLpgKDTJLP)tfQ+f5L)EKw5*Np{Pch<^eb-iI55s(_JXW7)Ggtb|Ri_zkN0;#xBlD|*I)`qHc3jf!Q{^=VX+f<de|`_;Y<x3K-=wv@HO?=!Asn;lvqJ)dY92NOcCkKZ)#=?~8G-L@q?DxvU@1h=KTD6r{0z}fE}-2;Mw+_<?ITV58X3q2PX<51gbR{R8}kXgSm9)E$wyGlC0XCmUUR`>%Cir0Dau}wwl4UoJ`41cM*nA#AK)|dK>SFeB6OgQE`mT2e%6?=bBBQ(WG2Wot(rV#_Rx=7~*T+V5ulwPF%Yslc~4YduMj5J-yj<}dr+s#)>W5UWJvIu7v^V?VHMxfyMHS;L}_ejMyv@|zchSLPDNcJl&s|Pp`Dn@E@YIed%C1z&FhI?158&|1TH?$fN(lOm^!+=hW0niQB8?GZIN)XI#R{7Cc&NjIcKIB6w3iv9gu>#I^_^@ptVA;#LgzVZ{)xTE7Uf3C#7qe&t5LyalT*6dMcL1;&3+Q5{K&!HoPSF&#5War~x_{#Id(DFGM8TWiaFckfhKhs}YS%|b#)o_GOhSU%@|I&2@*YKUq5BlN?_J7I%M~`7omdt<v2dqE#xJOO4b_WX<mV27|7F{xDtJpy?jRdhN&BrC(JvYLr#eZl8{M_mjc6ibd0w$G?--;s^`MeMA)@oh>6w{3231!E0YXm395I{^q7JtIjJB=|bQ|4A#^_b5!J-y1<%7c0GLaLRC7R(YErUnlv9Ft%_YGP2f-y?toK!lNOh+K6(LpqzS7%}R)UvL-dyEcxDzKJSQMclAJGflTm_G5}sAOJ7df!dN(t47qDCz_2n35*AeM5_zGde{r6KZ$C%DX_zoBqShhK73<Rip1vfETIBfNdvC+eTwJD{U(yT2JYAht!Dz7x`PtR6fhzZ#W25bDIm6W#3YH>2vIJg~OeOu|-s}iD_T!!&#oUzTkABBivVNR&=BbmY#$jDMf;Ii*zdon}-I3VIs7%h#^|6t)KX(T{Qbh+qf_@xjz3ppn0t-b$Qb@Ybp1PXC<6egSFEnKFuL^+g9f%Jf1()#TP7GJ3{9PI8E}^Tt=a~Ok)G)I~0~aW$wn6%G`~{GB?s-dnNovO?mVb<3M)}Xl`$*Hj*nH50D78{|nxM-6&a~VXOW_qrY1{&h}Ln5q*yIJ=$+vt0x>5T8=pI{k2dN-?;orN!0rMHX6~v@@mutm(^I~j3)|JeXh>^dYPBD9W2+kyAK$c$&>)PBYeeg5s+VTJHJUYY!q7_XYxS1+j;9Akskg%Q7Zp8RrP4R-?kp+KKMV>=$8}')).decode("utf-8"))
EXPECTED_TOTAL=50
EXPECTED_PRE_BLOCKS=296
EXPECTED_POST_BLOCKS=246

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
    out=root/"build"/"qarro_ru_residual_runtime_v3_139_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({
        "marker":MARKER,
        "sourceAudit":"RU runtime #238 / after reserved v3.138 set",
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
