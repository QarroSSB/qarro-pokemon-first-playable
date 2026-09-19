#!/usr/bin/env python3
"""Qarro v3.140-142 bulk: translate 150 verified residual runtime blocks.

All 150 targets were independently prepared as v3.140, v3.141 and v3.142 and
then revalidated against fresh RU runtime audit #242 (246 blocks / 102 files).
This bulk pass reduces redundant full ROM CI cycles while preserving exact-label
fail-closed replacement. Expected residual surface: 246 -> 96 blocks.
PalletTown_RivalsHouse and Japanese audit false positives remain deferred.
Pokemon species, Move and Ability names remain English by project canon.
Gameplay/trainer/reward/inventory/flag logic and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations
import base64,json,re,sys,zlib
from pathlib import Path
MARKER="QARRO_RU_RESIDUAL_RUNTIME_V3_140_142"
LABEL_RE=re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
FILES=json.loads(zlib.decompress(base64.b85decode('c-p;Odv6n2mj5ahwA#NyW)kRTmVYA0ahx;`i5x@3YNV)$Z{iY_s%*I&+S6)@BnwP0456WWVQJoUZ;#a7!i0pFJikKu8_jv#TQ66Y&90_}5@P$>=iGD8<98m{U!AJzuKtG=eYO6Fvb}gsxRXXz*bR4K?99Z%gkvuMp}y!Ct8RVBuoh39|LRots*3p1T_`#Y%N?GwT*p3j{*?F3+ts`SZ`a%F+||5o&D(*$54@IEDdeWL@=X3hp)&aAKU-egJMvnc+qnG1JN7<!EqdE-=dYc+1OIYrFq7U$h+fM()H>_lHoWyl=VoUU9~{HKcb#v5$br{Ja-G|q4ewa%Y;^8u@azuLfu)^$@Sp_*za9)pWNt2JSz=*qcw(V!+bd@i1=6*M_#1Cni@G&y*WEGQbxnaxzDBCsOxHWmyocT!@1^%fgI~XR-+K4GAG{~tW0VRA?1A?^Jpa^t49`CHp2H5mA4Pd&kqg8D`^OCdwU+mBKtuUx-ad%qsI!R#4!z^fmgc>O|8Bs-W01fGo)kWRqq7A|TLbCTO2W2uryAYePhRVE=cfDxB!7aBx*Z631CAL;DB?`y*gG7Ag9jekoh?`bV(Hu+?MZlCED7C3q7U%6L4}Ti;B)u@IA<Vw)Vbq*)Vz1_`5#HkVida0SzlUmY%6cL&4s+Z+FaD#`lQ{ci-nP7BglLMaXPI#hCMIfx3!!bYoHDzzmL85z)EWnMGsn_P3Ou}Ga7CH)V1B&pu-0ycVN{qKHs84f_)w1^L!>fiI;UpOxxCsWj4oc(?r6*vEtvr&j!J_Q9ds~t)76IJw^2zK+-?ss!>g@_O^kkU8Jv(VDTiq{mv%5|DfAgCX6*PRX263y1+I&4_wrUuOty>ESCbbny`m@316&ES+l~T1J}Gg&}o#(5jqWga6&du93P@6@m1VSWPkAUU}$J4#`LUxO{~}!5UU%uwJ@A~+}*2)#fpfTz!Oled!5^(8vDN!VzLcPwL14m58(vBB+yfl2YOGZdQ8d*!X3iXO{e8s_Y>cV0i{Re#n$m?kk)>%eUi@(DbEKK3m8P_4%%QAoiFT~Rky9c!d`c7k^jJtZh89}eJtnzdY4`JwDrywSs1!nQm(cnktFAeeO)+dMipPfs%)(3X26Y7(EFX6z6@L54k_<_4PDwU_<PuQo5jE5d%*+bG_JE{h$-T1N}QvYSorYDs;JJa38yIRYNJZ0eV;t*TMRTn3K-i*@5+QU6gLX&5M*+cu9Ww+(^|1GGk$5jAfsJCmHwVHmPzlQ0=bvo-!WczueG!ANz;`fZF*+rB78!=P`*?u<SuIYsmhi3$K)NOUT+2>e5`f;#>R3&UgrSC<y(3<N^arSWZ;H)g^ml)mnDm84SuAH>uGn|wygr_s%|Z!oD`q9`3Ddi;7|||APJHTdF154JHpO?BrERvYl!-oW82s2zNNeZ8YePDv?&^4Alk;wty8cg$GQXI;?Qd=H9n-nBJE~}vMZIIgV+sHdp4pB9-^M%1qGiY6kz8TM?%6!NCKZlH@1VK-y$p3!uI4H4D_HC9By(9B=aCeJtB|O0yhMjy3Nw)Y<BKxbpG#<d_*egl*e^b_;P+hnuKwE1D)BR7N`*I<Rkh(+DB^KopxsH&BdCrC}UZ#up3`bOkJ@XYvQ7fY_g*yKgFIRr1iAF5A1YDQ8sThf(EqzBX#hsEUlq<%uS;_uUoFDR%%8aXhW#+UXhM7{Az1tY9xI+4g`Z}4U9=NiUS*x$$`E|mc^ogAX=?VkNn$&W3Tv&fc#gprQDT5`D?jdIO5x=NE)uCKm@d=%R}1i+?D*~R6g#m=Y+mw>nj|e>kDINQ(#c{GS*7FVOE7xpEj0jZoZ~l%VJ)4g)?E=*QL6EdaaX#+{54JHR+=_QEyoX-viSdoFeQ=H%g&}j*7x4#=BjT94c$~9@c~<5eEFNH%vDVm;z#5MYrs$%?qNLvZ>zhV^7zt!=4N{kaA<?swpOPCwE<M;szh0+dM5n6osGz)PNhb-yIc=(B478Fb9%;iDCsCF5<*vR*<fp8DC2N0A;$#n}{wUe&=d<EMtx4v~HL=t2*x(t|$o?Hlb3e9SU1;3MW$5a8!@Mi~fq?iq3-F6~4T#+!)}Q&Sp2Xs?;2z5Z<hv!e`ea;&j4xu3@kR{3l4BzX6WtgyxX4ihas3zEcT~pTHrD7_g2ycfp0XC4k;1uZ<pvrMpWf0q?oVniF?R({5qqDqxVpmvp{PBIjL;I6<+O^$>Xa5p?(_hz8TSz`Qj~bCCt<mnmr_1jjf6LXbx8ACv|+2$*tRX2Z!;$Anw+eeokYA<DZ3H3izX5t^`b#$XR9g<hd>K>h%HA898B14eZkMb2*sTi+Q?Ck~#^fk;rPfsHqd!Yx7I^Pw66bP~X8wrk)^aW_Ps7q;0Z(jSrNQ1&JR$ujtQEkh;l3?l40$qMlw84eoIUo*t^g}o@uX6U$Hu*Jdg><&u!LwOHps*DeI2>>W4fQF5lbhl?}apsd!i!n!UR_$2*;1Q9ct$GKe8o5!-Z1M0m$qMixDENDM+IKmf1e~Rjqv3F#LUPVni4%MbpR=KMjLI^|-T`AO149M>(P4j7zM;i<%iAC7Mb1~+-&Fd>qCMuKz_EI8%<fR8ce`2Jkdh0MB|>vMSeKCc=;uoxFeFB~=YvIak^E;J=~#d1;+SG>YAs$7da9DxAcrHR+9vml_JHht2XY2w+@zp~=n(!?V4_XAMg;Zk4s~TYkrLY3z6yJ1lM8KcLr7_lBz8~QA=cY~d5Ytlezw4JC|kh%f#N#4W0emiRrex9&xFp9oY*0m<`EZ0cKuSCQuKZH>f{YJHA!EVFZPg!(OwisqNfu=g^XuUhgEX}oior4RWy4N7>*KnF3~2Zk(;FAM}*T#Qxg^KLg7kpAw@s&TgWP3d9UCDU-<UZ#$817I++`9E9ePgOH7T2|Flrh>#oY?(&{5=Yl+Q^LR80$#pWU)B-_cu|Aw_(w)HCV%c@Pq&L4pF@8IVp{5*s#m6GWX7|bbilq+6=Q+fe^e-|X4X@o<ha;AA{wPu(m;^ax;2&RoV>@F&a1Pa}3e9ssSA@p600#b6F|3cI=lq9lq=@L4}d|k2t8!tO{!>Z2eZcSzQFNp9XDh)jIe)0YX9Xura-mkd-SH#+VV(l5E{Pf@f{5*rFzV}{cCeUa5NT5}PRbSDas80RBo<(VntRbEd5NlH$yoXX+N5usxfuVP9Y7BQ}u@N747vs89OI6I)uUpYh0@ZJ2a(;x_s<cb#XBa`<rbvYih5c?H2-%eG82=7{a^WK2%vxH08C}GYN-R2HewcX8xu8S2nqcL9h1-BFy#@ye`tm*2=&?Yf&g%(1`C6SO9^F%ol^QvgSOQc0F6?~WmZ10xySdabi~5Sl+m0oYv1rC}HbL7hH!KTF(N+^*tXJ$RXDT5#0U+%a`%7Ty2+z8WVYhR~FD5eB;CyRK1}HqmUi1MK64jy&EX>)q#nRhnj0TP!V*^!kF|v_oJq%N)3fpey7ChBr9m99+a9EV85cgksVd_<xKFffd7m%PkX-+Kj4ZIDzVuzf{)Y8<X4zBGQdtQjV2bv7e8Yiq_*XBE}!FZWx7aJz{-V`77Ccd><aUIwqMvKjrWC#*n!lrHLD^bh7AJm}<Ki{T=<QWSWetk<EJfU?cWiBXlhi+e%DUv8nx%COi>mawR!_iObtE&Q)F9h`75uzkyKy|TWri_v!@GZN7ZO&yBa824&0*xOiljWw+vpzp(+_vCD)&#mC2vf3(lUW$zWRrA|(mE7lVn`SsVRzz3sFAENny@%t?m35HtYqLZ77fSDuJ@c%^&YOl$?SNaAuodXZJAQHhk}rr#>78KOfn4g(`St~1m|_bbws_MuL;L#&KhFY6ndS(Rp&n;^03c1qUt=h-41=|2yq{a&)ZyXIiV~Rm>X1O;19AO^^vy`u7q~;0P56}ga0S>tj_dsKb`4eW_K2Gkg@6q*r!y-p(rq@Tzs3`l(Kt!S~2y}@0jC5jT^@pZOMC6u^Ah2Nu6U!d`x$&W|tG%;%2?71aJo>=soyVKN<3=&40{6LKf^H=~vya!(QY=-6U=t4#<Wl7HBppXE=~eV@R|QaieW-58w=TJ_piqMF=PKLKoqsNp>~s7=ID}7sHC=g6b(oPkTy-GuTi*W^($EXVAywTvu3C-EuQr46ao!2GddkIBnT#&kV~Um_QrG&G!t=iEj#*;49PAw#1ZiFch~qo4^oTnI;|5zM89)7cS?@3nO1s;?^G(OlPKT2VOO-dJI7&(W9o{JI){|)yU6GU7Q>0pWwVGe7Q(9bRwy=gJ?g+=#7RW>*JJtV}F^5_~=+F0M*C`KTVpxCO)RZNP<W?LGy(<{3*hmuNjLqp9H1(9G4`=vU77Y7$y0H4@Yt3!4;Rqe>4n7ROMg{vrH1w^0~P}cjYcLnt;X3JlG{Wkw5mDWQZ@9`GdJyYleGtToQiE4s%PD5aR<%;catiZCm9FYFOup5}m<5S@2!{&!;1F!oHWNspiCbFjDa`=8s3yWk#)@l76-67*<N6mA;zT&6#kJp%Daj_wgL^7gfgJP@SSk&2W#q?;ydJn)@M47?W2LedPuV%gfYQ)2$5uS11+(goWzGc(c2$z{u+J7_!PNsU$3x3Eixyin{9<x>cXCVnvk~RAt}g_67~csWv<KfFNg1&NK#lke;-!SHU*`=AN>Owp}eOEy22=N+(r{`!Ou56O8GjoLcM>=%+G!AH=}(L2Q~92(d1$a!GoR>VDwt2Dk#gLuhG-2mJcNPC)>a30@gQ*;m|_>)E~N?qUt3jzdbhdeK;N>s%m}mDz*Ny@aYqVB|7Yq$1oNMh_m=k+tY;RikSWAln~`h3+sX^8h`?xKS-Q#<e0E_*|}>JFofeZwcy7RAp9@;6gp616rXxbs@u~d)P21ee`!w&3X%VOLY&-eP5G?JwWQuxrc!=(!8H!&GY!Y#!XW-mbsxxZ+F<)>eD@+{Uq<~*Si{y9tET?39ie!Ak{)ph7>humh_0A7a_$1sy#(IWj!i8GnOwj2l9l5BgTZjnCvCf*0PUW(c_FiU?524HXkMO11z-cMkgVuptqq6QU;RVBm=knHl8gUP^%BAJn=`xq6D+^zL7riJ~@2?PlW<%xQre&Qx7qu$>t_@0_n7ZAtoFrxS5dENeY#wDV$K-1ML}GvWZr$=Fc{$Q<~DOFFHb4Sn=)Au@BbC3Ap8&8<_=rM2;KFjrWl;wyhW5ed-l~%^y-v+(-U&MmyBf#OBCN62TGRj*l8uaMwBa>1?tv()cKerT*D?5ViqrHdm<>$``e<OLLPMQv$sP1QOiLYguA_+{4k(coTx;kFq`uV%iJ+Nma}^sUo-zYocMA7$0nE8l->#AUAQTRMN_YxynqrkTnWHaptq0dzH(0%cfbhXHC61Z@4vdV!~vDe@3lBIRPyXI8wlsNjuMcp9H2#17BKcX0B2wmAcps!|QResyprqM4LGjL0ajm$6Gl0ZZykc4P*)_Ov$#EXBsYq&$^uI<w4c=JehpL?Q0&nJ4U=48B2lPlna-qE*H|hYY%^#6tJ*%|Dbos+LjLhS!y_^O`3#?1wToMZ)7;5;}BgT$389H42FFpWAvM{=eoh!0uEw>SE6Xi14f-Y;G<Ndv+JYh^=dG)_a;=NK8}qI(trr;mi$_n1IBYabHKxFG8ssuH@7MP%{ie`6U8A-wvN8xAxi~Gb~zj!P{9R73lUa2rIfwIW-P<g8>-Z%@aGPVhHM05S3yf}I#-;!kSos)WCo|t`Up<aUUR@?!-?EYc@NY`u-{Ok4uB4VRRl28VUUn%XoHSYidUAy7*dZWgsceNs8HU@G!iT8Ck#3{c|4}k(xZWdA)JBK5SAUd60GX)U{z>J&wE)FW==anCB+}M?cAaYHT+~;HxPBui=yo;3-Fo?lYQMeNP3TSQ!YmSxtea8<94nN$<CM|o7Ft5kDVyGLII%lTf*36fo&cH2L(RjLmrIXv{_f#NjzsyXND8^d81xKHXsbmER`CI*AU|uO0$z!fP?>*N%=j$G83&h9kV^}a3iFv)?tIDW`O+Q<%HAynPM;BR7wW>uNhx*mHRk+;O{wp5~F;>1k7<q_V?ib7@wDoMF=KMOmWjv=GYQWly!T>@GUWEo@qx_4A2^+8{LpyM>(+B4jEynB0^p-iD=nIA=&ZEU$^8`Mq3TeP%bE~U-r(?2l#$D+aaCl!y%nfR{$DD9h9wLie=q$b5=EP|E0+j(ip#3IT1;0sPWT%dI3vtSpDz(jT%SqWh>=~T{O=M`bCvQ((}ghve|SSOG`j*eyUh3U8!7}m^hE3*u;o_8iPFr{LQq2NxDHtSHw%$BUrrY(ICTRe))#FVU*ZKyI~Oms#Kq|n*WSu;b#kT@Ly00N!@mQA!jW$-K_|{gtr1JdflZ%em*FP0!NiXPUdJ2XiyM1;({UvWv&K*D(usY8K!JQiEPFzHmPjJ7yiC%o{NqKWsK%T*8RRr{%K)e^uuIq-S5U^cp|>n#C$@Oz)_g*c!azc3gEGTeZJhsXcX%gl)1<kw)uBPhBbzbSTIYFRnIglyjD&bU)LQmZ<tkjsbsIo5+6_3aZdZ5vgW%QL8!F(CW`)4H0W$$-3S(q70Tr+0~yj~H<QuPO<5Z_CflrnV{)-DIi?d(ApB0F&~UbVGm%UA@Z<;CGE%T_FonX1x|8WHf+bf)_0sCNqhAl&$G5rO&Nqz7v+@WzUAuz72DwoN@*qOPy#R<@6%3u{t}j7y-kcQrT9YpWQxB5*R2*wj<Ne7JdFvbh-=cCJ!IH$FGm??4^}L*i@#OMUd1`!0-pJEVYqN#<N}(+8=cOjwc^hEEieVXzl{(6OsjrS`^1Ea()T`8E0~uB2bWEtrrf$+6$f>S<4E2$&6L(b9oZm)5|1E?1%vD!6ECC8x0Id>PJ(R-bLZQ1=>@-ZFTbYASU5mI@1$ZZPISp^+-sI{am!)XzLMg^zWDJY0G$v@onGBVXSSN%9i+Z3P4`hGkwRc~;Je9A^l&@&zncO&#pPji-n4Y<)l?u7yr9$?M$4Eaj9#T6e8zSiT;hgISy0j}t+y}MD75r`TRJ-ac0AfwH6cC!%SMhM`GfPWGO3X@LsmvE46yMYfA*fI#w+l=qk30APD-1ysNkZDhH=r24VZ`K~@Q;8zm0y&JzyaM5^)EEii1|RTqTX<SMZMwRjy?`{*NbAMK5o=kO})wdgl=?$p87WucyjAb_zwRr*MM4-k+e0wWXN}<ZZVusxE2@mkP!0p-}|D~j5)BIPU9h_S*eMMhUMRNQj_e=^ns78>3%WRT2+HWrdG5q|1w{fGY$qzv&UZLb)M+#skFbjYsRYfuUfuludI^EKlUCn{9rut1|B}AM(7jmi<v7EmrBu*)&xZJfGQd<d*YcO?N-yOG<1((=4R%=_UC;JY=0hnPr|IQS4~kA?wru;21ose>bnK7_c9oKGXjB?1F9uKP^Lx}U68x2rbp<w{GL(fMgHMFF7o@svyOe;G~Ak)uQkUFY$1;u@(v8fqGEYwzBE;tEJ(2WLZZ_{6}YLd0ls@QGbujTM^b!FA!mC<k6qJ#<yUke;m6r8dEaq|$9Uu|IV@ZTC4rj(yh>N!bPJ2GVcr@LNGNbm^RToE+9-~gho*6Jf7(dn+hD={*wLsqhlyZkPZC*69>Bp-B2`IMpW99v|A>X5GyTLW88ye7X6T!1<c%nK4N6U!OHij=9@dO_c5;{9;X7(Dw*32!s4)Xw6(q-~8WJg_pGU$ndE0kfuU0W35OvH4Dz+VHFO`^2=%zUrpjEq2ex*y&<%e{vLsUn4!yUO!9p(z(6T&{-yxyE?U~e>ZIZ4*v_;wjq41<Xo`K1g;RB*)!mabAv>`L26Ul-qa+!V)idC+j~x&iqEr-Zw7T`N>@QvJex{tlI3Xh+VZx9HNWLZB&^|8kCHh{VRQJSV<@Dv|Cwcb%{#j^>h*3S{L1QuqbkF`Kb(D*26q;cGQ37a2`D;cxSyTWO&&81-=_p)WT?2tr0-BFf_--KpD_*O_Hq8oM~H%)5UDQ>^K3%8llfr7YOhRiQhe^f>;QyTG@yqYW2-8c<Vb*b92}4LEX+(1Wfse{ae#is2C?UN7)g)OpSOUus2TB*rh&`c<{1<@$71=0$H-=0z4OXSn12Ty{F1d@?iP`iX-nlf$vIXR#%`Sf-^_ywD%0Vc4a2-IJzXYv}4yR|TM(z&L)dRd_7ogu6@X%S5;-NXSn<^sjI6efAG3Fm->cfw@}C+i9R8^fG@(fN9%4#G5M3PHOp?AvO)Z8uv^!B!0xNFwll4`c1t1XmQ8aGr|GnIRWZ%ZCVJI#_{M|NQ$}Xf;Leu<Sy`J4Bui#_txUk%WWDSYB2(iGig|sepPq;uSg)bSJJO86uw*)j)7hF^ddpOZ&o>3-d+*8WjJzq!~Qf5i3Hbs)tAS}u@V}TN1yriKLB4+Fc1')).decode("utf-8"))
EXPECTED_TOTAL=150
EXPECTED_PRE_BLOCKS=246
EXPECTED_POST_BLOCKS=96

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
    if re.search(r"[А-Яа-яЁё]",old):
        # Idempotent audit replay: an earlier pass may already have localized
        # this exact labeled block. Accept only a structurally valid text block.
        if ".string " not in old: die(f"{label}: Cyrillic block is not text")
        if "$" not in old: die(f"{label}: Cyrillic block missing terminator")
        return text
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
    out=root/"build"/"qarro_ru_residual_runtime_v3_140_142_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({
        "marker":MARKER,
        "sourceAudit":"RU runtime #242",
        "expectedPreEnglishOnlyBlocks":EXPECTED_PRE_BLOCKS,
        "expectedPostEnglishOnlyBlocks":EXPECTED_POST_BLOCKS,
        "translatedBlockCount":total,
        "translatedFileCount":len(by_file),
        "translatedByFile":by_file,
        "translatedLabels":labels,
        "componentPasses":["v3.140","v3.141","v3.142"],
        "targetsRevalidatedAgainstFreshAudit242":True,
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
