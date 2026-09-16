#!/usr/bin/env python3
"""Qarro v3.138: translate 50 verified residual FireRed runtime blocks.

Prepared from RU audit #236 after excluding the 50 labels reserved by v3.137.
Expected effective sequence: v3.137 396 -> 346, then v3.138 346 -> 296.
PalletTown_RivalsHouse and Japanese audit false positives are intentionally
excluded. Pokemon species, Move names and Ability names remain English.
Gameplay/trainer/reward/inventory/flag logic and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations
import base64,json,re,sys,zlib
from pathlib import Path
MARKER="QARRO_RU_RESIDUAL_RUNTIME_V3_138"
LABEL_RE=re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
FILES=json.loads(zlib.decompress(base64.b85decode('c-oa(ZBH9l7XB*(>PMgpt@42{5%CLgYhw$XpsXUHseQpC#xvH;IMf?O3eap>B@L7iHBAZ4OS@gE+l@mo7_iM>xbu(pyj&Z5{DPw-;2Gbs&pG!w&w0+dxj&lKJ^k~%UT{BOSeUUav2<fHx-@Uw`7f5Dj=A!=n{kYS=S~<_W_0@gXxE~&_|{trmrUJC*{*j(_dHXKPLIlc+3+9w>+(!iWkr*}$^-dQK8M=}@|FBklgDuX(BJeoH2G1U`<wEEY{25i#NE4={KMaXs}KHT4c0uC=WuZ-tNw=nM1x<C#xz-nCyr%ZmNofK?!kxt0Uy6J^4aKvu{M`dV$Bmy$nZ)_DSK7qZ7U=!xU&T2_wsJgdUA9zC#<iGm6eiNDioKO7Yu8~P1u$@E4;8{uel|3{U=!gbHSSt4UB4le@9^FSFzdI_?^_PXjGFIaJS-bjG?bxkvWlNe;vHOfZtF3jfn{eNdbP!_Zo%eSXSUllfU~9$LTLzeKtCFwee}8=jZLrs_+tC!nUngK53<Lwnh6zA-_JNr6V&5Z9W<LI+E7>O)Zh0&=Sey+;uedFL^qq`P*ba+ERg?srcW4O|Tu{>;c?6lx4VE9U0CdN6$hC6Qz(TmUY7^MQtZ#tm>Iu5p8;}0f@ebuc^bv`;YJfOiIPRo(bK&MZp6@{2wSPHF!tXXzjNDR13u;(V5u%9gQ(khc`X~xPtg#s}j298n#8K?g@+TWn_L_tQl@6?B6n^DGF!^V0IlM=0AiRCt%xSOol^<+P`F#p#BQp!0U%#BY<Lz{FEpDHi4*2c-J5m9)hRqkTVe5pcm;iJLW<HW|wZ-MOXB6A-IO@kD2D25ZOf0%{h?FNe5Pu6D`m}MC)iVryB$pb_Cw2%KA9`BKw}n*Ybt@QSMx3E?@&wS3L`#<8S#-t|KCPn$cxL+Kvm|u@d$@is^H39Ng9jT@85}U=xK5OejDm1PTa8)(9S-VtrrpLb~Na>SS^=R%B%b4f<Wyu4{-+`t%w`3(*HigWdnWNmTFU&+^~$0PU!Q_4L*CCQ@5=`kTS+yk%vDv*OrAE1S~2+|q(w^l}l)b95`ydvgarK~AKET`)!5c11deq!qK$IT6;KRZF-o`n1aljS*|$D-QA=kQs*g6})~X5AfzYfX54T>fC>d!PLNGB&-d^3BdY<`%9Py{F?{s#N@T5IooNovQO&uUCdik%9!BIysc+rZrEP4a)xP!?4simaCX7=U&xCC*k<%#2l5GwuCRHqE%F3k9Kp7n<DS*1YHbsgUxHg3_|JbrISl!WPp;!SeA&R9L_`K1R5fyHh&npeQAQVpu&|m$h2xZX$Iy*ES!UWjWaH&I6u>j!jkB)0%AAO7!X*fJ1YPB=szB;cp5VLWH$W1IJ7~VXtUJcvp)PRLm*$1*^=Fp0<q_TW6x<x+A0lRjg($$oDc$js%a;q;DJbw{OO-=<g!owpuWFp*O;u1u)<nPF$Q}6`{DXwm0G6s+R=Jv<tIXTNkK*Jy>EYP212qWiQOGWoGP>uoUsKV3uJwO_g^!&rB4vh?;akaRq?7766hEx{uffzez%9FA>2r<p=rw8-MC1tjgPZmi{Tb8fotJR^GZ9Ps<A2JZM+VoesiDeND`|3$;d;Un*|6befMXq?UsxvAcwg#-9n6ihX>IavSb?5mF;nG=Adkf~2)-R+Ku8TG0klM9k%dWbJ7yfq5S`WYFGx7rP{!yP0+;B8wFZ(XygY*xeT?6NG=oMlvsN`Cb%GS(;sjHqeJw12%S|vIsJAyQO$C@{Y7i~;Sj=_RbCu6&drdg#*{@W-kzO_koHa;4jnPfI7ubh{o<%W$*g{E?|ADB!4~F?b?vC^(oMD7}r*5Ay*YuJLD(s#x7Y#4B2-4Opd7x~S{5k}qD@`qMf!YS*yG1OxLGt}6<gB(x(l!m!mOS{8=|yQSjY$?Mwx*;Qsd~~m$KB<x)6i=}ICG7inKkun1khXphKafJV%ZUHPGr%O*MNkh7Jnk61EGG;fhHFjSjg#*NG$-?(32`MQk@`QRy>1jq_Gm47{D(>wHpH;2uSv{ZLcP2Upf@}I+7@e8_c*e(aKx6rUXLG+-7}^T8BEb>;*Sl@|13%d?C3Cf$74Q@vV|XvksIe(ic5_>9LMn_)5>1B`XFwf<%dZ%npmE3(D~$f)Z+AFaVuE^OVdZ%#5*sYCvZakED|G=_bD)A}6#oKRiZ7u6#Y<z-{5=4bxCzCi<T0=|RthybC$Qjk$9+uw;{^8Vuz73+ef#+cWb^lMe{`O{q#ucuHWSibR<(rcupP24gW^$Il_jB~Phi>TknMdoAWBN=Y-Tta!-+fU6}3k+|;k(x|Bi)VA%@k~UL`dlZ^6#B_nW2Mj)wl^_Ie8yU}bN~p5>Avv&wWxa0ajZS_i$y_Dm)mSlCSiLj9mw9U&u;e3lOq8fZ@E9pVdYuuB$l=Q~?)%O$!;zU<fS|6p!;g>vhESoM)$<}`I~L>`X%*y=o}OL#5cxW<uZnEU166Hjbs7RZljU)6jeme3c*7XLN`+wErp*UGs90*~hQCGmyNlt_c=&-L?-=}g%-O(=FunzkP}bmdrAEjZ&dw;*sZu(pdnwqh6$a8iQ}Sh}-PSKbzTKHk&W)(j&*PZ3-O-vH4}gLk=1yGc=115DV!5TZCkU!^4roF#M!0CX1>MPrbP;IX?A^c)Sg%Giwq0;<=qn*d&*w!pS~N{`?|_CD)H<Suegh56KB}!tnbFJygcEb<0Tly~qTCdHK$!l(S&xfPXa;jN&wMc~&!}>oGO{b86g5k6;XxHh+p0jQc^ZHq6${TsXsA)avPB&)3uq()H2qLhLismpd0z1VgvvN;qe`D42uYQt!4r_y8ZtNHh>QoY2kDpxI3<_ELPvI@ezK`w{?|jlaO-ix49=C72nhntMTm$}1L)MKkZti0Bp^5C?}Hn!FNbKnzEm<^Uki*c4`|BRpsD0Bsz+7xA<%WyF1=KlY8sK1j}bB3m*^oaO7a6W6D4d<L*jZ~cbc_Q4O0M#=dI7e7ync|Sdo=!_|A62kSD4<ETQ5`1Q8sVT<_oTQ3p44mzOs3A}p{47jDurON-Eci#v94Q8!o7{x=vF_|~@?wK>lrPS^y!Bbp-vYv|7=F&Yvf0-87k-8rLlBQ;N2@d)mH=!S1__^}8L=O;}|Iv(IY+=RZh1W29}x}%7d%NLe+*#0df?J=B>f{!?3*r6H2D`pko8QSY}92@WkHE_dtdpfqFXA?3tsT%LTokwd07a!Zw&1`V|PPG-knKgW^sk~8~bD-BXQo7vG)l_@eHmE{kr|OKe$E_yQ2eOc`+{37af`E8BJq`uX3f6vSR7Oan;z++KhG=5<km|`c&rey4<M*S)>67-&Gl|Jz4lX7Y<Kn=`D0Eu6tL8vxNL5AR=u(_qAOtR3${Lnn=H9?CW}Ku5WV}4-HacqDYnHP(e0vC5umP;qf3>2GqN9h!ve3Qufhp_gOBKohpbTp!8uQ4x(pg6|wtm7os@~kFw$Gq`ei&m~9JZ?}Cqn;%27*+CG|G`W(_2NJHXBMrCR#${EeP@UICCKK=SS3dq*HLxx~&*lmIs7(QHMGj*S{$_hSevb`ma_kG6<+neEdY}p5j3q&|+rpi?Q$8;D!uvyg>xe93*m|344Q10E%ij7}}v3(VqN6zMv7%ewRbVOwKj*OTEw=;ysp;3pW7cQDA2Grr{>naKaddj|NX}#Nu(taLTnhj;(1}uc!(oVUL>2-B_zjLt;sVCNy}v-d66ozbqs0S>Xn2PQr`izX2@~`4&QM*iKJ}x)yOmX=em<l!0>>)iYA4t31s8z={ty>w<J?Rc+jc;u)TnmhtSx-=>*rgK~r0s8(m$e)`hgRrDVcPJZfCu_>&=dT}KOF2~#jVJ`DXfCm}->=I=G4NXZSDWA@p^UntBJuH^!;ya$j1j|8<FxqGi#ZE8{2c!~@Ar^H<<oeEn2P{{o5Y{cr#CJ$1Moso=kEJOO*2~l;(WzZ)*oWye!3^8rxe=a}bse2{OhdZP9okMKXG{63&VO+UkCjUK1yA>ig2#COmHz{<p^SM0-~9sTwH;=RL+AHG?xV54z>7UxI*sEzRO2u2-YwAbAK~^My#1Ec!;5L{{(S8AO#H#%Iqw&rH0Mo-wOOF%8wS+mv<+7tpY8=Fyw^1UJG>?qP-EUiWKkpHKT-^<fpg`i^yx9@O)n<9yKSdv3jNBlORsgo*_Tr?td+DKHddgn*mL%*ZD)g%uvR@ep*{jF#fcKv6CU=Bw+1&fTB5Y3w9vw_*^!~<!IPgd4{n_k+x99fSSZ-ut%B?6hC?k<>*yCKc(bi|T+WGUbjJtokf~5R%OvSJ7k06opd^7mo2*b&M@18sa~=fB`ow_Nn*#pjl^wTQ#!0Lf^shl6yK&x?gvtzL*>Y>1df3wUO-)C4xVl#_$G|jIUZ-L~B-S=uxbk4?ibkbPjV>Bi6uh~ah#FRQL1Y}kCt6o^DX-KRugXIICB6R^$p#Z2HUEC_2uiz|=rUZ~6PAkPaD(AN52!;Nky%X^AvJX9zMR%ML+h-3v)S(BsrO;4AdEFB7IUNC>b={#_4XJ*U?v9m(*EUF`q8mi^(|SPbF`%5Gn9g@94$A6V+}FB-pU6mV;9&NuoS8A{}fV!s{6khp#u;84;Is_^8')).decode("utf-8"))
EXPECTED_TOTAL=50
EXPECTED_PRE_BLOCKS=346
EXPECTED_POST_BLOCKS=296

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
    out=root/"build"/"qarro_ru_residual_runtime_v3_138_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({
        "marker":MARKER,
        "sourceAudit":"RU runtime #236 / after reserved v3.137 set",
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
