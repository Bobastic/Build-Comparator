import pandas as pd
import numpy as np
import streamlit as st
from matplotlib.colors import LinearSegmentedColormap

EPW=pd.read_csv("data/EquipParamWeapon.csv").dropna(subset="Name").replace("Great epee","Great Épée",regex=True)
RPW=pd.read_csv("data/ReinforceParamWeapon.csv")
CCG=pd.read_csv("data/CalcCorrectGraph.csv")
AECP=pd.read_csv("data/AttackElementCorrectParam.csv")
PAA=pd.read_csv("data/Physical AtkAttribute.csv").dropna(subset="Weapon").replace("Miséricorde","Misericorde").replace("Varré's Bouquet","Varre's Bouquet")
RD=pd.read_csv("data/Raw_Data.csv").replace("Great Epee","Great Épée")

dmgTypes=["Standard","Strike","Slash","Pierce","Magic","Fire","Lightning","Holy"]
baseInfusions=["Heavy","Fire","Keen","Lightning","Magic","Cold","Sacred","Flame Art","Blood","Occult"]
infusionOrder=["Heavy","Hvy+Gse","Fire","Fire+FS","Keen","Keen+Gse","Lightning","Ltng+LS","Magic","Cold","Sacred","Scrd+SB","Flame Art","F.Art+FS","Blood","Poison","Occult","Standard","Std+Gse"]

idWeaponClass={
    29: "Halberds",
    25: "Spears",
    3: "Straight Swords",
    1: "Daggers",
    9: "Curved Swords",
    5: "Greatswords",
    7: "Colossal Swords",
    15: "Thrusting Swords",
    16: "Heavy Thrusting Swords",
    11: "Curved Greatswords",
    13: "Katanas",
    14: "Twinblades",
    21: "Hammers",
    23: "Greathammers",
    24: "Flails",
    17: "Axes",
    19: "Greataxes",
    28: "Great Spears",
    31: "Scythes",
    39: "Whips",
    35: "Fists",
    37: "Claws",
    41: "Colossal Weapons",
}
weaponClasses=idWeaponClass.values()
def weaponsOfClass(wClass:str)->list[str]:
    # returns a list of all weappons of the specified class
    classes={v:k for k,v in idWeaponClass.items()}
    tmp=EPW[EPW["wepType"]==classes[wClass.replace("2H ","")]]
    return [f"2H {w}" if "2H" in wClass else w for w in tmp[tmp["reinforceTypeId"].isin([0,2200])]["Name"]]

# Calculations

def ARcalculator(weapon:str,infusion:str,build:list[int],twoH:bool=False,reinforcmentLvl:any="max")->np.ndarray:
    """
    Calculates weapon AR
    Parameters:
        weapon: string
            Weapon name.
        infusion: string
            Infusion name. For standard use "".
        build: list of length 5
            STR, DEX, INT, FTH, ARC.
        twoH: boolean
            Is the weapon two handed?
        reinforcmentLvl: int or "max"
            Weapon reinforcment level.
    Output:
        numpy array of length 8
    """
    infusionOffset={
        "":0,
        "Heavy":100,
        "Keen":200,
        "Quality":300, # lmao
        "Fire":400,
        "Flame Art":500,
        "Lightning":600,
        "Sacred":700,
        "Magic":800,
        "Cold":900,
        "Poison":1000,
        "Blood":1100,
        "Occult":1200,
    }
    def CalcCorrectFormula(stat,ccgData):
        # used for stat scaling calculations
        for i in range(5):
            if ccgData.iloc[0,2+i]>stat:
                break
        statMin=ccgData.iloc[0,2+i-1]
        statMax=ccgData.iloc[0,2+i]
        ratio=(stat-statMin)/(statMax-statMin)
        expMin=ccgData.iloc[0,12+i-1]
        growth=ratio**expMin if expMin>0 else 1-(1-ratio)**abs(expMin)
        growthMin=ccgData.iloc[0,7+i-1]
        growthMax=ccgData.iloc[0,7+i]
        return (growthMin+(growthMax-growthMin)*growth)/100
    if "2H" in weapon:
        weapon=weapon.replace("2H ","")
        twoH=True
    if reinforcmentLvl=="max" or reinforcmentLvl>10:
        if reinforcmentLvl=="max": reinforcmentLvl=25
        reinforcmentLvl=min(reinforcmentLvl,RD[RD["Name"]==weapon]["Max Upgrade"].values[0])
    ID=EPW[EPW["Name"]==weapon]["ID"].values[0]+infusionOffset[infusion]
    rtID=EPW[EPW["ID"]==ID]["reinforceTypeId"].values[0]
    ccgID=EPW[EPW["ID"]==ID][["correctType_Physics","correctType_Magic","correctType_Fire","correctType_Thunder","correctType_Dark"]].values[0]
    aecID=EPW[EPW["ID"]==ID]["attackElementCorrectId"].values[0]
    baseDmg=EPW[EPW["ID"]==ID][["attackBasePhysics","attackBaseMagic","attackBaseFire","attackBaseThunder","attackBaseDark"]].to_numpy()[0]
    baseScaling=EPW[EPW["ID"]==ID][["correctStrength","correctAgility","correctMagic","correctFaith","correctLuck"]].to_numpy()[0]/100
    baseDmgReinforcment=RPW[RPW["ID"]==rtID+reinforcmentLvl][["Physical Attack","Magic Attack","Fire Attack","Lightning Attack","Holy Attack"]].to_numpy()[0]
    baseScalingReinforcment=RPW[RPW["ID"]==rtID+reinforcmentLvl][["Str Scaling","Dex Scaling","Int Scaling","Fai Scaling","Arc Scaling"]].to_numpy()[0]
    dmg=baseDmg*baseDmgReinforcment # element
    scaling=baseScaling*baseScalingReinforcment # stat
    tmp=baseDmg*baseDmgReinforcment
    for i in range(5): #element
        if dmg[i]:
            for j in range(5): #stat
                if AECP[AECP["Row ID"]==aecID].iloc[0,1+5*i+j]:
                    stat=build[j] if (j!=0 or not twoH) else int(build[j]*1.5)
                    tmp[i]+=dmg[i]*scaling[j]*CalcCorrectFormula(stat,CCG[CCG["ID"]==ccgID[i]])
    # convert 5-array into 8-array
    physType={"Standard":0,"Strike":1,"Slash":2,"Pierce":3}[PAA[PAA["Weapon"]==weapon]["1h R1 1"].values[0]]
    res=np.concatenate([[0,0,0,0],tmp[1:]])
    res[physType]=tmp[0]
    return(res)

def ARtoDMG(AR:list[int],defenses:list[int],negations:list[int])->np.ndarray:
    """
    Converts an AR array to a real damage array
    Parameters:
        AR: list of length 8
            AR for each damage type.
        defenses: list of length 8
            Defenses for each damage type.
        negations: list of length 8
            Negations for each damage type.
    Output:
        numpy array of length 8
    """
    res=[]
    for ar,d,n in zip(AR,defenses,negations):
        n/=100
        if d>ar*8:
            res.append((1-n)*0.1*ar) 
        elif d>ar:
            res.append((1-n)*(19.2/49*(ar/d-0.125)**2+0.1)*ar)
        elif d>ar*0.4:
            res.append((1-n)*(-0.4/3*(ar/d-2.5)**2+0.7)*ar)
        elif d>ar/8:
            res.append((1-n)*(-0.8/121*(ar/d-8)**2+0.9)*ar)
        else:
            res.append((1-n)*0.9*ar)
    return np.array(res)

def DMGtable(weapons:list[str],builds:dict[str,list[int]],infusions:dict[str,list[int]],defenses:list[int],negations:list[int],weaponBuffs:bool=True,counterHits:bool=True)->pd.DataFrame:
    """
    Computes damage for each weapon/infusion/build combination.
    Parameters:
        weapons: list of string
            List of weapon names.
        builds: dict {string:list of int of length 5}
            Dict of builds with the keys being build name and values being STR DEX INT FTH ARC.
        infusions: dict {string:list of strings}
            Dict to specify what infusions we want for each build. Keys are build names and values are list of infusions.
        defenses: list of length 8
            Defenses for each damage type.
        negations: list of length 8
            Negations for each damage type.
        weaponBuffs: boolean
            Display weapon buffs like greases or Flaming Strike/Sacred Blade.
        counterHits: boolean
            Display counter hit damage and spear tali counter hit damage
    """
    noAshBuff={
        "Fire":["Whips","Colossal Swords","Colossal Weapons"],
        "Flame Art":["Whips","Colossal Swords","Colossal Weapons"],
        "Lightning":["Halberds","Spears","Great Spears","Scythes","Whips","Fists","Claws"],
        "Sacred":["Whips","Fists","Claws"]
    }
    buffs={
        "Heavy":["Hvy+Gse",np.array([0,0,0,0,0,0,110,0])],
        "Fire":["Fire+FS",np.array([0,0,0,0,0,90,0,0])],
        "Keen":["Keen+Gse",np.array([0,0,0,0,0,0,110,0])],
        "Lightning":["Ltng+LS",np.array([0,0,0,0,0,0,90,0])],
        "Sacred":["Scrd+SB",np.array([0,0,0,0,0,0,0,90])],
        "Flame Art":["F.Art+FS",np.array([0,0,0,0,0,90,0,0])],
        # buffable split dmg weapons
        "Treespear":np.array([0,0,0,0,0,0,0,110]),
        "Great Club":np.array([0,0,0,0,0,110,0,0]),
        "Troll's Hammer":np.array([0,0,0,0,0,110,0,0]),
        "Clayman's Harpoon":np.array([0,0,0,0,110,0,0,0]),
    }
    res=[]
    for weapon in weapons:
        if EPW[EPW["Name"]==weapon.replace("2H ","")].empty:
            print(f"Weapon does not exist: {weapon}")
            continue
        weaponClass=idWeaponClass[EPW[EPW['Name']==weapon.replace('2H ','')]['wepType'].values[0]]
        columns=[]
        normal,prc,spr=[],[],[]
        for build in builds:
            # somber weapons
            if RD[RD["Name"]==weapon.replace("2H ","")]["Infusable"].values[0]=="No":
                dmg=ARtoDMG(ARcalculator(weapon,"",builds[build]),defenses,negations)
                normal.append(dmg.sum())
                if counterHits and dmg[3]:
                    prc.append((dmg*np.array([1,1,1,1.15,1,1,1,1])).sum())
                    spr.append((dmg*np.array([1,1,1,1.15*1.15,1,1,1,1])).sum())
                columns.append((f"{build} • {' '.join(map(str,builds[build]))}","Standard"))
                # if buffable (bhf, bouquet, ripple*2, treespear, great club, troll's hammer)
                if weaponBuffs and EPW[EPW["Name"]==weapon.replace("2H ","")]["isEnhance"].values[0]==1:
                    grease=buffs[weapon] if weapon in buffs else np.array([0,0,0,0,0,0,110,0])
                    dmg=ARtoDMG(ARcalculator(weapon,"",builds[build])+grease,defenses,negations)
                    normal.append(dmg.sum())
                    if counterHits and dmg[3]:
                        prc.append((dmg*np.array([1,1,1,1.15,1,1,1,1])).sum())
                        spr.append((dmg*np.array([1,1,1,1.15*1.15,1,1,1,1])).sum())
                    columns.append((f"{build} • {' '.join(map(str,builds[build]))}","Std+Gse"))
            # infusable weapons
            else:
                for infusion in infusions[build]:
                    dmg=ARtoDMG(ARcalculator(weapon,infusion,builds[build]),defenses,negations)
                    normal.append(dmg.sum())
                    if counterHits and dmg[3]:
                        prc.append((dmg*np.array([1,1,1,1.15,1,1,1,1])).sum())
                        spr.append((dmg*np.array([1,1,1,1.15*1.15,1,1,1,1])).sum())
                    columns.append((f"{build} • {' '.join(map(str,builds[build]))}",infusion))
                    # compute buffs (grease, flaming strike etc)
                    if weaponBuffs and (infusion in buffs):
                        if (infusion in noAshBuff) and (weaponClass in noAshBuff[infusion]):
                            continue
                        grease=buffs[weapon] if weapon in buffs else buffs[infusion][1]
                        dmg=ARtoDMG(ARcalculator(weapon,infusion,builds[build])+grease,defenses,negations)
                        normal.append(dmg.sum())
                        if counterHits and dmg[3]:
                            prc.append((dmg*np.array([1,1,1,1.15,1,1,1,1])).sum())
                            spr.append((dmg*np.array([1,1,1,1.15*1.15,1,1,1,1])).sum())
                        columns.append((f"{build} • {' '.join(map(str,builds[build]))}",buffs[infusion][0]))
        if columns:
            res.append(pd.DataFrame([normal,prc,spr],index=pd.MultiIndex.from_tuples([(weapon,"No Prc"),(weapon,"Prc+15%"),(weapon,"Prc+32%")]),columns=pd.MultiIndex.from_tuples(columns)))
    res=pd.concat(res).dropna(how="all")
    # reorder columns to respect infusion order
    res=res.sort_index(axis=1,level=1,sort_remaining=False,key=lambda x:x.map({a:i for i,a in enumerate(infusionOrder)}))
    res=res.sort_index(axis=1,level=0,sort_remaining=False,key=lambda x:x.map({a:i for i,a in enumerate(res.columns.get_level_values(0).unique())}))
    # add weapon class to index
    res.index=pd.MultiIndex.from_tuples([(f"{'2H ' if '2H' in w else ''}{idWeaponClass[EPW[EPW['Name']==w.replace('2H ','')]['wepType'].values[0]]}",w,d) for w,d in res.index])
    # put weapons of the same class next to each other (doesnt work)
    #res=res.sort_index(level=[0,1],key=lambda x:x.map({w:EPW[EPW["Name"]==w.replace("2H ","")]["wepType"].values[0] for w in res.index.get_level_values(0).unique()}))
    return res

def fancyTable(DMGtable:pd.DataFrame,comparison:str="row",displayPercentage:bool=True,showStats:bool=True,multicolor:bool=True,showWeaponClass:bool=True,wideDisplay:bool=False,saveOutput:bool=False)->None:
    """
    Displays a fancy damage table.
    Parameters:
        DMGtable: MultiIndexed pandas DataFrame
            Columns are build>infusion. Rows are weapon name>pierce bonus
        comparison: "row", "class", "all"
            Compute the difference ratio between cell damage and max row/weapon class/all damage.
        displayPercentage: boolean
            Display percentage value in cell.
        showStats: boolean
            Display build stat spread in column header.
        multicolor: boolean
            Display one color per build.
        showWeaponClass: boolean
            Display weapon class.
        wideDisplay: boolean
            Display a scrollable table instead of wider cells.
        saveOutput: boolean
            Save output as png.
    """
    tmp=DMGtable.apply(np.floor).astype("Int64")
    # sort by damage
    classes=tmp.index.get_level_values(0).unique() # we want to keep weapon class order most likely
    orderDesc=tmp.loc[pd.IndexSlice[:,:,"No Prc"],:].max(axis=1).sort_values(ascending=False).index.get_level_values(1)
    tmp=tmp.sort_index(level=1,key=lambda x:x.map({ii:i for i,ii in enumerate(orderDesc)}))
    if comparison!="all":
        tmp=tmp.sort_index(level=0,sort_remaining=False,key=lambda x:x.map({ii:i for i,ii in enumerate(classes)})) # restore class order
    # percentages
    if comparison=="row":
        DMGratio=tmp.apply(lambda x:x/x.max()*100-100,axis=1).astype(float)
    if comparison=="class":
        DMGratio=tmp.apply(lambda x:x/tmp.loc[pd.IndexSlice[x.name[0],:,x.name[2]],:].max().max()*100-100,axis=1).astype(float)
    elif comparison=="all":
        DMGratio=tmp.apply(lambda x:x/tmp.max().max()*100-100,axis=1).astype(float)
    res=tmp.copy()
    for c in tmp.columns:
        if displayPercentage:
            res[c]=res[c].map(lambda x:str(x).replace("<NA>","-"))+" ("+DMGratio[c].round(1).map(lambda x:("👑" if x==0 else (("+" if x>=0 else "-")+str(abs(x)).replace("nan",""))+"%"))+")"
        else:
            res[c]=res[c].map(lambda x:str(x).replace("<NA>","-"))
    # display max of each row in bold
    res=res.style.format(precision=1).apply(lambda x:tmp.apply(lambda x:x.apply(lambda xx:'font-weight: bold' if not pd.isna(xx) and xx==x.max() else ''),axis=1),axis=None) # miracle
    # background color
    for i in tmp.index:
        vmin=-20
        if not multicolor:
            res.background_gradient(cmap="Greens",axis=None,gmap=DMGratio.fillna(vmin),vmin=vmin,vmax=0)
        else:
            cmaps=[["white","red"],["white","gold"],["white","blue"],["white","orange"],["white","violet"]]
            for j,jj in enumerate(tmp.columns.get_level_values(0).unique()):
                res.background_gradient(cmap=LinearSegmentedColormap.from_list("",cmaps[j%5]),axis=None,gmap=DMGratio.fillna(vmin),subset=(i,tmp[[jj]].columns),vmin=vmin,vmax=2)
    # weapon class display and hide pierce bonus if useless
    hide=[]
    if not showWeaponClass:
        hide.append(0)
    if tmp.index.get_level_values(2).drop_duplicates().size==1:
        hide.append(2)
    res=res.hide(level=hide)
    # borders
    for i in [j for i,j in zip(tmp.columns[:-1],tmp.columns[1:]) if i[0]!=j[0]]:
        res.set_table_styles({i: [{'selector': '', 'props': 'border-left: 1px solid grey;'}]}, overwrite=False)
    if res.index.nlevels>1:
        for i in [j for i,j in zip(tmp.index[:-1],tmp.index[1:]) if i[0]!=j[0]]:
            res.set_table_styles({i: [{'selector': '', 'props': 'border-top: 1px solid grey;'}]}, overwrite=False, axis=1)
    # stats
    if not showStats:
        res.format_index(lambda x:x.split("•")[0].rstrip(),axis=1)
    return(res)

# Defaults

def setDefaultBuilds():
    st.session_state.nBuilds=3
    st.session_state["name0"]="FS abuser"
    st.session_state["str0"]=66
    st.session_state["dex0"]=16
    st.session_state["int0"]=9
    st.session_state["fth0"]=9
    st.session_state["arc0"]=7
    st.session_state["infusions0"]=["Heavy","Fire"]
    st.session_state["name1"]="Phalanx abuser"
    st.session_state["str1"]=21
    st.session_state["dex1"]=20
    st.session_state["int1"]=50
    st.session_state["fth1"]=9
    st.session_state["arc1"]=7
    st.session_state["infusions1"]=["Magic","Cold"]
    st.session_state["name2"]="SB abuser"
    st.session_state["str2"]=21
    st.session_state["dex2"]=20
    st.session_state["int2"]=9
    st.session_state["fth2"]=50
    st.session_state["arc2"]=7
    st.session_state["infusions2"]=["Sacred"]

def setDefaultWeapons():
    st.session_state.weapons=["Dismounter","Banished Knight's Halberd","2H Cleanrot Knight's Sword","Cleanrot Knight's Sword","Wakizashi","Lance","Longsword","Partisan","Spiked Spear","2H Shamshir","2H Godskin Stitcher","Star Fist"]

def setDefaultDefStats():
    st.session_state.defstandard=140
    st.session_state.defstrike=140
    st.session_state.defslash=140
    st.session_state.defpierce=140
    st.session_state.defmagic=155
    st.session_state.deffire=187
    st.session_state.deflightning=127
    st.session_state.defholy=155
    st.session_state.negstandard=33.0
    st.session_state.negstrike=30.7
    st.session_state.negslash=35.1
    st.session_state.negpierce=35.3
    st.session_state.negmagic=26.1
    st.session_state.negfire=28.4
    st.session_state.neglightning=25.5
    st.session_state.negholy=26.6
