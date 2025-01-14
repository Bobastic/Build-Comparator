import streamlit as 

from utils.utils import fancyTable, DMGtable, weaponsOfClass
from utils.defaults import setDefaultBuilds, setDefaultWeapons, setDefaultDefStats, setDefaultTableOptions, setNegations
from utils.constants import baseInfusions, weaponClasses

for k in st.session_state:
    st.session_state[k] = st.session_state[k]

st.set_page_config(layout='wide', page_title="Build Comparator", page_icon="🔬")

st.html("""
<style>
    p {
        text-align: justify;
    }
    /* Removes useless space on top */
    .appview-container .main .block-container {
        padding-top: 4rem;
    }
    div[data-testid="column"]:nth-of-type(1) div[data-testid="stButton"] {
        display: flex;
        justify-content: flex-end;
    }
</style>
""")

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

st.sidebar.info("The damage you see is post enemy defenses and negations.")
st.sidebar.info("Attacks have a motion value of 100 (usually R1).")
st.sidebar.info("The physical damage type is the most common one for the weapon (Standard for Longsword, Slash for Wakizashi etc...)")
st.sidebar.info("If you have lots of columns and the table starts to get compressed you can fold this sidebar.")

# Weapons

def addWeapons(selected, twoH):
    for w in selected:
        w = f"{'2H ' if twoH else ''}{w}"
        if w not in st.session_state.weapons:
            st.session_state.weapons.append(w)
        else:
            st.toast(f"{w} already selected", icon="⚠️")

@st.experimental_fragment
def weaponsParam():
    cols = st.columns([3,7])
    with cols[0]: wClass = st.selectbox("Weapon class", weaponClasses, placeholder="Chose a class")
    with cols[1]: selected = st.multiselect("Weapons", weaponsOfClass(wClass), placeholder="Chose your weapons")
    cols = st.columns([5,2,7,1])
    with cols[1]: twoH = st.toggle("2H")
    with cols[2]: st.button("Add to selected weapons", on_click=addWeapons, args=(selected, twoH), type="primary")
    st.multiselect("Selected weapons", st.session_state.weapons, st.session_state.weapons, key="weapons")
    st.number_input("Global weapon level",0,25,key="reinforcementLvl",help="NORMAL weapon level from 0 to 25. Somber level is automatically calculated from this. Applies to all weapons.")    

# Builds

def addBuild():
    i = st.session_state.nBuilds
    st.session_state[f"name{i}"] = f"Build {i}"
    st.session_state[f"str{i}"] = 14
    st.session_state[f"dex{i}"] = 13
    st.session_state[f"int{i}"] = 9
    st.session_state[f"fth{i}"] = 9
    st.session_state[f"arc{i}"] = 7
    st.session_state[f"infusions{i}"] = []
    st.session_state.nBuilds += 1

def removeBuild():
    i = st.session_state.nBuilds-1
    del st.session_state[f"name{i}"]
    del st.session_state[f"str{i}"]
    del st.session_state[f"dex{i}"]
    del st.session_state[f"int{i}"]
    del st.session_state[f"fth{i}"]
    del st.session_state[f"arc{i}"]
    del st.session_state[f"infusions{i}"]
    st.session_state.nBuilds -= 1

@st.experimental_fragment
def buildsParam():
    for i in range(st.session_state.nBuilds):
        with st.container(border=True):
            cols = st.columns([8,3,3,3,3,3])
            with cols[0]: st.text_input("Build name", key=f"name{i}")
            with cols[1]: st.number_input("STR", 1, 99, key=f"str{i}")
            with cols[2]: st.number_input("DEX", 1, 99, key=f"dex{i}")
            with cols[3]: st.number_input("INT", 1, 99, key=f"int{i}")
            with cols[4]: st.number_input("FTH", 1, 99, key=f"fth{i}")
            with cols[5]: st.number_input("ARC", 1, 99, key=f"arc{i}")
            st.multiselect("Infusions", baseInfusions, key=f"infusions{i}", placeholder="Chose your infusions", label_visibility="collapsed")
    cols = st.columns(2)
    with cols[0]: st.button("\+ Build", on_click=addBuild, type="primary")
    with cols[1]: st.button("\- Build", on_click=removeBuild, disabled=st.session_state.nBuilds==0)

# Enemy stats

@st.experimental_fragment
def enemyStatsParam():
    with st.container(border=True):
        st.subheader("Defenses", anchor=False, help="Default enemy defenses are the average of classic STR, DEX, INT, FTH and ARC builds.")
        cols = st.columns(4)
        with cols[0]: st.number_input("Standard", 0, 400, key="defstandard")
        with cols[1]: st.number_input("Strike", 0, 400, key="defstrike")
        with cols[2]: st.number_input("Slash", 0, 400, key="defslash")
        with cols[3]: st.number_input("Pierce", 0, 400, key="defpierce")
        with cols[0]: st.number_input("Magic", 0, 400, key="defmagic")
        with cols[1]: st.number_input("Fire", 0, 400, key="deffire")
        with cols[2]: st.number_input("Lightning", 0, 400, key="deflightning")
        with cols[3]: st.number_input("Holy", 0, 400, key="defholy")
    with st.container(border=True):
        st.subheader("Negations", anchor=False, help="Default enemy negations are Imp - Beast Champion (Altered) - Beast Champion - Beast Champion.")
        cols = st.columns(4)
        with cols[0]: st.number_input("Standard", 0., 100., key="negstandard", format="%.1f", step=0.1)
        with cols[1]: st.number_input("Strike", 0., 100., key="negstrike", format="%.1f", step=0.1)
        with cols[2]: st.number_input("Slash", 0., 100., key="negslash", format="%.1f", step=0.1)
        with cols[3]: st.number_input("Pierce", 0., 100., key="negpierce", format="%.1f", step=0.1)
        with cols[0]: st.number_input("Magic", 0., 100., key="negmagic", format="%.1f", step=0.1)
        with cols[1]: st.number_input("Fire", 0., 100., key="negfire", format="%.1f", step=0.1)
        with cols[2]: st.number_input("Lightning", 0., 100., key="neglightning", format="%.1f", step=0.1)
        with cols[3]: st.number_input("Holy", 0., 100., key="negholy", format="%.1f", step=0.1)
        cols = st.columns(3)
        with cols[0]: st.button("Beastmaster", on_click=setNegations, args=("beastmaster",), use_container_width=True)
        with cols[1]: st.button("Fullgoat", on_click=setNegations, args=("fullgoat",), use_container_width=True)
        with cols[2]: st.button("Lionel", on_click=setNegations, args=("lionel",), use_container_width=True)

# Table settings

@st.experimental_fragment
def tableSettingsParam():
    cols = st.columns([8,7])
    with cols[0]:
        st.toggle("Compare Builds",key="compareBuilds",help="Compute the damage difference between all builds (one crown per line).")
        st.toggle("Counter Hits",key="counterHits",help="+15%: normal counter hit. +32%: counter hit with Spear Talisman equipped.")
        st.toggle("Opaline Hardtear",key="hardtear",help="Opponent has +10% negations.")
        st.toggle("Elemental Tear",key="eleTear",help="Use the best elemental damage Physik Tear (+12.5% dmg).")
        st.toggle("Grease Buffs",key="greaseBuffs",help="Lightning except for Clayman's, Treespear, Great Club and Troll's Hammer.")
        st.toggle("AoW Buffs",key="aowBuffs",help="Flaming Strike, Lightning Slash and Sacred Blade.")
    with cols[1]:
        st.toggle("Compare Class",key="compareClass",help="Compare the weapon with the best of its class (one crown per class).")
        st.toggle("Multicolor",key="multicolor",help="One color per build or single color gradient.")
        st.toggle("Display Dmg",key="displayDmg",help="Display estimated damage.")
        st.toggle("Display %",key="displayPct", help="How much worse the weapon is compared to the best. Ex: -20% means the weapon deals 20% less damage than the best.")
        st.toggle("Weapon Class",key="showWeaponClass",help="Display weapon class on the left of the table.")
        st.toggle("Build Stats",key="showStats",help="Show stats in column header.")



cols = st.columns(5)
with cols[0]:
    with st.popover("⚔️ Weapons", use_container_width=True): weaponsParam()
with cols[1]:
    with st.popover("📊 Builds", use_container_width=True): buildsParam()
with cols[2]:
    with st.popover("🛡️ Enemy stats", use_container_width=True): enemyStatsParam()
with cols[3]:
    with st.popover("⚙️ Table settings", use_container_width=True): tableSettingsParam()
with cols[4]:
    st.button("Update table", type="primary", use_container_width=True)

# Table

if st.session_state.nBuilds != 0 and len(st.session_state.weapons) != 0 and [inf for i in range(st.session_state.nBuilds) for inf in st.session_state[f"infusions{i}"]]:
    with st.spinner("Computing table..."):
        weapons = st.session_state.weapons
        builds = {st.session_state[f"name{i}"]: [st.session_state[f"{stat}{i}"] for stat in ["str", "dex", "int", "fth", "arc"]] for i in range(st.session_state.nBuilds)}
        infusions = {st.session_state[f"name{i}"]: st.session_state[f"infusions{i}"] for i in range(st.session_state.nBuilds)}
        defenses = [st.session_state.defstandard, st.session_state.defstrike, st.session_state.defslash, st.session_state.defpierce,
                    st.session_state.defmagic, st.session_state.deffire, st.session_state.deflightning, st.session_state.defholy]
        negations = [st.session_state.negstandard, st.session_state.negstrike, st.session_state.negslash, st.session_state.negpierce,
                     st.session_state.negmagic, st.session_state.negfire, st.session_state.neglightning, st.session_state.negholy]
        table = DMGtable(weapons, builds, infusions, defenses, negations, st.session_state.reinforcementLvl, st.session_state.greaseBuffs,
                         st.session_state.aowBuffs, st.session_state.counterHits, st.session_state.hardtear, st.session_state.eleTear)
        fancy = fancyTable(table, st.session_state.compareBuilds, st.session_state.compareClass, st.session_state.displayDmg, st.session_state.displayPct,
                           st.session_state.showStats, st.session_state.multicolor, st.session_state.showWeaponClass)
        st.write(fancy.to_html(), unsafe_allow_html=True)
else:
    st.error('Input at least one build, one infusion and one weapon in the "🛠️ Parameters" tab.', icon="🚨")
