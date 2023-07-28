import streamlit as st

from utils.utils import baseInfusions

st.set_page_config(layout='wide',page_title="Parameters",page_icon="🛠️")

if "builds" not in st.session_state:
    init=True
    st.session_state.builds=[
        {"name":"FS abuser","STR":66,"DEX":16,"INT":9,"FTH":9,"ARC":7,"infusions":["Heavy","Fire"]},
        {"name":"Phalanx abuser","STR":21,"DEX":20,"INT":50,"FTH":9,"ARC":7,"infusions":["Magic","Cold"]},
        {"name":"SB abuser","STR":21,"DEX":20,"INT":9,"FTH":50,"ARC":7,"infusions":["Sacred"]},
    ]

def addBuild():
    st.session_state.builds.append({"name":f"Build {len(st.session_state.builds)}","STR":14,"DEX":13,"INT":9,"FTH":9,"ARC":7,"infusions":[]})

def removeBuild():
    if len(st.session_state.builds)>0:
        st.session_state.builds=st.session_state.builds[:-1]

cols=st.columns([4,2,2,2,2,2,5])
with cols[0]: st.subheader("Build name")
with cols[1]: st.subheader("STR")
with cols[2]: st.subheader("DEX")
with cols[3]: st.subheader("INT")
with cols[4]: st.subheader("FTH")
with cols[5]: st.subheader("ARC")
with cols[6]: st.subheader("Infusions")
for i in range(len(st.session_state.builds)):
    cols=st.columns([4,2,2,2,2,2,5])
    with cols[0]: st.session_state[f"name{i}"]=st.text_input("Build name",value=st.session_state.builds[i]["name"],key=f"name{i}",label_visibility="collapsed")
    with cols[1]: st.session_state[f"STR{i}"]=st.number_input("STR",1,99,st.session_state.builds[i]["STR"],key=f"STR{i}",label_visibility="collapsed")
    with cols[2]: st.session_state[f"DEX{i}"]=st.number_input("DEX",1,99,st.session_state.builds[i]["DEX"],key=f"DEX{i}",label_visibility="collapsed")
    with cols[3]: st.session_state[f"INT{i}"]=st.number_input("INT",1,99,st.session_state.builds[i]["INT"],key=f"INT{i}",label_visibility="collapsed")
    with cols[4]: st.session_state[f"FTH{i}"]=st.number_input("FTH",1,99,st.session_state.builds[i]["FTH"],key=f"FTH{i}",label_visibility="collapsed")
    with cols[5]: st.session_state[f"ARC{i}"]=st.number_input("ARC",1,99,st.session_state.builds[i]["ARC"],key=f"ARC{i}",label_visibility="collapsed")
    with cols[6]: st.session_state[f"infusions{i}"]=st.multiselect("Infusions",baseInfusions,default=st.session_state.builds[i]["infusions"],key=f"infusions{i}",label_visibility="collapsed")

cols=st.columns([5,1,1,5])
with cols[1]: add=st.button("Add Build",on_click=addBuild,type="primary")
with cols[2]: rem=st.button("Rem. Build",on_click=removeBuild,disabled=len(st.session_state.builds)==0)

init=False

print(st.session_state)


## rendre les input non modifiables?