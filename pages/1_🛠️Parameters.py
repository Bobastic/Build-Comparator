import streamlit as st

from utils.utils import baseInfusions,weaponClasses,weaponsOfClass
from utils.defaults import setDefaultBuilds,setDefaultWeapons,setDefaultDefStats

st.set_page_config(layout='wide',page_title="Parameters",page_icon="🛠️")

st.sidebar.info("Default enemy defenses are the average of classic STR, DEX, INT, FTH and ARC builds. Default negations are Imp Head/Beast Champion Armor (Altered)/Fire Prelate Gauntlets/Lionel's Greaves.")

st.header("⚔️ Weapons")

if "nBuilds" not in st.session_state:
    st.session_state.nBuilds=0
    setDefaultBuilds()
    setDefaultWeapons()
    setDefaultDefStats()

def updateState(key):
    st.session_state[key.lower()]=st.session_state[key]

st.markdown("""
<style>
    div[data-testid="column"]
    {
        display: flex;
        align-items: center;
    }
    label[data-baseweb="checkbox"]
    {
        justify-content: flex-end;
    }
    div[data-testid="column"]:nth-of-type(1) div[class="row-widget stButton"]
    {
        display: flex;
        justify-content: flex-end;
    }
</style>
""",unsafe_allow_html=True)

def addWeapons():
    for w in st.session_state.selected:
        w=f"{'2H ' if st.session_state.twoH else ''}{w}"
        if w not in st.session_state.weapons:
            st.session_state.weapons.append(w)
        else:
            st.toast("Weapon already selected")

cols=st.columns([2,7])
with cols[0]: st.selectbox("Weapon class",weaponClasses,key="class")
with cols[1]: st.multiselect("Weapons",weaponsOfClass(st.session_state["class"]),key="selected")
cols=st.columns(2)
with cols[0]: st.checkbox("2H",key="twoH")
with cols[1]: st.button("Add to selected weapons",on_click=addWeapons,type="primary")

st.multiselect("Selected weapons",st.session_state.weapons,st.session_state.weapons,key="WEAPONS",on_change=updateState,args=("WEAPONS",))

st.divider()

st.header("📊 Builds")


def showBuild(i):
    cols=st.columns([4,3,3,3,3,3,7])
    with cols[0]: st.text_input("Build name",st.session_state[f"name{i}"],key=f"NAME{i}",label_visibility="collapsed",on_change=updateState,args=(f"NAME{i}",))
    with cols[1]: st.number_input("STR",1,99,st.session_state[f"str{i}"],key=f"STR{i}",label_visibility="collapsed",on_change=updateState,args=(f"STR{i}",))
    with cols[2]: st.number_input("DEX",1,99,st.session_state[f"dex{i}"],key=f"DEX{i}",label_visibility="collapsed",on_change=updateState,args=(f"DEX{i}",))
    with cols[3]: st.number_input("INT",1,99,st.session_state[f"int{i}"],key=f"INT{i}",label_visibility="collapsed",on_change=updateState,args=(f"INT{i}",))
    with cols[4]: st.number_input("FTH",1,99,st.session_state[f"fth{i}"],key=f"FTH{i}",label_visibility="collapsed",on_change=updateState,args=(f"FTH{i}",))
    with cols[5]: st.number_input("ARC",1,99,st.session_state[f"arc{i}"],key=f"ARC{i}",label_visibility="collapsed",on_change=updateState,args=(f"ARC{i}",))
    with cols[6]: st.multiselect("Infusions",baseInfusions,st.session_state[f"infusions{i}"],key=f"INFUSIONS{i}",label_visibility="collapsed",on_change=updateState,args=(f"INFUSIONS{i}",))

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
with cols[0]: add=st.button("Add Build",on_click=addBuild,type="primary")
with cols[1]: rem=st.button("Rem. Build",on_click=removeBuild,disabled=st.session_state.nBuilds==0)

st.divider()

st.header("🛡️ Enemy stats")

cols=st.columns(8)
with cols[0]: st.number_input("Standard defense",0,400,st.session_state.defstandard,key="DEFSTANDARD",on_change=updateState,args=("DEFSTANDARD",))
with cols[1]: st.number_input("Strike defense",0,400,st.session_state.defstrike,key="DEFSTRIKE",on_change=updateState,args=("DEFSTRIKE",))
with cols[2]: st.number_input("Slash defense",0,400,st.session_state.defslash,key="DEFSLASH",on_change=updateState,args=("DEFSLASH",))
with cols[3]: st.number_input("Pierce defense",0,400,st.session_state.defpierce,key="DEFPIERCE",on_change=updateState,args=("DEFPIERCE",))
with cols[4]: st.number_input("Magic defense",0,400,st.session_state.defmagic,key="DEFMAGIC",on_change=updateState,args=("DEFMAGIC",))
with cols[5]: st.number_input("Fire defense",0,400,st.session_state.deffire,key="DEFFIRE",on_change=updateState,args=("DEFFIRE",))
with cols[6]: st.number_input("Lightning defense",0,400,st.session_state.deflightning,key="DEFLIGHTNING",on_change=updateState,args=("DEFLIGHTNING",))
with cols[7]: st.number_input("Holy defense",0,400,st.session_state.defholy,key="DEFHOLY",on_change=updateState,args=("DEFHOLY",))
cols=st.columns(8)
with cols[0]: st.number_input("Standard negation",0.,100.,st.session_state.negstandard,key="NEGSTANDARD",on_change=updateState,args=("NEGSTANDARD",),format="%.1f")
with cols[1]: st.number_input("Strike negation",0.,100.,st.session_state.negstrike,key="NEGSTRIKE",on_change=updateState,args=("NEGSTRIKE",),format="%.1f")
with cols[2]: st.number_input("Slash negation",0.,100.,st.session_state.negslash,key="NEGSLASH",on_change=updateState,args=("NEGSLASH",),format="%.1f")
with cols[3]: st.number_input("Pierce negation",0.,100.,st.session_state.negpierce,key="NEGPIERCE",on_change=updateState,args=("NEGPIERCE",),format="%.1f")
with cols[4]: st.number_input("Magic negation",0.,100.,st.session_state.negmagic,key="NEGMAGIC",on_change=updateState,args=("NEGMAGIC",),format="%.1f")
with cols[5]: st.number_input("Fire negation",0.,100.,st.session_state.negfire,key="NEGFIRE",on_change=updateState,args=("NEGFIRE",),format="%.1f")
with cols[6]: st.number_input("Lightning negation",0.,100.,st.session_state.neglightning,key="NEGLIGHTNING",on_change=updateState,args=("NEGLIGHTNING",),format="%.1f")
with cols[7]: st.number_input("Holy negation",0.,100.,st.session_state.negholy,key="NEGHOLY",on_change=updateState,args=("NEGHOLY",),format="%.1f")
