#!/usr/bin/env python3
"""Qarro v3.135: translate 50 large verified residual FireRed runtime blocks.

Targets exact English-only labels from fresh RU audit #232 at green v3.134
checkpoint 58ec10fd9f13ada81afd5824395efb7310d7245a (496 blocks / 119 files).
Pokemon species, Move names and Ability names remain English by project canon.
Gameplay/trainer/reward/inventory/flag logic and Ash Bond/Ash Cap are untouched.
"""
from __future__ import annotations
import base64,json,re,sys,zlib
from pathlib import Path
MARKER="QARRO_RU_RESIDUAL_RUNTIME_V3_135"
LABEL_RE=re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
FILES=json.loads(zlib.decompress(base64.b85decode('c-rM#TTdHVw*D)dXdVgO>6tm_C@;tuLr`o$wh7ZmEujkDKnYWYs*0ph6e++-ClP5Nw+^8b(n(IAe&}g67>tc=%wH(~qgl5qmv4|hZ=-(TV%OePd#}CLx4w0$dslLXXMC|_EW2N1@7iN--mr2rH|!Nx&x|<v`7hjA$6WT@0n?hja{b<w_Ay!gtp~r1*@cvCrR+O;#CB3E?t)|6OINO6@qbtTTYtxY=l|3H-QQFGOaHmQ>;K@tg0FV{H_CtS@B4f3@h$v)2S3jTzWHVur<MFO|Dds@{6b^RFDn1oFZgBu#4p14<;Hfu@+*G5u?{~E8k>Icn{TYPd;O{!8;wVBk9FmrHy-$91;6TzHJDSRhwLi9*m%--rW)JIKZF~XV1{4w4;0>5`A0YjF4X-3jek#{&tTFT+>91fRN1lduTxW*8|jIOl!D7uzl=+%!(|w&hQ>x!aG7rM5iT9U#RGaOZV?vQ*iba%j4syOrLu!}toR4GW53qexQZh14`H##ji>FB*&6uEmHYjXW1X}Y^^$F6?Yr8U`D&!=v9^z)V@;cPjQphSdP9ci<uxAX9xg(G1P}Zg{wctMPSxbZO+B3W#~_~^o{3*=JjK;2*xNd8=o|;4Z2hW=PYq3sC;D*ojw1QO=*DB&dn%Tmn2z04v`5-B?*0r_poT+GRv<S26mDE5k?x@&@YGIlP#q`o1CK!@1$-okWv%g)*7q8}#ZPcpjfb>YP?9rTBRzu^1n1y?Py7CIrT+ryj9H#zgJABZ$8N=v_pdAeH~+L>-J49tzD}g?(;j~z2{hIln~GLcg}WCUk8uU1U@?QN8Ys@P>d<2_fd{-D6$qjTS`XrHY>K%w9-_{YBI9#HNtHmsctfBgFo3s>5<MsD!TW5}_n_2uHae1gk=Fi_CLZ9P*oJU0?tvuJqGlO=M_Ymo-Bc`kodn4LyD1~5$1J)!Y^=JdWxwIk%2CkH3wXLE{0FRMU1but#>UiGCK($a&h$4oL&g!R933w}2YmSyr8F=w0Fs3Z6}TsC2}KFY%fj@F{jAm%I3z{^_<9}hjk2tw_#4ms6TTIk$^qW{fG*a8bA^*RqSe+}s{P?wNGb7Va5|`tfwYfN+IV0kz9B7E5fZ@K22lBW$nBQtcq>LezdB`k_R8#n&Y|Q8qC{EXhToG=2vOREi2}p5l>_6Fi)Sccocf4%grkcLI}Cv^?fX#Dpb{ITLyt*|84e1FxGl;Z2=N3ZN(#yYaF6F9CfD0>D{ZfM`r5UbgyDJ#urtG&)ic++<5#b-B(RiWjaf+p#F*1g+VHeHZY*iiw2yF58w|Xn;C%XUO2IzJvT%`)(JBz)YlO51ogQb$e=Bx^Rs$zMX1z~meMpn&Ip{yC0Y(L&Na_mziwhuWKUc}vt;G0nBCWC$)8hzmWiWwfAjQ`6>1PMgbcd&S;NP)FAOkK2UJ$hoq2P&sK+o6*Cq-&V;E5}W9Mw6SM!4tjbm4h&+{LaAtLs^Q^;Pe)gKKnF3B$>+_J-EJR%qQtqhu&8DE~+J{KEg#g;NOf9|S(LPr)z(vP1F0C`Z`pSz{Z0PCyLE*{`#Sl-peNYdY{>;6Xcme9RB&;Lp%{!dr)uCEVr%K&wHG2R!a$|3wIm-}DDgwTl-B9TVCtQV?>oXhg+91d1MVY<1utVA3Y2GTf&>BD7asgvQ!X#T~ai5axrXe)NAL688%J!eH9S2jVl2XpsjhP<u47sJM3F!Gb^pBzSWaTqzh#-np^H44@`X{ykaYLBMv7SPx;S2$?BFaR5%11|a>a;pKKeHDcb;0;kh}1y0hqz3P~jx6oBNdyghD$3f&keA9Z#L|3LK=7tT^T}4Un2QHITYaJH0Ck&2!4hj?P^j;>Lp1BoE&wO>iX^*IoY>H+2pNz341O=6l-P{HvEP?hGYAF*QBs7)AMn6$!!u2A-#TgHzV`t<p2ajZ(CGU4AHh)531;ZYa3YUdR5$vJ2>cl>O7hJ4(M}~B8f=^&3Z5SuR8i*ItS7<6nh+<6Q*ic}(YeepgXnv)DzG2|-%6|h|v`bF$l4D6~FQv1_qE6cOV$6dR613lpKx`NH1rjA@hN5FU@au!JBa-zN>Sn)Ka~alGBR$*{jD5^JiVT=pR;N`l_`@^FtEz}0^P`Y*onB=WD!>zt;OaJ>oNyS`<)@vB8FPkX{<m%EnT(!wwAVYH>oJs-+qUK%!*jp3SMKO(+d>iU0Cc_+Jw|Z+?kb)$SwBgaJw^dl8zVGkKgS3JWaCvlUDj0i{sRbRk8tE83Fn2sj|aVvA!DEL+KrI6fS43%W`!tpEzsr)eK=>{8rVTKh^`(p$$K48=?|c({|i4qh1$9+-27a;^f3ana9lwi<TB#b;l_<E5W+`cZFroZHYc<^G58Wi4Ht<v@$GWnFs;mrGY3+=k^1tl4420wz7t%5%1ot41o|R6gyXt+=mIU08Ghh>gcvKjcpL`3OyHs}j)CGC?e>+B6GWKMi;;Q2oih_t$)VWrXaWfbu20EYBK(P%g2WW?WV-z!LP1Ads_%m3#!YXPa|zeFN2VR4IOX6#*noB&bM%O5nX`)ox`;fF+n`DO7$pOWh_2_%$PZ<y8({>|WVWIA>13%Ksi6fBW9#BJ5wT0cAh(FCiGtK3fLmrFEXs|FO_+&@MEFt<gSdcz6cy_ldhaHIMmhm}x(RAg$GpQdlG7O&7)tPr+v7;29u2^YQ8$gLm=0u#YiA{|4Xb$`-8o&iaU3<<vy0kuGoGE-+0=;b44d;o;8I7+Ce7J|rKBg~Hxt=RV1lgnB&~8=T!nH80_%VsvGmFun=z-Y^)+P=2f|Sxs(LmRO(ubKwn;rWdlV4BHg8805Omn$wlQSrYdTYrE@hG)vD>4C&@M4XJZ+b3cEQnsOB-IX+-1X=)!7xx()sR*xC_RUq%)qgGP^ix=X2Qw(;ag`)&S%bUL%i|R8AncLFR8EIUH07zH7AN0tYA+RJ{-pYlODsD^Xr$7+c|SrDleu#Gx|^mfa|$3OyKk3adJpEQHoo7HRRSoUMc}sMm~K;=Ku7g8WW^mrQ3{Y#7zxdr7?@j=^0Jl`oasq+`3wde$?oc@P=OPx6=$GjT?x+x7yE%6^-ZiKMi3vachiQfq|QK&aTnnN}Zjj-^Rw#nf?Tne=f>GEuEO)?RTgNVh~TGbOSeo!4ecdr4#2G2ECNUod%ZFIsaJ5EASYhWv<>D@r2QDZhCTP#g;V7(2=7%RZB_$#g6e=2jn&6L|)^YNip0<dTUfF&A-TM?_o8Y}oXmb9S*3t-fnUYPf**GY{v9j#V35Bt)`c+|En?cccOS&)pKwL@c|D?S|ndZO@&U%Xlkub2>L{=kr7<KXr(U;pU))Xx0EAj@V;Rq>k`|y3;HDEg-_WbJ7d|IA|y`JAFbxD0x2ty#gmNS~5T7P@^isvB7FPfjw{JY{qNgeK{Kf8gpgI1;DoF;Ag1^%wIN(o%Motv^#El3t&`Z!?xw!wCuZLR?$2^@{!JDg8y?LpFK$dVdoL+UcU<d6YnO*BWcVkP5YT4SfGmCtcW5^7PchRDVYAuoe7T{HXT5Wxb0Zlfo%<sr4#Y2ich4+6KRI35}5}wdD_G=#Tpp;Vk|4Zk8<j3<d#mNcu?jDC}b=giv`yQIA}n^i*^Z5DAAD<=Q!h}Gp77ThhmDH<7h0EP|30Jn<^d~N+t&W_;#l(6JlPe@H|&j<6{%!iVGkSIv5Q;!_|tO9#h`!h&hpJm4T3?k0g)C4Le2C-%}_gSoY#iBBJ`^Tb(x1{#`eoU%Ab@orc3rCNdcnPfiWBY?yZu=EuTqmf-2zyisusxX(ihG5Gl2(P1GuZ7H6FkBSY)CbNn31q^z0b?Gwtj6;MwuMV4lVve@FNyG70C!Cyi2+rPz;ad$4a1-H$10vNKhE%z{g0e1PVD;YLh2MK!lS#DAw-Oq#`$m65Xjx&;U!w@_xUtzEk*ZL0q3=?`I1iGN@a2<c>NzaZ5qX2CPtr<foDgk$BoT<#CvUJru8TvH0u*UYH#vq`2H;g$8$d2=FNaBZ&ieFW`LjqM6Bd2W5pOD_8Rz68U>k#NNTq_5AWry&1c}mRVZQB^;rw0TFA@T@#S*e@0l*SJp+77yHiO_3q$PN9prs5HNold42}8t+q)aGH4y)+vmI3}-?*#DQgnemyIj@uEqK;X)v?eAt<Ur7Xf_+B0#y!fssL8}Mn1mYrIu%W>a*!5eRe*KS`hNr-aE$gxgaB!d;vk?PfP!Hfdy<Gfo{3-SECbZK)JIT?>`mAgMGg>itS==~3WxUsKECadBmetM2L3FBHH@C}Y9A<$*02`cv3x$WU^qIfjcL<c7+o=(oGU5GAo%|U-0B-i+A_tWN_QWdDan&Hf^A562Je~4?>SrJKugl#VMK)`+kMK#yn@QaMn=*T<0Pl;W`VZK^j5K0*N`;_iS#aE67BszX2xyjbA;4B@XsWq|7<OW^^{TDxIdGK{%dAhe~yUS#{Ee|6v?r3)@B+uy3jL|e8F%M*r;jWF)Yh;Z<;v>r_vgJn@*Sb6TQ?+{|EGH)H(Ey8+AAX83`xr)ER=?s4%T3M^7}XAc6T>gipSsoF_-(EjJPO5ypx^=BaC0qK=VkSmZ}16DFg=6Il=Pi4U4Z<TVv3>0c(Qv|a|-B875{<pmd9A$~6jPIfJI?l-8CuO@zmao{5^4zDSpqW>d3G&L^tm)T)g<POc6{zJ|vH<h+bQBsxC;Z*hIrVzL;fy`FpJNTm9wZ_p=k1)TL?WTZkcCSOU4k0nb<_&Mbn8@eQ`0i*YkvBb!0eVU=-KIbb9O)4^bI_i<RHP{U<?2<LWAiE=Utc6Ix&sQh1Dt6`iVb29g&^6%B?mms<NlxsTOiFN5095mo2;NJh4LEKtI_duY2yvkxR3DAHQ)hz{%$nTFHmmqp*%N?62oMd<VeCiE#<P>OFnZ>7}YGV&KjP}^@biDUl&f`wh42|oL$5;m~qE;K=e24+qYLo^pe4)WF#@TJ(S(P|I>8^1hzKFs8+{FUMz~ZCk5pPTo^z_8VvGf$I+mU=Nx0S)ET=Ij7i)seEHxiCewgq^HECLhs!w;BgOeaN#_5x>D0gLmU}1frKc?pF`#yOwbfiaBM2t376THST6R4^basE;!}1;`S_)I+g-9m#JQB$@<9roZ48|G{2~=y0S_IS`cy!hOKZ=DuQaOYZ0GDnG(Pq`Qblk}2-61odr(uR=8ncuH;EvSxIuFDryI}G^Vs)UohOqe+$$yyrWY-iP-&znxm0NC0jRT?ck`S!}nuBU(m#~mqQO}}fh-TD-qWfHlpb&;_?M^Qko(AcR*iIUpR!~`&okuG%MXr32XWSsw<Tfi({$noFJfKZfdUU<g&fAmId>dT<F{*sMqkRblQ<9uSMcUrB5RNZtQHqpnk?nyKc0aFfPNPXkH|=?2((oKR@A7rhql`T<=V_{*hk;-i1S-;t7x+(E^2Nv89fL-LIRb1JctDK_#4EUv{i(H(-Ca;;+|<Wy!Ey_>!j{&&0(C%ATQrp&!VU)JQr+4-E~s5yR;waGP1`H^oCUPU^0IbD>mi8u9ruQIH28eeiu8aUQm1BxtbJ33?USv+{sw_5@jnv9vuH(=a^FPFkXUkSP%-R;jmRQ2GzQZaP>QxAQB^{^0m|Iba6xV6vvBsJ@g%TeV>J%u#@P`VZRHa4^Fw;hcE~U7W4X?M15mf$abSbZ*4Mxng?VzS);G3j=R4wV*iy>_s+l#xbPMI5K2mQ6cJA*{Q@Ui&`4pn5^#H%BEfsIha&pN}5{rDAy!IWgb4Th+r%GCsA5c#QGwyOn?ZUJy<F?Tz!K85;lepS3mq3=iOBkO!If(ka5!-dm{Fpm2hp#*si+apU0-<lwTq2g74c!OH?a*=jiY)M4ULrsY49R;Zi~iL1e#5DfI-#W2H@R)OFW?^A)M6#cHz}M2<;SMO<n~@Rd#RgLm>y%rq)Z&?j|t?4aR<|%F%}BG{Gqul*4aD~bmfGswu^iQ!$J>e^bg$D*8$X-m}L=T!)5%nJ3P0I;flDuq_coTZrrejbbQ4dw(ru3y=`kwqqj|@uLg7X?NtcS<3kR~x!EZ4`UTOE_*Ay(wM$_yA6&kU*VI)NsZ0}zp(st=;8#SRH#RxjjV`R%c-GIYW{1rten#;+m&0HLcb0QI;JQGblt3?Nu#SYGN!#_}aFisjYhPX#;I|K#HtW@~n7hcya4?G$aOb7yTO-X3YP}gWud^4IbTq?hJ19$*gpH=onGw}2O%PKqWA!f#;F|T~;I$E{5OSwi0PDg0P${J~ji#IqUJzql$PC&>Me9kElT%nDn4DBolZ>|oX}OSy?*OB7u5ExOO-_=B26I1@L`_&zZhIe!w)>lO#WcxYz_7|e?jAoPbgYN(JMc+RdVpbr>Q5!+-I6d_<2R$~L>PO%_VHQ1?!pNH`?frHSTAb}<BAC@Zi6w;dZv)gcg<HDYOOCege}&{kx4%&*B_|^6@wBF<@MPW7T8D&w10}-xILRKEG(*G_9pT^k0eUu#SN*u%6mN2ZW78{vMrRP!PDMGsuJ|-g)fmbHacGS=)ncd9N1Xe%;}6a<{?6{mytPz4X*5A&Z$+Pig>lfloH)QCJ`HrC6g1AgRO0B<hJV}R7j8aIi)w)8VX9fkwrD7-5AX^%uRBXB5z|w<R84k7rtA?ZRCD2NKiJ5_MNY<wKMI{X5*6((zw_hn4317oVHv<t*qAGLZnmh1NmDF4w2np6URSQ^wlWr(Rl5D0!sO-#1u@xUv(1jAT!Hvr#0V90Qm~FqCO?GE0#k)vu`OiDth^6<D$k4FbTu)&;e&WV1B()JC{u1+9hVP<ABd@)*e~`a=FYe#JrY%^T%Ab`VF@FfrFFMWeKgpu(PK%k|FZetRpuSl9C%#1r2KEsI~CniLk~`oHUj9m)0p1dK8p%3)GOd)=s@sUILSYfVW^XrtNf<P{$zY^_e%U*4HK4gDSQHH0##B$!mZA^2?wB|1{_&Z*1XC(2xog$5n#NB5m$N6BO#))$%Z?&TdFsIr}vveMH+HNN-~_MHxhNCuFK%!zhpY{{n<xyF~')).decode("utf-8"))
EXPECTED_TOTAL=50
EXPECTED_PRE_BLOCKS=496
EXPECTED_POST_BLOCKS=446

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
    out=root/"build"/"qarro_ru_residual_runtime_v3_135_audit.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"marker":MARKER,"sourceAudit":"RU runtime #232 / v3.134 / 58ec10fd9f13ada81afd5824395efb7310d7245a","expectedPreEnglishOnlyBlocks":EXPECTED_PRE_BLOCKS,"expectedPostEnglishOnlyBlocks":EXPECTED_POST_BLOCKS,"translatedBlockCount":total,"translatedFileCount":len(by_file),"translatedByFile":by_file,"translatedLabels":labels,"pokemonSpeciesNamesRemainEnglish":True,"moveNamesRemainEnglish":True,"abilityNamesRemainEnglish":True,"gameplayLogicTouched":False,"trainerDataTouched":False,"rewardInventoryFlagLogicTouched":False,"ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: localized {total} residual runtime blocks in {len(by_file)} files; gameplay/trainer/reward/Ash untouched")
    return 0
if __name__=="__main__": raise SystemExit(main())
