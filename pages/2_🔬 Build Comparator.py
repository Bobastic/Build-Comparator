import dataframe_image as dfi
import streamlit as st
from io import BytesIO

from utils.utils import fancyTable,DMGtable
from utils.defaults import setDefaultBuilds,setDefaultWeapons,setDefaultDefStats

st.set_page_config(layout='wide',page_title="Build Comparator",page_icon="🔬")

st.sidebar.info("The damage you see is post enemy defenses and negations.")
st.sidebar.info("Attacks have a motion value of 100 (usually R1).")
st.sidebar.info("The physical damage type is the most common one for the weapon (Standard for Longsword, Slash for Wakizashi etc...)")
st.sidebar.info("If you have lots of columns and the table starts to get compressed you can fold this sidebar.")

if "download" not in st.session_state:
    st.session_state.download=False

if "nBuilds" not in st.session_state:
    st.session_state.nBuilds=0
    setDefaultBuilds()
    setDefaultWeapons()
    setDefaultDefStats()

st.markdown("""
    <style>
        div[data-testid="column"]:nth-of-type(7)
        {
            text-align: end;
        } 
    </style>
    """,unsafe_allow_html=True)

cols=st.columns(7)
with cols[0]:
    weaponLvl=st.number_input("Weapon Level",0,25,25)
with cols[1]:
    opaline=st.toggle("Opaline Hardtear",value=True,help="Opponent has +15% negations.")
    aaa=st.toggle("a a",value=True,help="Opponent has +15% negations.")
with cols[2]:
    weaponBuffs=st.toggle("Weapon buffs",value=True,help="Grease (Lightning except for split damage weapons like Treespear), Flaming Strike, Lightning Slash, Sacred Blade.")
    counterHits=st.toggle("Counter Hits",value=True,help="+15%: normal counter hit. +32%: counter hit with Spear Talisman equipped.")
with cols[3]:
    multicolor=st.toggle("Multicolor",value=True,help="One color per build or simple gradient.")
    showWeaponClass=st.toggle("Weapon Class",value=False,help="Display weapon class on the left of the table.")
with cols[4]:
    displayPercentage=st.toggle("Ratio with best",value=True,help="How much worse the weapon is compared to the best. For example -20% means the weapon deals 20% less damage than the best.")
    showStats=st.toggle("Build Stats",value=True,help="Show stats in column header.")
with cols[5]:
    comparison=st.selectbox("Comparison with best of...",("row","class","all"),index=1,
                            help="Row: tells you what is the best infusion and build for the weapon. Class: tells you what is the best weapon of the class. All: tells you whats is the best weapon of the table")

def convertPNG():
    if not st.session_state.download:
        st.session_state.download=True
        st.warning('Now click on "Download PNG" to actually start the download.')
        import os
        st.write([f for f in os.walk("/mount/")])
    else:
        st.session_state.download=False
        buff=BytesIO()
        dfi.export(fancy,buff)
        try:
            pass
        except:
            st.toast("You have to use chrome to get a decent table sadly. Trying to solve this issue.")
            dfi.export(fancy,buff,table_conversion="matplotlib")
        return buff.getvalue()

if st.session_state.nBuilds!=0 and len(st.session_state.weapons)!=0:
    with st.spinner("Computing table..."):
        weapons=st.session_state.weapons
        builds={st.session_state[f"name{i}"]:[st.session_state[f"str{i}"],st.session_state[f"dex{i}"],st.session_state[f"int{i}"],st.session_state[f"fth{i}"],st.session_state[f"arc{i}"]]
                for i in range(st.session_state.nBuilds)}
        infusions={st.session_state[f"name{i}"]:st.session_state[f"infusions{i}"] for i in range(st.session_state.nBuilds)}
        defenses=[st.session_state.defstandard,st.session_state.defstrike,st.session_state.defslash,st.session_state.defpierce,
                  st.session_state.defmagic,st.session_state.deffire,st.session_state.deflightning,st.session_state.defholy]
        negations=[st.session_state.negstandard,st.session_state.negstrike,st.session_state.negslash,st.session_state.negpierce,
                   st.session_state.negmagic,st.session_state.negfire,st.session_state.neglightning,st.session_state.negholy]
        table=DMGtable(weapons,builds,infusions,defenses,negations,weaponBuffs=weaponBuffs,counterHits=counterHits)
        fancy=fancyTable(table,comparison=comparison,displayPercentage=displayPercentage,showStats=showStats,multicolor=multicolor,showWeaponClass=showWeaponClass)
        st.write(fancy.to_html(),unsafe_allow_html=True)
    with cols[6]:
        st.download_button("Download CSV",table.to_csv(),file_name="buildComparatorData.csv")
        if not st.session_state.download:
            st.button("Convert to PNG",disabled=True,on_click=convertPNG)
        else:
            with st.spinner("Converting..."): st.download_button("Download PNG",convertPNG(),file_name="buildComparator.png",mime="image/png")
else:
    st.error('Input at least one build, one weapon and fill enemy stats in the "🛠️ Parameters" tab.',icon="🚨")
