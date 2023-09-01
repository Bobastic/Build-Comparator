import streamlit as st

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
    st.session_state.weapons=["2H Shamshir","Dismounter","Banished Knight's Halberd","2H Rogier's Rapier","Rogier's Rapier","Wakizashi",
                              "Lance","Longsword","Noble's Slender Sword","Short Spear","2H Godskin Stitcher","Star Fist","Katar"]

def setDefaultDefStats():
    st.session_state.defstandard=140
    st.session_state.defstrike=140
    st.session_state.defslash=140
    st.session_state.defpierce=140
    st.session_state.defmagic=155
    st.session_state.deffire=187
    st.session_state.deflightning=127
    st.session_state.defholy=155
    st.session_state.negstandard=33.3
    st.session_state.negstrike=30.9
    st.session_state.negslash=34.9
    st.session_state.negpierce=35.1
    st.session_state.negmagic=26.2
    st.session_state.negfire=29.3
    st.session_state.neglightning=25.5
    st.session_state.negholy=26.6
