import dataframe_image as dfi
import streamlit as st

from utils.utils import fancyTable,DMGtable,setDefaultBuilds,setDefaultWeapons,setDefaultDefStats

st.set_page_config(layout='wide',page_title="Build Comparator",page_icon="🔬")

if "download" not in st.session_state:
    st.session_state.download=False

if "nBuilds" not in st.session_state:
    st.session_state.nBuilds=0
    setDefaultBuilds()
    setDefaultWeapons()
    setDefaultDefStats()

st.markdown("""
    <style>
        div[data-testid="column"]:nth-of-type(5)
        {
            text-align: end;
        } 
    </style>
    """,unsafe_allow_html=True)

cols=st.columns(5)
with cols[0]:
    weaponBuffs=st.checkbox("Weapon buffs",value=True,help="Grease (Lightning except for split damage weapons like Treespear), Flaming Strike, Sacred Blade.")
    counterHits=st.checkbox("Counter Hits",value=True,help="+15%: normal counter hit. +32%: counter hit with Spear Talisman equipped.")
with cols[1]:
    multicolor=st.checkbox("Multicolor",value=True,help="One color per build or simple gradient.")
    showWeaponClass=st.checkbox("Weapon Class",value=False,help="Display weapon class on the left of the table.")
with cols[2]:
    displayPercentage=st.checkbox("Ratio with best",value=True,help="How much worse the weapon is compared to the best. For example -20% means the weapon deals 20% less damage than the best.")
    showStats=st.checkbox("Build Stats",value=True,help="Show stats in column header.")
with cols[3]:
    comparison=st.selectbox("Comparison with best of...",("row","class","all"),index=1,
                            help="Row: tells you what is the best infusion and build for the weapon. Class: tells you what is the best weapon of the class. All: Tells you whats is the best weapon of the table")

def convertPNG():
    st.session_state.download=True
    dfi.export(fancy,"tmp.png")
    st.warning('Now click on "Download PNG" to actually start the download (that\'s janky I know)')

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
    with cols[4]:
        st.download_button("Download CSV",table.to_csv(),file_name="buildComparatorData.csv")
        if st.session_state.download:
            with open("tmp.png","rb") as img:
                data=img.read()
            st.download_button("Download PNG",data,file_name="buildComparator.png",mime="image/png")
            st.session_state.download=False
        else:
            st.button("Convert to PNG",on_click=convertPNG)
else:
    st.error('Input at least one build, one weapon and fill ennemy stats in the "🛠️ Parameters" tab.',icon="🚨")
