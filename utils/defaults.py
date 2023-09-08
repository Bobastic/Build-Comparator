import streamlit as st

def setDefaultBuilds():
    st.session_state.nBuilds=4
    st.session_state["name0"]="FS abuser"
    st.session_state["str0"]=66
    st.session_state["dex0"]=16
    st.session_state["int0"]=9
    st.session_state["fth0"]=9
    st.session_state["arc0"]=7
    st.session_state["infusions0"]=["Heavy"]
    st.session_state["name1"]="Lightning abuser"
    st.session_state["str1"]=16
    st.session_state["dex1"]=66
    st.session_state["int1"]=9
    st.session_state["fth1"]=9
    st.session_state["arc1"]=7
    st.session_state["infusions1"]=["Keen","Lightning"]
    st.session_state["name2"]="Phalanx abuser"
    st.session_state["str2"]=21
    st.session_state["dex2"]=20
    st.session_state["int2"]=50
    st.session_state["fth2"]=9
    st.session_state["arc2"]=7
    st.session_state["infusions2"]=["Magic","Cold"]
    st.session_state["name3"]="SB abuser"
    st.session_state["str3"]=21
    st.session_state["dex3"]=20
    st.session_state["int3"]=9
    st.session_state["fth3"]=50
    st.session_state["arc3"]=7
    st.session_state["infusions3"]=["Sacred"]

def setDefaultWeapons():
    st.session_state.weapons=["2H Shamshir","Dismounter","Banished Knight's Halberd","2H Rogier's Rapier","Rogier's Rapier","Wakizashi",
                              "Lance","Longsword","Noble's Slender Sword","Short Spear","2H Godskin Stitcher","Star Fist","Katar"]

def setDefaultCalcParams():
    st.session_state.wClass="Halberds"
    st.session_state.weapon="Banished Knight's Halberd"
    st.session_state.STR=66
    st.session_state.DEX=16
    st.session_state.INT=9
    st.session_state.FTH=9
    st.session_state.ARC=7
    st.session_state.baseSTR=14
    st.session_state.baseDEX=13
    st.session_state.baseINT=9
    st.session_state.baseFTH=9
    st.session_state.baseARC=7
    st.session_state.pts=55

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
