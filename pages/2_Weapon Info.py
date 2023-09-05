import streamlit as st

from utils.utils import baseInfusions,weaponClasses,weaponsOfClass,ARcalculator,ARtoDMG
from utils.defaults import setDefaultDefStats

st.set_page_config(layout='wide',page_title="Weapon Info",page_icon="🔬")

if "defstandard" not in st.session_state:
    setDefaultDefStats()

cols=st.columns(5)
with cols[0]: st.number_input("STR",1,99,66)
with cols[1]: st.number_input("DEX",1,99,16)
with cols[2]: st.number_input("INT",1,99,9)
with cols[3]: st.number_input("FTH",1,99,9)
with cols[4]: st.number_input("ARC",1,99,7)

cols=st.columns(3)
with cols[0]: st.selectbox("Weapon class",weaponClasses,key="class")
with cols[1]: st.selectbox("Weapon",weaponsOfClass(st.session_state["class"]),key="weapon")
with cols[2]: st.selectbox("Infusion",baseInfusions,key="infusion")

cols=st.columns(8)
with cols[0]: st.number_input("Standard defense",0,400,st.session_state.defstandard)
with cols[1]: st.number_input("Strike defense",0,400,st.session_state.defstrike)
with cols[2]: st.number_input("Slash defense",0,400,st.session_state.defslash)
with cols[3]: st.number_input("Pierce defense",0,400,st.session_state.defpierce)
with cols[4]: st.number_input("Magic defense",0,400,st.session_state.defmagic)
with cols[5]: st.number_input("Fire defense",0,400,st.session_state.deffire)
with cols[6]: st.number_input("Lightning defense",0,400,st.session_state.deflightning)
with cols[7]: st.number_input("Holy defense",0,400,st.session_state.defholy)
cols=st.columns(8)
with cols[0]: st.number_input("Standard negation",0.,100.,st.session_state.negstandard,format="%.1f")
with cols[1]: st.number_input("Strike negation",0.,100.,st.session_state.negstrike,format="%.1f")
with cols[2]: st.number_input("Slash negation",0.,100.,st.session_state.negslash,format="%.1f")
with cols[3]: st.number_input("Pierce negation",0.,100.,st.session_state.negpierce,format="%.1f")
with cols[4]: st.number_input("Magic negation",0.,100.,st.session_state.negmagic,format="%.1f")
with cols[5]: st.number_input("Fire negation",0.,100.,st.session_state.negfire,format="%.1f")
with cols[6]: st.number_input("Lightning negation",0.,100.,st.session_state.neglightning,format="%.1f")
with cols[7]: st.number_input("Holy negation",0.,100.,st.session_state.negholy,format="%.1f")

st.text(ARcalculator(st.session_state.weapon,st.session_state.infusion,[st.session_state.STR,st.session_state.DEX,st.session_state.INT,st.session_state.FTH,st.session_state.ARC]))
