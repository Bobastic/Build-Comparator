import streamlit as st

from utils.utils import fancyTable,DMGtable
from utils.defaults import setDefaultBuilds,setDefaultWeapons,setDefaultDefStats,setDefaultTableOptions

for k in st.session_state:
    st.session_state[k]=st.session_state[k]

st.set_page_config(layout='wide',page_title="Build Comparator",page_icon="🔬")

if "defstandard" not in st.session_state:
    setDefaultDefStats()

if "reinforcementLvl" not in st.session_state:
    st.session_state.reinforcementLvl=25
    
if "nBuilds" not in st.session_state:
    setDefaultBuilds()

if "weapons" not in st.session_state:
    setDefaultWeapons()

if "compareBuilds" not in st.session_state:
    setDefaultTableOptions()

st.markdown("""
    <style>
        /* Removes useless space on top */
        .appview-container .main .block-container {
            padding-top: 3rem;
        }
    </style>
""",unsafe_allow_html=True)

st.sidebar.info("Default enemy defenses are the average of classic STR, DEX, INT, FTH and ARC builds.")
st.sidebar.info("Default enemy negations are Imp/Beast Champion (Altered)/Beast Champion/Beast Champion.")
st.sidebar.info("The damage you see is post enemy defenses and negations.")
st.sidebar.info("Attacks have a motion value of 100 (usually R1).")
st.sidebar.info("The physical damage type is the most common one for the weapon (Standard for Longsword, Slash for Wakizashi etc...)")
st.sidebar.info("If you have lots of columns and the table starts to get compressed you can fold this sidebar.")

cols=st.columns(6)
with cols[0]:
    st.toggle("Compare Builds",key="compareBuilds",help="Compute the damage difference between all builds (one crown per line).")
    st.toggle("Compare w/ Class",key="compareClass",help="Compare the weapon with the best of its class (one crown per class).")
with cols[1]:
    st.toggle("Opaline Hardtear",key="hardtear",help="Opponent has +10% negations.")
    st.toggle("Elemental Tear",key="eleTear",help="Use the best elemental damage Physik Tear (+12.5% dmg).")
with cols[2]:
    st.toggle("Grease Buffs",key="greaseBuffs",help="Lightning except for Clayman's, Treespear, Great Club and Troll's Hammer.")
    st.toggle("AoW Buffs",key="aowBuffs",help="Flaming Strike, Lightning Slash and Sacred Blade.")
with cols[3]:
    st.toggle("Counter Hits",key="counterHits",help="+15%: normal counter hit. +32%: counter hit with Spear Talisman equipped.")
    st.toggle("Multicolor",key="multicolor",help="One color per build or single color gradient.")
with cols[4]:
    st.toggle("Display Dmg",key="displayDmg",help="Display estimated damage.")
    st.toggle("Display %",key="displayPct", help="How much worse the weapon is compared to the best. Ex: -20% means the weapon deals 20% less damage than the best.")
with cols[5]:
    st.toggle("Weapon Class",key="showWeaponClass",help="Display weapon class on the left of the table.")
    st.toggle("Build Stats",key="showStats",help="Show stats in column header.")

if st.session_state.nBuilds!=0 and len(st.session_state.weapons)!=0 and [inf for i in range(st.session_state.nBuilds) for inf in st.session_state[f"infusions{i}"]]:
    with st.spinner("Computing table..."):
        weapons=st.session_state.weapons
        builds={st.session_state[f"name{i}"]:[st.session_state[f"{stat}{i}"] for stat in ["str","dex","int","fth","arc"]] for i in range(st.session_state.nBuilds)}
        infusions={st.session_state[f"name{i}"]:st.session_state[f"infusions{i}"] for i in range(st.session_state.nBuilds)}
        defenses=[st.session_state.defstandard,st.session_state.defstrike,st.session_state.defslash,st.session_state.defpierce,
                  st.session_state.defmagic,st.session_state.deffire,st.session_state.deflightning,st.session_state.defholy]
        negations=[st.session_state.negstandard,st.session_state.negstrike,st.session_state.negslash,st.session_state.negpierce,
                   st.session_state.negmagic,st.session_state.negfire,st.session_state.neglightning,st.session_state.negholy]
        table=DMGtable(weapons,builds,infusions,defenses,negations,st.session_state.reinforcementLvl,st.session_state.greaseBuffs,
                       st.session_state.aowBuffs,st.session_state.counterHits,st.session_state.hardtear,st.session_state.eleTear)
        fancy=fancyTable(table,st.session_state.compareBuilds,st.session_state.compareClass,st.session_state.displayDmg,st.session_state.displayPct,
                         st.session_state.showStats,st.session_state.multicolor,st.session_state.showWeaponClass)
        st.write(fancy.to_html(),unsafe_allow_html=True)
else:
    st.error('Input at least one build, one infusion and one weapon in the "🛠️ Parameters" tab.',icon="🚨")

#st.download_button("Download CSV",table.to_csv(),file_name="buildComparatorData.csv")