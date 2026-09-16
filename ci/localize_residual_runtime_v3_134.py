#!/usr/bin/env python3
"""Qarro v3.134: translate 49 verified residual FireRed runtime blocks.

Targets exact English-only labels from fresh RU audit #230 at v3.133 checkpoint
5f9cdd22600ff36aab35a0a21c33b85ee3aa7279 (545 blocks / 120 files).

Pokemon species, Move names and Ability names remain English by project canon.
Gameplay logic, trainer data, rewards, inventories, flags and Ash Bond/Ash Cap
are untouched.
"""
from __future__ import annotations
import base64, json, re, sys, zlib
from pathlib import Path

MARKER = "QARRO_RU_RESIDUAL_RUNTIME_V3_134"
LABEL_RE = re.compile(r"(?m)^([A-Za-z0-9_]+)::\s*$")
FILES = json.loads(zlib.decompress(base64.b85decode('c-p;NTTdHVw*D(cG>?YXNarap$T$W(Z7{OkjUq*gs__ogiK#+W<@BIdBn+aH2qrX{WF|AGLwC|TnsYR2#W)lc#&#a&50wAWtlO?C8*`b587U#ST(xVj+qb^8*3Nf#YNl^~v2Jd7U(8xhRKcs8cI{zVd5-JPIqs@*8s5Ws_@N%oy7kpBycO5l@VzO^Ub%DkyE`{MQ&qqBA1*ldeW#H#8>?&ntm7`I>Y8akhD&$u-l^n^OY`^d8qrb4h&~UtqA+Sl!C-sp!Gn$H$cT=kesmfI8DsE=!FJR)@PqMPrCNUYb+-KQw@)(<9@tSQ>f@L2bU*q8Hx0H2d$1aOI*+<hE4nbEljve_V8Ev!>J1KP_5Y2+$-!<EPEAeWBCp`pr-L2XMjM~*!JS?B$t&Vwa4+s9q=ygT_lv>);5qyo7=tF<(1M>KZWwQXMGg6ji~kMxH^~z8@PTdER%aSl`jI6ZJRj^E@capU6^>cqf8c==+)oA{4&Z&kU<)2WsZdgoD!PbT_+%wNldV(>*~JNb@Er*fpaxKQTmtqxcnKF;6Ti8Wxt$G5YlZcy<*Hig(Xwgzmc2S;yuoh9Aaw<?p?b7o&<?z}Pa=FY20QR(6diWTVjScCPjN3`w0%<TJN%9o8EhM1(^hoGuF)U7Ap4*MQ5%(x5}m-JF9$C`b?5LBeLwDm^m2m!1V6*X__r2%sjf^<%`4Mg*j%=}wIPwGQKTQyRX)M;ff%=q0>UPO!7~ywgwOkA=T{=bGqgvB9jp!aoT5Ba><Og59k_(P#D<DGAm1~&$Bup?Z-JHJwsTe{tQC?2f=9xABxrx|QtJ%f4_e;2z0^gswpmg2jkV3nx>Z;6rZ?kS^}1!+E2{LU(y&1d(QDXypXB@=!Vh#0D)|L=wFd#v0Rv*x$fh7<3|1T32Vw*~6(T&t2JFK^A}Q@3)(c1*Khf@=4|ZZl$#58=g-=j?)JN(ya3{a!_M)Out4>8JfG9RL$_9SAi-y8i@4)s#v@g1+0qQ@B{u;djQyqby{y--A5pK8;oJb*)V9fY+0znlB;R7@miXVVMpP}XdHA5c~CSpY4HBjEIrJrf|b>*_$*_9Qw;aArzFYC=Kmk`>!%Fu`OwoepYEfC>lDwfYUvik_kAo{ij&n<z2HskSFyJ@qBAXpd!Ne7`4RECls55E~bhXQUNQ1aGtvvbeEtySl-vP+M$8yl`#u}t4`>~xH?3ku9cA$Tka1cL6N3A=+Gv{V~3fFX)r5TXKlyx}f^-}#lB2AKcNou`>p2CjbV$mW0NY(8q#=gf7Lb6i`wW0UVSx2NE1&Z#=pHCKsV(5Ame=Mqaz^e;$at>}EhK*!g11h4B-iaQv*BvaBC2&z2-sGdN)QJpX6^G2ak%r4#|1HK`Jf%%$=3W}vlHD4^|W1pBLUj<l#NZvPO8=yikWfKs3YD#CubA!C5YfRFD9rPo{M*Ips4)$RC0fWKV{T$I{aGw|GKwZhU+nQ~hqaosi$T{PTC<m^HIwChjV^glB#Dc4Q;;=r~`5FMePs?hIhwlY~(;$Ycf(MCrvwI{|;+#?>1^p)p<(sTrsMqI|pIj|BY@5?Fp%1;ESi`{($S{+_aD`3oU}lA#&1DzzMy^y|%$G%Xuw%T3b`P6myOZXK4xOZQN3noOmYh2vd!1lxkn49xoxNo1NFC?f$+w)78Y_=CtIoXnMCDZ7asZ+Tsww}TB552Pf|IbR`;vnZYy$CfL@?YfyGZ~~oDtE)ttRoPAv;l;AlMl}caxx-0Y@kt+DtnNV)+SKzXy5n+#pW4MWkatqj4;kFBVGLz0slC7*X&HWlf|HhlGv-y9g?z*?ywTAhk%ESdz0DqoUzru)tF3%YXd;LUyr`%}q1Q3IwYlz_pwja``&NV}>=>=XXLF64ypzGfqq*lq0r7qb=o%mi^dVRm+yYHt#5#NW@hdplc`uCpu0VJ=Oz#g!guJZ~+3)on6w$9}~?X#b7K(dW;E-ec^yo@dX9}V^14>9DZHO5kWD)(O)7iQ5HgV8uO+6;^Nf5Pi?gHTj8xt4cY>1kSi(Oe5QM2{Np9Mh{gD(xV({+lc+Sjl}WxdZQuFNm}IDWNuudCX81C@SS?NcXT7)J+5WQWuIK93y6Gzfo;g>UJ}T>{q+XrCBB+VgCP7a~`jMh8g-290d;qNaOk5dL819Cj8-kgUeP%EZwx+Kn4A=7mk|bNJsoH{aSAg5qEKflxUUWQP)$0VM?-(lsK}xE}V$?$WkJ1=WnW1R`ibc#%7s3IP(Kz!nx6^D&XTMKe(TAK~z|86FO<o|?VrVc!z>r|w5NH!&*k||bq}<~NgB>=|^rD5%IqX7zy5hA=0Vu=si>a)Y(h^?v9G=_a7aMe;NglsVRzx@29!cBGwcUp8<RD2`<?`|x)K)X*%45|1`-FyNj5H~mVt?7wwDLk@H`+idr%OpsQ=5Q@3_Qfv!RNbd7;KQB^L>bZhGOO&{QX&TC4;j%{(|~~u&L&a+0s{K+R7U?*%?Lr4!G=0`K!fJ{48!8oclt`cFKh<$;1d3=*m$00&4Mg+Nmm`3{Yg`Kr@@)m@X3&0&dN$F)YSub`~7i`F6p1qH43QvkvsYtT}eh@;6blA2cb8gFJEa04NL=BWVJIG6Pm*@0AvfT%meDr54yF@lAx}E=2;02$~v4e7Y1YC+IEcddK8E+c74-ML*$fFq_Rt7l*L`UqQYHS2DbOKjtEBLCQVB7^ci)G=nIA-)U4`OVxhYSl<9vh%`}<3!eWpVZ^^_M<aG02$B;wm5MC{#=C_?w#jwt9^BU<mkOsjxYMQa-w8UTEeEM=S5xmE`%jD0u#|38@WvZKg`aSN%P;zbFpte3qFfUk;V~TwWxIpDN&QDZLAQ>CPx7X*VG2ruKLuZ{d+1L0EYFABScE&M93E*?W{mHairM@5@>5daYbp-6q~_(|V-2F9w40BHWG7OpUJ7fDP}53&0QRUIl7jsL0;_|x8-?MP-i0uSH<Cn=j5B(7SSz^47sP9A0blGGP=XpK{j#dBI0#XdHD@E0DT>y*<tr*3k0wNei3X@ZyIN{&)eXlB>4BJgDyBHVxee5&1kz<T6ayV2`#8Ym_Yzm>Q9eo)R51gPhGYPK(WK0VpU=UI4mpBSmF=a<i`xdEl*dYKDA${D9e+)^%Z~flODZqa&mjjos{VrCM_c(G_co*if*bCKQltUK3C%JtS7AL0CXh13rB4{h(DjE~68*R<#JNkdGPV#20m&MPc7l|%;lJaAF4b$x&bnzAttZMWHT;sDGdF}UphytfP4YCU(?O07ewLaHgO+kQ^+=whjnYLqSIP{^lvE|(bD_!Y!q{U`bb4wSX^x^-ni8fP_PPPgMep%=lg>LEh>+L{D){h=JEOcY%<f|>1i?y^JN0MM@5MY~Q1AbO0_`o&A4s>Sln(T>)W|zXFk`eN&RMo?LiW3c(~aE16!j5o9l;)ue#!Ja8n)PTPIlF_sLpzat%#5<bU}!DPE`dWP=`<yq!EUx8!ytp5Ripmi9u)5laRPY0v6n&C{2}B+r;?~*m1k)endQY^zsX-mJ)J?+}7Y;5H)7FRY+?Gx|c)>ZR)}!?w=Bekh~ir*{0Rs8`W}Qaw%J>h<&I--%4d5_AFg{uvdMSFzBK)f1NKc6hPiZW2scG(yHkJ%+R=pd!8e5z9f7dXRVn!SVdtx)v%bTfML~)dgQpOXnq6Mnki-ri+N^Wxx(UNb|zak=I$>TlU(Taxd@Y9jNpeRSLX&r6vHo+iwS-t0Xf{vz^)jibYdgBsIM(D{h<(#4#g8{ub7>Ys3Ok+Jibc8%8I3I9}=gR|2?3kwGN*O_JV19++U4;0nj?6{l-KCWjYxgp!xp*KG_tK7DGHILmK*g;(j!2^*LvWGs+Q2ow$SZj;DAWf!#C_p<x|)jnF3~32}1-ti6z3tbo<86m4#Ey<)AR5V2{bYKWHrQ}Mj+EzkiV)^`oI=z|A!EQPU4M3nZN5&~1k!InYM(~)grk{rbb<u>ZdBx1|W?Ee}M5M%D+DXh6_TaT<2Fvg<#)~jql6<b5pm{Be;L}E8Y0J+1Uhez7GLIjJRl=2cc;yqju1=Bo5rHYFD=7I`+cxFPzdJ^@NVKY*eanepNE2Dx|dV;`!j_%zgtD^gN@M_#CL*F6mzve-SlsfwDSB@2~oG4J!4Z}sohJ>IrlH`3;?>4n_alVht*1AU0F;8dQnS8li$X8f4c3(=~GU6k@yUKzEd&N~X>zlel1CE&PXp$tgqhBXU!cnzOaBs6Kz4f1DBy*;#V8#<#;jdJBwWQlEM(d-3iMk#blBl_*b1)%V*X1aWfs+aBXErB727(Urv5=(KAU<l<aI`$aJLx^|)5x3jXL-`gu17pdM*4m1D6!eUCn<MuFiHp_-X;c_xK{I^Z&Z1~2AEzqeZX!?w`&%u{s)<}a~JHKdUw=RZ=!>xT?9P%vK`R5xS>Jo9HlrB)dig7S|et{MW`~nG<_S^o-wiqoHq)T>IOFW>Pxx>Qy-~pO9Ru?zoK)FI<7YK;8X5u#VwOKEI1CY_jn#d&N?om6%=M@hN}5E(S1h9!EI4%dbr0gUOt3BOhWmhOr+R-dOUX;NsL%h7{c@qbS<HoXn3s-B?Nnrmzy%-<Wi5o;<68u%C2`+9BJpAM!i;9GhG4-?C+MaTp@-1iPxtM!|P9_EMRBg@EB4D&;C-eNklzi)l>1%gqvx7CKgnWba-wy8Out=TZd$BrAz;$>xkjQdWft0uFQ6?6ghAIx3dYpv9Rf>`XdxKTd!9f*Y`?~PyyW6?s4ZZ4z8H9Y76hAV~qtTq$ipZTWXK7Z4~w?>!9Idf`;$mu1dP!ttq%Z2h^mhoX&VqF}Q!dsEbf{f~0xdSFR5{QU-m$4tDh^CgyM4=1bfV`%5ixQe6o4=#UD5uvigFC~p67^9jR;&bDYU=Ry^BDWgB)PQze67P+Udm5J*v*WFxl8Y^oBZ?;jd^YpSijV;PHrCP-4`@pik%FP>c1OkvVJ}Pk{?7frf1@z-c4q_XpPXP__tBQJ}Y@vF5R-o)S>%Se#v97w8+w7k2G;GAG8PoT<w|*$T)}Kfi%5mzN&bfUaNKnBGSkfed`a<e8{8lrm(S$knnFMAMvGtgo8U!4NyF6^dXva1|DARjtH~~%O9$Gxs3?#i#cXLmZA}*B&djyTg*m=ga<Q!BoGnQQ(O0^Q`vi}gHO!9lkhr>ib5D(ij$+S)??N}M0Or|}Yl%zJ{=Kp0PijH`#^=6f-qeI@aJac2iv1}i!7a~{*bnv;H{RuhL_6$$=(1zOtpi=uDUeyKHIpG}#OiWa{fzwY05PVP}HDi%hf(*<;p#y=e_Y2LunsG(j<C%D<hlg!xLWfd6>xzmGtWnEak8LoHi1$$gn<fY8xm%0$+$OjdKAqMAFHL3pmJA%W<QUUITs7=a1-?Z!HArx?X{ZZHCs`I8+gnm@#j2@<e|_K<0k^(n1ZB|Rzonb2{Qlvipu`9MoSGO4*qvcC5u#J=NaqMc_C>f#0oF+!(-a1n3^eJH-sP4g5f0s4zaX`9OY8%+BZXjdGoeT3YUv{k+$ao^v1`Cb=t63&^^^JQv(%BoxaW>1R)iGENgHVf(y>W#0ett!88`U%EuX!i!-^+-N~IYW)DXziH`=ab*EcCmV>B(B{>oa6j~)-el7lI9&@XoXjKQghy4j!kTqTZ1^}!^48kCPKk=Auyp3()`1ui5FcWy7!WSN^{$8yMvzD8)H;T9k4k~VbuP-l+^-KohLsz@xDO7vY#I5=eECi4Y1s`UDwrD@vJSy@gDktl(|NUU3+L1MIU>PDUC*35cc*{kYn%cB#!RTn!?ZW1!rk1NCq=P?%}y!|=F;!fjpO#~UZ<4I0AQ%3YEIe&}G2GY+<*yea=7q*;ohi#tTo^q>xNcGZxOi(nubOQ6e_-!bKLOd0g)Wh@2*b5{s(teOWZEhqjjGLYQo@;))Y<dNs+vN~;fB*;6G4wMRJQbiy^I~%BGYU!cmlvt7n-M!Wo^B^^BstUhZ_Fu&<G65X5BI~mBgif0;&h8x3SS<xgWe3$r8UT%%Z}|Q)aOXR@q-+yPddHNxz^eu^RzTRkE@F_@ez0aj0?uNo18dIPA|~uMLB<wkrQ|04zls!jq~CQ-JicXvMP9d#&uR*<$2t?P2^1-AH(UY-Vs{>(S*+y^WM0|=nr;dWacp*k6Nd%YXQz}uHW4M!<%&9a;~wNtv#_;XqSHx+IdJPFn5Gwaz~0dU|+^`uZMeCJf5Sm2=~OL$!RPUD%JZ#e#iRNL$H8rg;$VMUgLO}vdXwr!{hOhc`-Wt4)qzOG53LB_f_=q7Hct|-5KgaM8Cq`-@yI2(A(&5@cVoC^cJ7ulH$^0m&@*0yUS|9d<-6;e1CJ!acWg%uIqLxdG0YEK7`05Jx%EUZ*s!PfGbBDyAPfGo7RI;hQYo>@$kVy=~KpPPeCfWl>T2H<9A+cSl*K3CGpC3oE$>g;ZZ)%j$~MqoY6_zB|@|KDB~EKdKA;5xTF+n62vopZX6`Xj{v!^k>Z|Z+GfG_T{^->M<TIu1Y*Kj4*6bkvUyj!X*5tw{#yt-w0Q9eK~lQx4U;*s)_0rOTPKBFS8ou<2EOSx)KcBt#JMp|5c1`(iuvr~b)y5?kUm{;2-jZ2cdw%VgP(7PNyy*tVyY?^zRnh(CKJXRbT(xA=)J~bVe07vyxcn<r9IKxq)9Kw6g5uk5j!Qeq*CQ(-L3}7+vx1ysw#lkr~d>$1I_3')).decode("utf-8"))
EXPECTED_TOTAL = 49
EXPECTED_PRE_BLOCKS = 545
EXPECTED_POST_BLOCKS = 496

def die(msg: str) -> None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")

def validate_translation(label: str, tr: str) -> None:
    if not tr.endswith("$"):
        die(f"{label}: translated text must end with $")
    if "\n" in tr or "\r" in tr:
        die(f"{label}: physical newline/carriage return")
    if any(ch in tr for ch in ("—", "–", "“", "”", "’", "…", "«", "»")):
        die(f"{label}: unsupported Unicode punctuation")
    if "\\\\" in tr:
        die(f"{label}: doubled runtime backslash")
    if not re.search(r"[А-Яа-яЁё]", tr):
        die(f"{label}: expected Cyrillic")
    for seg in re.split(r"\\[npl]", tr[:-1]):
        if len(seg) > 35:
            die(f"{label}: text segment too long ({len(seg)}): {seg!r}")

def block_bounds(text: str, label: str):
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::\s*$", text))
    if len(matches) != 1:
        die(f"{label}: expected exactly one label, found {len(matches)}")
    start = matches[0].start()
    nxt = LABEL_RE.search(text, matches[0].end())
    end = nxt.start() if nxt else len(text)
    return start, end, text[start:end]

def replace_block(text: str, label: str, tr: str) -> str:
    start, end, old = block_bounds(text, label)
    if re.search(r"[А-Яа-яЁё]", old):
        die(f"{label}: target already contains Cyrillic; refusing overwrite")
    if ".string " not in old:
        die(f"{label}: target is not a runtime text block")
    safe = tr.replace('"', '\\"')
    return text[:start] + f'{label}::\n\t.string "{safe}"\n\n' + text[end:]

def validate_written(rel: Path, text: str) -> None:
    for lineno, line in enumerate(text.splitlines(), 1):
        if '.string "' in line and line.count('"') < 2:
            die(f"{rel}:{lineno}: broken assembler string")
    if re.search(r"\\\\[npl]", text):
        die(f"{rel}: doubled FireRed runtime escape")

def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    total = 0
    by_file = {}
    translated = []
    for rel_s, patches in FILES.items():
        path = root / rel_s
        if not path.is_file():
            die(f"missing target: {rel_s}")
        text = path.read_text(encoding="utf-8")
        for label, tr in patches.items():
            validate_translation(label, tr)
            text = replace_block(text, label, tr)
            translated.append(label)
        validate_written(Path(rel_s), text)
        path.write_text(text, encoding="utf-8")
        by_file[rel_s] = len(patches)
        total += len(patches)
    if total != EXPECTED_TOTAL:
        die(f"expected {EXPECTED_TOTAL} blocks, got {total}")

    out = root / "build" / "qarro_ru_residual_runtime_v3_134_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "marker": MARKER,
        "sourceAudit": "RU runtime #230 / v3.133 / 5f9cdd22600ff36aab35a0a21c33b85ee3aa7279",
        "expectedPreEnglishOnlyBlocks": EXPECTED_PRE_BLOCKS,
        "expectedPostEnglishOnlyBlocks": EXPECTED_POST_BLOCKS,
        "translatedBlockCount": total,
        "translatedFileCount": len(by_file),
        "translatedByFile": by_file,
        "translatedLabels": translated,
        "pokemonSpeciesNamesRemainEnglish": True,
        "moveNamesRemainEnglish": True,
        "abilityNamesRemainEnglish": True,
        "gameplayLogicTouched": False,
        "trainerDataTouched": False,
        "rewardInventoryFlagLogicTouched": False,
        "ashBondTouched": False,
        "ashCapTouched": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[{MARKER}] PASS: localized {total} residual runtime blocks in {len(by_file)} files; gameplay/trainer/reward/Ash untouched")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
