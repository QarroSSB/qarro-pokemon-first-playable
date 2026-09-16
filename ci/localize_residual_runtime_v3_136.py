#!/usr/bin/env python3
"""Qarro v3.136: translate 50 verified residual FireRed runtime blocks.

Targets exact English-only labels from fresh RU audit #234 at v3.135 candidate
c6a4eefbdd755386c3236ea1e3a41e45de8c4da8 (446 blocks / 119 files).
PalletTown_RivalsHouse and Japanese audit false positives are intentionally
excluded for dedicated handling. Pokemon species, Move names and Ability names
remain English. Gameplay/trainer/reward/inventory/flag logic and Ash Bond/Ash Cap
are untouched.
"""
from __future__ import annotations
import base64,json,re,sys,zlib
from pathlib import Path
MARKER="QARRO_RU_RESIDUAL_RUNTIME_V3_136"
LABEL_RE=re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
FILES=json.loads(zlib.decompress(base64.b85decode('c%0Q*TW=Fvmi{Xh)Q=`d(B0E&UXbIIi3i`tt|a2<NKs*L;u20(R8<Dj2q~AQ0fiw62j<WmZU_3zjKs8Xf=!$_cK$-uKk9YayL=Dyy!8Vlv3Fh8?OWga_P%?rZ2IPRE9R>A-Gb#>Wy`b^mcO<%=hQs0lys}h-+3k1TJ^nY%PyU}bobntWrn!pFJ-OLP1{_t?B$e~tl8%-oeSQE>p?4Mgj>N$xE&k>^>8zMtOcj=aW^=G4_e`)psv9$&2S@V2JN65`{9Sxpc8bp@IS*%_yNB+HTbO_9Lo#C4g6vn*L?_1f)3odslj7T;07JITX-MV;JSxFE2h!CdKcp2AAYdmNzLGM_yDgwgnOUD`@pT>ec%PBe{=3$tj{kAQ8mjB+dC^(P1j!$wqNueS1esfj`h)3E+Ky<tB&K&3ck{EY!5tkA$ds)ehJ<OZ-T!DFN0kTe%XT$eg;$jD|it+4R(Xq@beQ`e-YQd3qHaJZ-SQ^T=Xt@4u3p{pKpSvu;RD4;uT!-BmDabE_<!P9bN>_V9gu&`D5@7R{aiFy@d~+!K!!g)E9Ws2lx~3_us)Ttoc2z*@ac_;iH%I5&Xc1|8KB+Nuw8j2ls>L!e`HM?Nj;?pZ-4h_?vUFZ}Q2asFs`+VK}gWzrr;72~ubsqI5u^KY(;Pf}hPP4c@UE>|<;-3gH)61UaNK4Fi3kCG>QBHkZ|A^}I2y6^&d$r{wvCvZ9WQHA<YIfjJT!V^ZMVj^Rs84#+UN6Q(GqWgVW>(ja5%!Dm|3!W#_dP1?LA?6PnT=eEs-a$#(;j9W+EC^)5?!uPIP)v72bYS$fGcp1m92p7Hb0nLSX;sPk-5?6JjIE8QeA~>PC2{%>dKcd=bg*#Jd`5ye$z&8$e$Ox*+#QaPyt4~i);~n0xL(mJK!MJ_!YCWcb<M**{_`)vS-q7P2`RHNmlh!Sf@~Wm?URpGL;ik>&Yp!Mcm9ajUyqY{=xWe=^j$N>pEB+k#%cxjbFOX%YVCMt0A!vs?X!A6rW4PT916?!;Be{<+4Q_ZCK89368#wb{LRP<mpRXZXf2HJjhL{C+eG)_PX`<ceDoil~lm=y4Gh7dM2r}>qZ~1ZIRtymh04{tCm$W33O=Asw#mrg9ChLl;W=W*%YfjD0L!GRlr7tyzwMuc0<`aAnz8^lV860VlvR%r`4!j`Y9A^PsiA%tIiaQ3ii{><`pz37tQ-)+L2?S**G4jwMA}Sit!lXK-MPGvEaI_0f%@-FgE@d6pujsb#ns!MnT^x^&6Bm;c^gF9n)3S}s#Xo@E_=7EPpu4f~z@UO|%onos-p}F7HhQ@)-r7L4Hz!8>c?^Bj4LX#~6i~W=%La=CUD=VX<8k-|{Z03MLg75y5W~DFj10y!D?~YNudM){Wz4Ejt+5{7=cH<KK!#EgOd^2dwgeV1p5=2_^$g&dkz3RY<bqd}7fnoS%)CR+NeWxIr5PE@&R5h)(O9f(OocXB^bkLzFFKI%UkJvg|G%~+#mc{ibrair!m-N^P#CMW;sN|RH{jpOS3CUptH@7zb7i$s6@Cu#nE-1~g2WRv9#fJGfbt^(gpLAVY$0Gr%}(MtnN3x&fxj!upL1?%SOR#96a4)|RXMr%5Wy<khIq`;!-}bNeojl|hCNX%#%)_H%|JIs3&wY=kws+ZjOp5IDaaD1$NQ+9h=DcX6*@@a2%ehZU#JbeX7<%lFpHqQK`Dc<ij<D(8a^UJVvJ`5zSOl5@J=PHwW%wE^*v{D^0kH&@1u5JJp+4vYZS|jiYpXK=OO#Yx?yCI<S(wcYTCY2u%MwQ1^j0sw?n7A0{h_6e}gx9MkH+)$Q4jI4f^pe(LKrBw5#!~k(**e*0B*yA#Y=w;oo^gY4x%EO%=)!CO>!v*fQZFp&;|27<r4E5oF00xD&h#tLljCEy|L8$`|AnPc*pm9>U!TVIyVI)NsNGU@p=Lh6|ugBu2R76KB$5ZhfX}IeEwPXH4H`5P1r=fN>2j2Y5+J5oUo1&#IMUUNpl;;a)HATZldF@ClYna6~!rKX9vvKyvFu`b51Ehyx<bCf@0o@)Q`(d73}u!?+LB*<qNNbppw=Z7Mir;rn9Hsvq&4&a2r*HrFnOpevt6%mSZ7H7~n31!o(Wj+}Rfl6n9sG1Q2Jko#ZAeVe`ch(;@7G~v$W$&@Yc+!QMSZ@|#Onh8_RS?kFGNMJ<H{*RjQe8WkYeyO7067E`tD<Yz44-~v(IUhxolwyGvY-3&@;3!EvYru3Un9CYs3G*?y8#oQkq?&k#F{VO~I6F8K{L_@Qq4!9B2TlRP&hzL(nSzgH+yQ|lvJTfm&K6N32-5?@XM|ZA&vqxRC8u3+oHEc`d)Zqwy~_M*&ZaNPVZ?Qb{Lzp?FiZ4=SxYaUsAUi%{(=@o{a|1^#v(zdJ&KCtZ9hP0nC%b9ftzZGZsGO87yNRA%BzmIZ?T6tXjmrqiLU{=j<gu_#tk=Wo2zRj)Av|In2=*<ULcX9215aGY3ru&3@2l)Sf#vhR=M0>VM6d|_W<7xL1CZ0g<(F0U)OsR;~;3*!QZ9j>@&zh*-sk^Cu!h7&;1m+9&>9C8ymOk0llM6IhV-guO;Fm6BC#UAox8@c}%*N3Q#tab(p^8y6MRVbXAB|U}Gs?tR$V9UC!CO3|;XvnvU2<F@mITFe30r2U;<nj2BYc_b>($7b8%8JTUeUttM_q6l{Z;Ikp(ipVw@@EUkgGK<wSatRWA=ki;|fI#CuLG$<k+NIA&}8DhtonOV~Td4+z<sooN0;2ln~YPv!;T8fmeFX%digeD(|YWNqZ6+%T7@Sx3<GntMT^c+tUyYf1WFcki0j4I7YL0emh=W}u)&e$D<QR+h*=p5NzACNs;!_X>O6VT^`<GNPanb0FgmoeRjakp5pR#RTOcBkg9rLohXt$$a=ek{4(K4KK`3>LiT<A>BU072UnbsP!T(S!!#!-#G~A=OyzP;+97nm-Ye2$Z>JQDqPjM~P2^R8sx2MJ@(ss9btL-a@=O#^jJs|11SPthh6H7?r{AzskhqGV)n!CF}TU=)I!KQ1A)*#3!By(z&9cr_;Jj+Pdr=2$Id18Y94%hv+k`jTyaAxTYl`{zZf0|DI`+T**~HZX&vl%TszWva(CUNn=zaS`hAvRkfTxHTAdSRo8I~8UKXo=B?FLD~)7>vf`P<D^_aqseC>a<Dy4QdP1lqlVhFK5yc2l;-Nl^R*<ZLI$0Zt$3rZEn1qRB0VXsFYx^WeoRCHafY7f9al$O<g-j})%4KDR+-H^&)5s@>1j2Q$Au9OEmKKFw&aCCF^0HVnoOv78;0Qvol|%v)5#Q-Vc1elrH2-JfsWiVNlU^tal4lswJMvHN04&{1_h@xKHG4(BrpeAm{o_EJ&w^QCZ7xGyaOBaH3;0;pQTQvuwMo3|D>O?E8J1g~sae%BYVCGLz#w{?#V~>bmNDy;ZkqB82Dpth@Uwz%CYE(AqsM1+ixGSi*vZOPd{j+heN?#1!y79kz(!*10ea3U31g23p2lO~XUwc&C5#71A?z!Vz+lo$&9j6Xcd>uX30KVm^g@(u4Z2rT8*Cr4-BN_fhz`NL>?NuJ$p%k1Ae&$GQz9bx>yQci94@)}5SfHVo^r;L>CM5L)9Z{;$DkFv{}i!4V?9q6(Cktr0X*7E*$MMj&qu`O@I8?GLlTC2sQ<B;h12d4n(#Btpr436|8;1VkU1~ss2<I1lJEzEA?b<C{p3i_u(HEsM~WDOI5Ji({I@eUnFd$zehKD7X00enuJ8-OM@bmXeiIx?^?<17Lzr6IJhkp|G9SrwmGbo$+I4CwzRQX#?I}>&5Ky*Qsz5X$`RFsH5@tyYZ3dj7*|0zFhFKu9&N_{)N<coK0_6q6^Fv=jVAH~&o}t1_UQNDAo3}m39vnR10*Y@^04YvgN?i&grtfx-*I`EY#1>gLeWi9Vs1!&2gl{%Hi4vW|y6tLAy1>;`nJ9)}Ej8qLc8LFv%5(h#K*r5`Yo&@+^3J5i6W0&v%YRfuD7Jqd@=zsIsuT}|m%$Ub7C9A1HebA!m`f#?FY?wTqlL6tQ)&b$avhRZS`u+_sz(8A8d0ZCXnHJpWQ+2zMeGR3D(;4kj89w^7l;W*n(PD+nY1?AS~6<DHLHeG!0}RTLZM5ZM+6?6vL}UCEgfIbv$J{urP(ay2k$M(j;Kk32RK3fUo+;jSv^f&ddcWd_0%^_oT}ch+7Wn4OX!99v>wlDiIj2eEK2w_F37#IBJ5eG?9_Nv@UA$}U<@Z;HP^0~D@+R`nMq?^seeYG)-{`(ozL;CFvJ6K7qm-VtxjBU!o0yEZcKF#)fRaW(~QNOmMW&>*;(q0BQ_Wn)4qAlspTrDrvT<(as0WOOW^m5Bu}_U*PYU69>Bd2cw!r$)7!pmNTQ8g7j=O)^OXkcL>L~P@1=Ue$w(#=z+!C953m@u@ieNiN;@OI(BQfEEaCl|+TxiPu-p!xCaaM5@!RH2VSB|Y%)=1z3~#UF<^qg+^M)>CPDD;BZI4(G8Bv#*?&EMH$NN5TkpAhgehPL{yCrno3XWqumXUah6ByUOWYhTIP2Q)#RZ_7V@sVZQ=5=$34W!NM2xG#va0`9%9>up_Oun0gHKLq!JkJ79Ad)%jlzhi!<q3dl3eP6+&_ML7r^BnBCwl;nig%N_tg)2M6*BSky}S8z{F+|4#|%Ynt>OHAw`dfW7UG4ai}!{JCcy>Hna9$FTT~zaoK<WO#DB&F#B<Wt4H2P!SMF!hy8u-tX%;hMJ7{0V$iAnJP4gReC}#F_Ohs+FbctoP$>c~bq8n(DWf$(ncxpZ-Qh>8B?=A=J5kcL$a|XKgzE!y3FPbn3(N=Qa^ecs$WiOa8?$VC&3xZ{~PHu*s=T=YBk5W4kf)?Wj0DC@e%rPw@_(RvXi5~GrOCN~0v>pxS4#DtPm``Q3g*Z&sBha1k^_A;Ts`?#xS!;s+F|vpZ{dcD%s%v(%z4U1eP-6^`halmgy4uGGvtG5WnlDd!B>yoZ+@Nf1V7sN055(X&mH#aJ_5%`lj^+Hr59$|#p%N(ezoMVchdWc4qvP$E5q@Qmll66vwmgbLd-XVM+($<r((AA~(IAbx9<`FXI)QS+XQ)ufL%*~r$izC2qvfj#{*l1*%yLTcl}L~DhNukhi0><zu7A0lEyC^T$u=&EYSnPpX07FAz};wk<H@u~mbGAy@E5mrq!24L#Z9zA3J+NN>vD>F#L7$`q_P6lN6oRx;Op<gaPta}I|UzOT9n2eS(;q9y;m8^)4aG1_I!I&I%~Z=yJF&?p0{oS&8jV0e&woFmc&E0QpL%K&!T`4Qn1+M4X|~RY4%7%>&nf}5511e$irKtm`nN8)p%lVo~2d}!N3U+5<i-_6@VjCBwolfEyDv!tyJ+Wv!}{Tm`p~OablQm8TZO^)$*L_CC#cQ3;_kfECww`A@T*CF#9?9zkW4Z(Q=u<>m$R7<lC&icF>b_)FoVx&<ty<LBky%<HFP?h>#;5`{N*DNVLnwLd67oW~^#8<z?2c0I@E6tUUi3oLuJ9NBtY#sFTm6(&@|cWEFGZBU!T0RuzfBt?q`@6gK%>n%u6CQZ-w9ObLxb$nmJCjgcGaDy%BY9s56=r94M#WQTE9Os@}j`(@!a@4j+M(KZwd3@8|E5s8FZMxyE~;)z7GqOWMcP(u45G^icz{OI=H$5{UsT}N$y9;l~`Fs2bXczl|US=QUKj8|`)YhKYwI8GG|S86eylk7j)pjge6Vu+D@5YgpiNRd89BdO^eO$|&9Lwk%w50qY@MywWz<eL=VHVzF^P42zGh!1W%{icm~z|b05q_&?ChGXDJm~mKFdJXV&A6^uHKs+@}b29l2b68f63Bm8n1814};vCANMY8tS-WG36lX5t?LyEN#9;pdX%@t$WxY~x?8@J2Sr<;96R^weHvn-0$npd&JyoXw9N!$STgklQ(N@py?`!Uvh+v-iHNK)OP-qogkA*%FKNh*$&6+{m(4^jy|35-Zf!2CQd-Jx#B`!d+DAw{<2Va}tG`t6f6zNsgjc>zo5R&}+Ka2BkRZ>{8RBzYE&4hBW%a(ExPOVER|_!euXY8I3S3-RosJZ^G;Wx(frPUY#Y9Vw2V%Gx31A{uqZ@lpBOe41jyIl|#JJ<EzEXH_JeTD3fH1A^VWQUTiK@zzM4C7u%&42cAuPy$BB0b~R0SNfvSk4~30Nyh1Nbt_21gBJJY$jpZ+BdH^%v1f~kTwa$%6iFq4HYrAw>`DRZsKnsi6@=08-pQD@XE`<<#yZ16{mVG<fwN%wCr#IIoILvPMy<;3=@82#gubL*;4@_%aK{dELX72VMqfn9f<+=A530!#B?fN72lB?dmnvV5%2M=Er{0L=t&<Kx#&@`Fk5vQ*_sPGqJI;&9@b9hVKbgyb{Z4JUVnD4!_x3!dAb58DdGLO4L-Yfy#DfROFq0ug9uVJV`JXBGhRO*|4zdTNGuvtuJ0vVWB+?E(8=O`6I0pAf_@3E3v9Npp0Cz`(=K')).decode("utf-8"))
EXPECTED_TOTAL=50
EXPECTED_PRE_BLOCKS=446
EXPECTED_POST_BLOCKS=396

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
    out=root/"build"/"qarro_ru_residual_runtime_v3_136_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({
        "marker":MARKER,
        "sourceAudit":"RU runtime #234 / v3.135 candidate / c6a4eefbdd755386c3236ea1e3a41e45de8c4da8",
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
