#!/usr/bin/env python3
"""Qarro v3.132: Kanto 6v6 A/B/C with save-stable per-Gym selection.

Variant A stays on the already-green story Leader IDs. Sixteen private B/C IDs
624..639 hold the other final-canon rosters. Two bits per Gym are stored in the
otherwise-unused FireRed var 0x40AF. First selection is seeded from the save
Trainer ID, so defeat/reset cannot reroll even before a manual save.

5-of-6 remains retired. E4/Champion/rematches/ordinary trainers/localization/
font/Ash Bond/Ash Cap are outside this pass.
"""
from __future__ import annotations
import base64, json, re, sys, zlib
from pathlib import Path

MARKER="QARRO_GYM_ABC_V3_132"
OLD_COUNT=624
NEW_COUNT=640
BANNED={"Regirock","Suicune","Zapdos","Virizion","Darkrai","Mewtwo","Moltres","Groudon"}
CFG=json.loads(zlib.decompress(base64.b85decode('c-rk;TXUm268<ZcpEKvgmpGn0txc{oxgFz^*{z+aDH+Q~WsJN6l5tMWf8UmbKwtsM`jW}+KBR(e0e$_t)oSUlMugEKY@Gbn7!CVZw`arefAojLyYJU${Zsfb7~a{RzYqBDv(=(;(mZH9B1TXUHBK6X#z6zQ7_LSuh5`~H2H%iJ7}h#y;K%RdcrwE<@({j_Fn<kvzeFrrHBSE7xS&2>d=0MgBlb_MX8UV!^$@~E%euU`e&_%D(Oh1f;;FoFmVI?`sxI)?pg%zipvk&LQOx+~G4V;XI<Xx1JXw7WKEM@5e&kt0>dyJ+Ga$qJSB&PEf8yU-j!!1pr+ey?&;y1(qj4P3Ww>Kf2PlesZ1vfKGET%76k#?+zQ0aiALzC|;YjfHMA;;?PEi1wIA}Ot?9P3h(c0O7RvR%qjr}UIj_42K3V8-DWrDhUMkDM-DcK{s7z1T@3lxHdY=^QNI>Dhy-yZh;OomR(ru_evi>(0|x)5IA5)2Bsr%#w^^a6=CLlfe!tiM^;cpA}1%rvDRZ6rv4VUi+c3+t32668cV#4dj~zq}wbl#R%d4)msO2Nc^LUHY6$##R~8-JLiU3MN22O9X1OIB>mnE6sZtFfpS+VyEAJ9#r9tZN?jWGrZBIWzcVXCytUARS|^BL^tx{V1gN7z$16+p|_gQV8{4#O=eyckYEP1OzIHw2G5X3S)dbp&v^lA`<T%Qa-)^M9bf-MeelUOdhZzy!<gYZ!&Bs)qhO}6fM356Bwem1jDoBd%OWrdvNKqc_c=hK_vX-)hanSCWgxm9F1x>KxGaUCn=5DZ4=wF!nbRHzjAucx0-<gR2(>j3N^UXh@uLz{HxX1<3973E)m4J(DnWInphjdtChKAnUm)MI6HiIJL5RXd{-mJBAzH#yoFxf(F5%OsF&OLCX&q4CK<W_BaDW+#Xr8?LaOHZ^;2a-;V(+F?14!CFU4>u+K<*b0ByU|}Hcshn9d1Bx2?9BD0v>uzf_cGTrDqct>=W)sEH%l24}c@({7jj=1xWuRMzfGGyd7$<7E4H6*U9}eKu<_oK`Pq<#%G2gd>lx-MoWe=wYQoZ5LSke!ga0wIHX)*=BzDI_L%xYe)pJh9vv!h`~fW?_tYX}tF?9OTq9D6P^a<>k;+$SSOYM&8DQ*90OlH=5wl?XPHPSn51<f}RK)kr6Ny}}M3u^K3l_E!jXSfjD%jr0Szia+ia4Y3CEl9=_nh!_XB#A%75`eaR+JjuwfSqfYjw!m0jO*g@=C$wdi34-b9iy4B`|Gs0(0gA+vE{KPXaNm!yLr)GK}eH7&An~^<pk0GR4-N9%fZ4+B%dng8x!Ra3N&`7g9#z;#6ILSkCy39rbhPu+l@;rYi*(Ij3$MW&!sCFebD<2UL8zg>P5Zy-&H$`-`QA7!7yHMCs%pLXp&SHTe#i1po)ia5Z!l2r3{yqrbZa`o)cc{L|fG{|%Z2IHEjSojno?kHy>N;zgz;sen0|oIDgY0Xpz38wCLk4BTCk$pi;!Nk(`S%z&PsjXWLii>C(?fxSQ?&q!2nUN7KDpakdX#}cy$6v`i@*y?S8EqQ}tt0d*Vp#YUI6D5yW0yv<m4c<G$%F^ytMJ1ow+Th@!D3ZMZH*GU++W*H*9XCNm5f;7+VkNGa>$u??uvEaI0z(Dcc04qpPu3u*6qrn%(aBrDkVAp)C8KmIXNV-JmKLV%BNPYGdJtHTV%_%@#coi*Wl!8vgF60Ie57Df5Fr*g@|ddJ{g1-u+3@OfU&}c==A82Z2XTmERl09=a>&{2X3%-0LFWVU@zReMT!sUY5<5P>B^6>@%^_NyM2H<F#EueTM+vc`gxJx9*h{3}6GAUb+0Uj^P$%4$tajx~qmn3VKo>G4@-bd=Lr^8RRS<bNBq1;lCg6im>B2bK*cUst=Tk<P-b%t@k((0o4OVVrACHNdm(~_|kw5niUo~ycv!l(b^h#GgB|ZCrXS0~Qi6KnyfRi#zEht8#y;?^FwcH~J;9@mavC!V4VI`A;lEtr6w&FEXNv86bYm8mbaxfOa`u7ixOTY=%yhEXcQ45`Y*;COw0OBL>RbF2Qm$n%$?M>mbN_@?CBt8%x3TEQQH^s?9rRL>6$Uj5+ENeL2un8nN7>}{PGk}pdDBYB<pcS;EuZ&4YMN=MX<r<n3yK}Y1EAWVt5OV)dh_`lpiWd-@r_<e`f1ah1?54<2K`VLWapG|pktmLE*1b{_#@g>FjHUU~c2RSG2~sI;e!jcVv&<uNmI(>#7)1&+^9v`fqgD!<T@5tlJ*5d|I{iq>zb#e%ZK?8aOO=0Hs{GsPYVw2kR@(1X5b!<)K4;>x7%)(!H6Tpb>z^M+vFx`PQYxoYVkRhKC0)=mfZQJ0CDuA3L4+sp>OheFM+~zImf^@Cp26Sqvq{~872x0t#?O4ZRVMo0Hh8G8S$GeDIjou#`5*2+d?De|V6f+W8kbIJ@A)L%S;9m3D((~Ur+m$5_gs`M@m>WH*HOZWvm|pIrmMNy=UlUdGNV3t(S(LTzMQr@VkKJ<|8X0{!yOd?=_-KPP(YB0V!h!gi#^52#LEcryi5U|!`<`XM8uu1tV^0K<m5?}wI?UQXudY#2Cxrt4eZ%w*t0i+y*lSReh<!fOD6PRF~)&0tJ)F<_A9%*1a>nQn|iq<A3Qb}S48xdK+)$_8H0MiY783TAVMySMOwRS+DihFESV;2x><Kq+R|jg6>V9%0y*}9ew!jkO&+iv@Y`t~P>Ov{e=xkd)w8~?IqU2DXpWwRHU$9oasb%YCd)bis=G|k(Mgm3ULv-h5?fD+t*6A+Q)26_LkI5#IPBG}LxOEy#E2D}0E%_={2GQ>oxLH!q^5ykJG{u&hr`}0X3MW_<@>Y>ewfpcPG^7W(92iXAW4AB&m;_s0Iu<rTOPYyErSw0bhfI8iWPc2qtfV14aQ(h#d2u4lxutjHjeh~8Uq?9V4@pRp8gw15_vY`#6i(FZt#<tk?#H&feEhbF&dEPA|HL2^24njX1Ho<Ukj4986@ouL9)sa+V9N}*l%zt){?|hpJn@K^(O3`6F*8qAfEckt|>{A<1$ER3p@@G@0PhoA+M2F#;wl#id&_=*?C94nRQ<75HMeY`x`W8UVw7Y1RHH?D>#|7Oe$TJ_143*XfjnZJx(@-JXd_OeHvoRhB+aUO)1h{{G{>zWjj0u*ZfN@qdYFjD4B}@MpU0qJKyKiX_>+D7Ve0Uk9jfW62p8>ZunAiRI`b8Qc!KH0(V=j_qSE0xUJUv+lOYG?$#wSGzRgk&z>FXBQ{POVRO^&e0yXf0i#81g%j08+pAfy$XB<{fqu>piNuuR>_^1#LiCKt0)L^oL2k8^J%=uQX->_K4!6Nj(j8oxB8#RG2xM{_?KOHtAaGHy&*4jP$DrDmF<LD>@B@<TzXHCdTV~~DRt8ojG4qVY%ZSKE$-KQ4LP24f`jYoPQECijN6q~)BAY$WiNyKL55x{u#OAz7G{o!N71$9q2P8_t>+H04;4>vCnrElrF$D+FE38`XR12ZD8A9z1A+$<_JAs`YitwPp$B<`8kaow;D?K%DzkR~82wHGewMbJH2(|+@dk+K)u^D`=O?#ivS!~p<M9o4Uq87IQ`!KXRhuRK`?k9&TMbL|@yNCYm?Uj~>_RMK0U*6#J3WcG~9EKh>OE6TN8(_3>H5F+$6Y({b_?k+5O(njj5?|BkuSs1Pu6Sj6A14e{F7|APwPY4kU~Si{KR1ZcC&ZT_MlemA!&E2M80)@)&V*9H{S5j#rSaIuAI>HcSDlDLY*3$sqbPmxQ!qk53FhlL_gnBK4(1rfp`q6~&q#jxsBqeja!aEf9={_y)B+2SBxJdyPm_{z-%)QHjL8DRkvajQE6W*WjSYo!RH_t~D{SQas~(4KGY;Du;_zuaix{EiC5>G|aY;_wXE;FCh@oYzFbi#e1-v??!O}w|X7UyxCOeoa&lR_I$4d&71((jVR2^Ho?>DwoBm>>|oD8VLGt5SKynn3vkIvbsj3m8x8cDwW1jO|qc>tAgWNmT;MGFkmP=3zW*T9CPAmklDNSx5b{Mpywp1A2Z1IEojet&`abNOlmKi=*p4*59wL1rS!kw7QbEd@rdct0@aXRe?LOvWEM%Okb|fm`Q@fJOeE{Qf|YWE!;4N(mGPbkq}gLwJ^7LEt%Fh>ur1Du7tyB{y9vYh+uayPeW~J^IZOn^@~<zmE7h7@)>l`5K4^GR|Y)=c%E;MMgR)BVv0*Jrie)%+V_paJkw!4@W5vyl1bTh0k<`UaW%x{d-`io3fLvFxPYBpfMxC25Q*@TgMp|i8|&Bz{p3u`t|E-s+Y2)654vEE(m=@K|re5;^(Km8CwuR#wf%pe5m|gKQA%??!r$3!4qsO{G>MeCxBD<RUl8|$AzD`Lnkg#_$Bd;#ITA~3JXg#RQOG)iZhzbIAp9Gh%+mz4&^=QwmRPq8cn-qq|HYj!N^wmGu4TAFtW=>+BGA^Gml|pyZo8jIW#c1#|PW>gT<3S!r)H%lhsz^gKqnfkF;w>@@KZ2F!HGUnaREq7}(+i?dpNziES9zEq`Lxwg_Xnrn+|RSn*u0tK$m&tF>zw%9V9&*9{d<<=X0%KUFJ6!eFkgo?Sm!JozJ^S)=dx#}c~{p6I7Z=loPV)s<0xR$qDybne(t{bbwhl+NrBOzn`##<%q&VYOL)4hpoh*0Q(rQ=TJ=C+R_C*<oMWNmbb)J6Vfm_G&eL{lzKJXy=J!?@kY!5G#iKXprnw4efB8+z|rWNe>wT+Ry7WNI27WnPvo}C3bDYZElOAzL8AZ=a=r2%ScFXUnf9-rnYY(dw;rHA=!c;o3OP`=3HaBw#6oUZ}N!sw<<u^n&Gk+Yb|iHuT5(T)AxXD9X+x~DSL7Hi1k+|aIY<knnkWHjH=bnbXiJU&(V4owAZV9*I%DT6s?w}6OdN0(o#oS9pEJ$S*yy5J9<4Zdw=?vpFe;88|1qgxB')).decode("utf-8"))
TEAMS=CFG["teams"]
HEADERS={int(k):v for k,v in CFG["headers"].items()}
A_EXPECTED=CFG["a_expected"]
VARIANTS=CFG["variants"]

ORIGINAL_CREATE_PARTY='''static void CreateNPCTrainerParty(struct Pokemon *party, u16 trainerNum)
{
    if (!GetTrainerStructFromId(trainerNum)->overrideTrainer)
    {
        CreateNPCTrainerPartyFromTrainer(party, GetTrainerStructFromId(trainerNum));
        return;
    }

    struct Trainer tempTrainer;
    memcpy(&tempTrainer, GetTrainerStructFromId(trainerNum), sizeof(struct Trainer));
    const struct Trainer *origTrainer = GetTrainerStructFromId(tempTrainer.overrideTrainer);

    tempTrainer.party = origTrainer->party;
    tempTrainer.poolSize = origTrainer->poolSize;
    if (tempTrainer.partySize == 0)
        tempTrainer.partySize = origTrainer->partySize;
    CreateNPCTrainerPartyFromTrainer(party, (const struct Trainer *)(&tempTrainer));
}
'''

SELECTOR=r'''// QARRO_GYM_ABC_V3_132_BEGIN
#define QARRO_GYM_VARIANT_VAR 0x40AF

static u8 GetQarroKantoGymIndex(u16 trainerNum)
{
    switch (trainerNum)
    {
    case TRAINER_LEADER_BROCK:    return 0;
    case TRAINER_LEADER_MISTY:    return 1;
    case TRAINER_LEADER_LT_SURGE: return 2;
    case TRAINER_LEADER_ERIKA:    return 3;
    case TRAINER_LEADER_KOGA:     return 4;
    case TRAINER_LEADER_SABRINA:  return 5;
    case TRAINER_LEADER_BLAINE:   return 6;
    case TRAINER_LEADER_GIOVANNI: return 7;
    default:                       return 0xFF;
    }
}

static u8 GetQarroKantoGymVariant(u16 trainerNum)
{
    u8 gymIndex = GetQarroKantoGymIndex(trainerNum);
    u8 shift;
    u8 variant;
    u16 packed;
    u32 seed;

    if (gymIndex == 0xFF)
        return 1;

    shift = gymIndex * 2;
    packed = VarGet(QARRO_GYM_VARIANT_VAR);
    variant = (packed >> shift) & 3;
    if (variant < 1 || variant > 3)
    {
        seed = READ_OTID_FROM_SAVE;
        seed ^= (u32)(gymIndex + 1) * 0x9E3779B9;
        seed ^= seed >> 16;
        seed *= 0x7FEB352D;
        seed ^= seed >> 15;
        variant = (seed % 3) + 1;
        packed &= ~((u16)3 << shift);
        packed |= (u16)variant << shift;
        VarSet(QARRO_GYM_VARIANT_VAR, packed);
    }
    return variant;
}

static u16 GetQarroKantoGymVariantTrainer(u16 trainerNum)
{
    u8 variant = GetQarroKantoGymVariant(trainerNum);
    if (variant == 1)
        return trainerNum;
    switch (trainerNum)
    {
    case TRAINER_LEADER_BROCK:
        return variant == 2 ? TRAINER_QARRO_LEADER_BROCK_B : TRAINER_QARRO_LEADER_BROCK_C;
    case TRAINER_LEADER_MISTY:
        return variant == 2 ? TRAINER_QARRO_LEADER_MISTY_B : TRAINER_QARRO_LEADER_MISTY_C;
    case TRAINER_LEADER_LT_SURGE:
        return variant == 2 ? TRAINER_QARRO_LEADER_LT_SURGE_B : TRAINER_QARRO_LEADER_LT_SURGE_C;
    case TRAINER_LEADER_ERIKA:
        return variant == 2 ? TRAINER_QARRO_LEADER_ERIKA_B : TRAINER_QARRO_LEADER_ERIKA_C;
    case TRAINER_LEADER_KOGA:
        return variant == 2 ? TRAINER_QARRO_LEADER_KOGA_B : TRAINER_QARRO_LEADER_KOGA_C;
    case TRAINER_LEADER_SABRINA:
        return variant == 2 ? TRAINER_QARRO_LEADER_SABRINA_B : TRAINER_QARRO_LEADER_SABRINA_C;
    case TRAINER_LEADER_BLAINE:
        return variant == 2 ? TRAINER_QARRO_LEADER_BLAINE_B : TRAINER_QARRO_LEADER_BLAINE_C;
    case TRAINER_LEADER_GIOVANNI:
        return variant == 2 ? TRAINER_QARRO_LEADER_GIOVANNI_B : TRAINER_QARRO_LEADER_GIOVANNI_C;
    default:
        return trainerNum;
    }
}

static void CreateNPCTrainerParty(struct Pokemon *party, u16 trainerNum)
{
    trainerNum = GetQarroKantoGymVariantTrainer(trainerNum);
    if (!GetTrainerStructFromId(trainerNum)->overrideTrainer)
    {
        CreateNPCTrainerPartyFromTrainer(party, GetTrainerStructFromId(trainerNum));
        return;
    }

    struct Trainer tempTrainer;
    memcpy(&tempTrainer, GetTrainerStructFromId(trainerNum), sizeof(struct Trainer));
    const struct Trainer *origTrainer = GetTrainerStructFromId(tempTrainer.overrideTrainer);
    tempTrainer.party = origTrainer->party;
    tempTrainer.poolSize = origTrainer->poolSize;
    if (tempTrainer.partySize == 0)
        tempTrainer.partySize = origTrainer->partySize;
    CreateNPCTrainerPartyFromTrainer(party, (const struct Trainer *)(&tempTrainer));
}
// QARRO_GYM_ABC_V3_132_END
'''

CONSTANTS='''#define TRAINER_QARRO_LEADER_BROCK_B               624
#define TRAINER_QARRO_LEADER_BROCK_C               625
#define TRAINER_QARRO_LEADER_MISTY_B               626
#define TRAINER_QARRO_LEADER_MISTY_C               627
#define TRAINER_QARRO_LEADER_LT_SURGE_B            628
#define TRAINER_QARRO_LEADER_LT_SURGE_C            629
#define TRAINER_QARRO_LEADER_ERIKA_B               630
#define TRAINER_QARRO_LEADER_ERIKA_C               631
#define TRAINER_QARRO_LEADER_KOGA_B                632
#define TRAINER_QARRO_LEADER_KOGA_C                633
#define TRAINER_QARRO_LEADER_SABRINA_B             634
#define TRAINER_QARRO_LEADER_SABRINA_C             635
#define TRAINER_QARRO_LEADER_BLAINE_B              636
#define TRAINER_QARRO_LEADER_BLAINE_C              637
#define TRAINER_QARRO_LEADER_GIOVANNI_B            638
#define TRAINER_QARRO_LEADER_GIOVANNI_C            639
'''

def die(msg:str)->None:
    raise SystemExit(f"[{MARKER}] ERROR: {msg}")

def trainer_block(text:str, trainer:str):
    token=f"=== {trainer} ==="
    start=text.find(token)
    if start<0: die(f"trainer block missing: {trainer}")
    nxt=text.find("\n=== ",start+len(token))
    return start, len(text) if nxt<0 else nxt, text[start:] if nxt<0 else text[start:nxt]

def party_species(block:str):
    parts=block.split("\n\n",1)
    if len(parts)!=2: die("trainer block missing metadata/body separator")
    out=[]
    for line in parts[1].splitlines():
        if not line or line.startswith(("Level:","IVs:","EVs:","Ability:","- ")) or line.endswith(" Nature"):
            continue
        out.append(line.split(" @ ",1)[0])
    return out

def item_count(block:str):
    parts=block.split("\n\n",1)
    if len(parts)!=2: return 0
    return sum(" @ " in line for line in parts[1].splitlines()
               if line and not line.startswith(("Level:","IVs:","EVs:","Ability:","- ")) and not line.endswith(" Nature"))

def assert_var_unused(root:Path):
    allowed=root/"include/constants/vars_frlg.h"
    hits=[]
    for base in (root/"src",root/"data",root/"include"):
        if not base.exists(): continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".c",".h",".inc",".s"}: continue
            try: text=path.read_text(encoding="utf-8")
            except UnicodeDecodeError: continue
            if path==allowed: continue
            if "VAR_0x40AF" in text or re.search(r"(?<![0-9A-Fa-f])0x40AF(?![0-9A-Fa-f])",text):
                hits.append(str(path.relative_to(root)))
    if hits: die(f"save var 0x40AF already used: {hits[:8]}")

def patch_opponents(path:Path):
    text=path.read_text(encoding="utf-8")
    if "TRAINER_QARRO_LEADER_BROCK_B" in text: die("variant trainer constants already present")
    m=re.search(r"(?m)^#define TRAINERS_COUNT_FRLG\s+(\d+)\s*$",text)
    if not m or int(m.group(1))!=OLD_COUNT: die(f"expected TRAINERS_COUNT_FRLG={OLD_COUNT}")
    anchor="#define TRAINER_CUE_BALL_PAXTON                    623\n"
    if text.count(anchor)!=1: die("Paxton trainer-ID anchor drifted")
    text=text.replace(anchor,anchor+CONSTANTS+"\n",1)
    text,n=re.subn(r"(?m)^#define TRAINERS_COUNT_FRLG\s+624\s*$",
                   "#define TRAINERS_COUNT_FRLG                  640",text,count=1)
    if n!=1: die("failed to set TRAINERS_COUNT_FRLG=640")
    path.write_text(text,encoding="utf-8")

def append_parties(path:Path):
    text=path.read_text(encoding="utf-8")
    for trainer,cfg in A_EXPECTED.items():
        _,_,block=trainer_block(text,trainer)
        if party_species(block)!=cfg["roster"]:
            die(f"{trainer} Variant A roster drifted")
    reports=[]
    chunks=[]
    for trainer,cfg in TEAMS.items():
        if f"=== {trainer} ===" in text: die(f"duplicate variant block {trainer}")
        block=f"=== {trainer} ===\n{HEADERS[cfg['gym']]}\n\n" + "\n\n".join(cfg["party"]) + "\n"
        species=party_species(block)
        expected=[x.splitlines()[0].split(" @ ",1)[0] for x in cfg["party"]]
        if species!=expected or len(species)!=6: die(f"{trainer} roster parse mismatch")
        if cfg["ace"] not in species: die(f"{trainer} missing Ace")
        if set(species)&BANNED: die(f"{trainer} contains banned legacy boss species")
        if item_count(block)!=cfg["items"]: die(f"{trainer} held item budget mismatch")
        chunks.append(block)
        reports.append({"trainer":trainer,"gym":cfg["gym"],"variant":cfg["variant"],
                        "partySize":6,"roster":species,"ace":cfg["ace"],"iv":cfg["iv"],
                        "evBudgetPerPokemon":cfg["ev_budget"],"meaningfulHeldItems":cfg["items"]})
    if not text.endswith("\n"): text+="\n"
    path.write_text(text+"\n"+"\n".join(chunks),encoding="utf-8")
    return reports

def patch_selector(path:Path):
    text=path.read_text(encoding="utf-8")
    if "QARRO_GYM_ABC_V3_132_BEGIN" in text: die("A/B/C selector already present")
    if "TryCreateQarroFiveOfSixGymParty" in text or "QARRO_GYM_FIVE_V3_26" in text:
        die("historical 5-of-6 selector reappeared")
    if text.count(ORIGINAL_CREATE_PARTY)!=1: die("native CreateNPCTrainerParty shape drifted")
    path.write_text(text.replace(ORIGINAL_CREATE_PARTY,SELECTOR.rstrip()+"\n",1),encoding="utf-8")

def main():
    if len(sys.argv)!=2:
        print(f"usage: {Path(sys.argv[0]).name} <upstream-root>",file=sys.stderr); return 2
    root=Path(sys.argv[1]).resolve()
    party=root/"src/data/trainers_frlg.party"
    opponents=root/"include/constants/opponents_frlg.h"
    battle=root/"src/battle_setup.c"
    varsfile=root/"include/constants/vars_frlg.h"
    for p in (party,opponents,battle,varsfile):
        if not p.is_file(): die(f"missing required source {p}")
    if "#define VAR_0x40AF                 0x40AF" not in varsfile.read_text(encoding="utf-8"):
        die("expected FireRed VAR_0x40AF definition missing")
    assert_var_unused(root)
    patch_opponents(opponents)
    reports=append_parties(party)
    patch_selector(battle)

    final_opp=opponents.read_text(encoding="utf-8")
    if "#define TRAINERS_COUNT_FRLG                  640" not in final_opp: die("final trainer count mismatch")
    final_battle=battle.read_text(encoding="utf-8")
    for token in ("QARRO_GYM_ABC_V3_132_BEGIN","QARRO_GYM_VARIANT_VAR 0x40AF","READ_OTID_FROM_SAVE",
                  "VarGet(QARRO_GYM_VARIANT_VAR)","VarSet(QARRO_GYM_VARIANT_VAR, packed)",
                  "TRAINER_QARRO_LEADER_BROCK_B","TRAINER_QARRO_LEADER_GIOVANNI_C"):
        if token not in final_battle: die(f"selector token missing: {token}")
    if "TryCreateQarroFiveOfSixGymParty" in final_battle: die("5-of-6 survived")

    out=root/"build/qarro_gym_abc_v3_132_audit.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({"marker":MARKER,"mode":"Kanto final 6v6 A/B/C",
        "variantATrainersUnchanged":list(A_EXPECTED),"variantBCParties":reports,
        "variantBCPartyCount":len(reports),"totalKantoVariants":len(A_EXPECTED)+len(reports),
        "saveVariantVar":"0x40AF","bitsPerGym":2,
        "selection":"save-Trainer-ID-seeded A/B/C, stored on first encounter",
        "resetStableBeforeManualSave":True,"lossDoesNotReroll":True,
        "legacyFiveOfSixRuntimeSelector":False,"trainerCountBefore":OLD_COUNT,"trainerCountAfter":NEW_COUNT,
        "ashBondTouched":False,"ashCapTouched":False},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"[{MARKER}] PASS: 16 B/C parties + save-stable 8-Gym A/B/C selector; Variant A preserved")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
