import streamlit as st

from utils.utils import weaponsOfClass
from utils.defaults import setDefaultBuilds,setDefaultWeapons,setDefaultDefStats
from utils.constants import baseInfusions,weaponClasses

for k in st.session_state:
    st.session_state[k]=st.session_state[k]

st.set_page_config(layout='wide',page_title="Parameters",page_icon="🛠️")

if "defstandard" not in st.session_state:
    setDefaultDefStats()

if "reinforcementLvl" not in st.session_state:
    st.session_state.reinforcementLvl=25
    
if "nBuilds" not in st.session_state:
    setDefaultBuilds()

if "weapons" not in st.session_state:
    setDefaultWeapons()

st.markdown("""
    <style>
        /* "Center" 2H */
        label[data-baseweb="checkbox"] {
            display: flex;
            justify-content: flex-end;
        }
        /* "Center" +Build */
        div[data-testid="column"]:nth-of-type(1) div[data-testid="stButton"] {
            display: flex;
            justify-content: flex-end;
        }
        /* Removes useless space on top */
        .appview-container .main .block-container {
            padding-top: 3rem;
        }
    </style>
""",unsafe_allow_html=True)

st.sidebar.info("Default enemy defenses are the average of classic STR, DEX, INT, FTH and ARC builds.")
st.sidebar.info("Default enemy negations are Imp/Beast Champion (Altered)/Beast Champion/Beast Champion.")

def addWeapons(selected):
    for w in selected:
        w=f"{'2H ' if twoH else ''}{w}"
        if w not in st.session_state.weapons:
            st.session_state.weapons.append(w)
        else:
            st.toast(f"{w} already selected",icon="⚠️")

def showBuild(i):
    cols=st.columns([4,3,3,3,3,3,7])
    with cols[0]: st.text_input("Build name",key=f"name{i}",label_visibility="collapsed")
    with cols[1]: st.number_input("STR",1,99,key=f"str{i}",label_visibility="collapsed")
    with cols[2]: st.number_input("DEX",1,99,key=f"dex{i}",label_visibility="collapsed")
    with cols[3]: st.number_input("INT",1,99,key=f"int{i}",label_visibility="collapsed")
    with cols[4]: st.number_input("FTH",1,99,key=f"fth{i}",label_visibility="collapsed")
    with cols[5]: st.number_input("ARC",1,99,key=f"arc{i}",label_visibility="collapsed")
    with cols[6]: st.multiselect("Infusions",baseInfusions,key=f"infusions{i}",label_visibility="collapsed")

def addBuild():
    i=st.session_state.nBuilds
    st.session_state[f"name{i}"]=f"Build {i}"
    st.session_state[f"str{i}"]=14
    st.session_state[f"dex{i}"]=13
    st.session_state[f"int{i}"]=9
    st.session_state[f"fth{i}"]=9
    st.session_state[f"arc{i}"]=7
    st.session_state[f"infusions{i}"]=[]
    st.session_state.nBuilds+=1

def removeBuild():
    i=st.session_state.nBuilds-1
    del st.session_state[f"name{i}"]
    del st.session_state[f"str{i}"]
    del st.session_state[f"dex{i}"]
    del st.session_state[f"int{i}"]
    del st.session_state[f"fth{i}"]
    del st.session_state[f"arc{i}"]
    del st.session_state[f"infusions{i}"]
    st.session_state.nBuilds-=1


st.header("⚔️ Weapons")

cols=st.columns([2,6,1])
with cols[0]: wClass=st.selectbox("Weapon class",weaponClasses)
with cols[1]: selected=st.multiselect("Weapons",weaponsOfClass(wClass))
with cols[2]: st.number_input("Weapon Level",0,25,key="reinforcementLvl",
                              help="NORMAL weapon level from 0 to 25. Somber level is automatically calculated from this. Applies to all weapons.")
cols=st.columns(2)
with cols[0]: twoH=st.toggle("2H")
with cols[1]: st.button("Add to selected weapons",on_click=addWeapons,args=(selected,),type="primary")

st.multiselect("Selected weapons",st.session_state.weapons,key="weapons")

st.divider()

st.header("📊 Builds")

# Header
cols=st.columns([4,3,3,3,3,3,7])
with cols[0]: st.subheader("Build name")
with cols[1]: st.subheader("STR")
with cols[2]: st.subheader("DEX")
with cols[3]: st.subheader("INT")
with cols[4]: st.subheader("FTH")
with cols[5]: st.subheader("ARC")
with cols[6]: st.subheader("Infusions")
# Build input
for i in range(st.session_state.nBuilds):
    showBuild(i)
cols=st.columns(2)
with cols[0]: st.button("\+ Build",on_click=addBuild,type="primary")
with cols[1]: st.button("\- Build",on_click=removeBuild,disabled=st.session_state.nBuilds==0)

st.divider()

st.header("🛡️ Enemy stats")

cols=st.columns(8)
with cols[0]: st.number_input("Standard defense",0,400,key="defstandard")
with cols[1]: st.number_input("Strike defense",0,400,key="defstrike")
with cols[2]: st.number_input("Slash defense",0,400,key="defslash")
with cols[3]: st.number_input("Pierce defense",0,400,key="defpierce")
with cols[4]: st.number_input("Magic defense",0,400,key="defmagic")
with cols[5]: st.number_input("Fire defense",0,400,key="deffire")
with cols[6]: st.number_input("Lightning defense",0,400,key="deflightning")
with cols[7]: st.number_input("Holy defense",0,400,key="defholy")
cols=st.columns(8)
with cols[0]: st.number_input("Standard negation",0.,100.,key="negstandard",format="%.1f",step=0.1)
with cols[1]: st.number_input("Strike negation",0.,100.,key="negstrike",format="%.1f",step=0.1)
with cols[2]: st.number_input("Slash negation",0.,100.,key="negslash",format="%.1f",step=0.1)
with cols[3]: st.number_input("Pierce negation",0.,100.,key="negpierce",format="%.1f",step=0.1)
with cols[4]: st.number_input("Magic negation",0.,100.,key="negmagic",format="%.1f",step=0.1)
with cols[5]: st.number_input("Fire negation",0.,100.,key="negfire",format="%.1f",step=0.1)
with cols[6]: st.number_input("Lightning negation",0.,100.,key="neglightning",format="%.1f",step=0.1)
with cols[7]: st.number_input("Holy negation",0.,100.,key="negholy",format="%.1f",step=0.1)
