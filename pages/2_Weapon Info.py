import streamlit as st
import numpy as np
import plotly.graph_objects as go

from utils.utils import baseInfusions,weaponClasses,weaponsOfClass,ARcalculator,ARtoDMG,dmgTypes
from utils.defaults import setDefaultDefStats

st.set_page_config(layout='wide',page_title="Weapon Info",page_icon="🔬")

if "defstandard" not in st.session_state:
    setDefaultDefStats()

st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size:1.5rem;
        }
    </style>
""",unsafe_allow_html=True)

info,allocate,bic=st.tabs(["Weapon Info","Allocate Stats","Best of class"])

with info:
    cols=st.columns(2)
    with cols[0]: st.selectbox("Weapon class",weaponClasses,key="class")
    with cols[1]: st.selectbox("Weapon",weaponsOfClass(st.session_state["class"]),key="weapon",index=3)
    cols=st.columns(5)
    with cols[0]: st.number_input("STR",1,99,66,key="STR")
    with cols[1]: st.number_input("DEX",1,99,16,key="DEX")
    with cols[2]: st.number_input("INT",1,99,9,key="INT")
    with cols[3]: st.number_input("FTH",1,99,9,key="FTH")
    with cols[4]: st.number_input("ARC",1,99,7,key="ARC")
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
    st.divider()
    stats=[st.session_state.STR,st.session_state.DEX,st.session_state.INT,st.session_state.FTH,st.session_state.ARC]
    defenses=[st.session_state.defstandard,st.session_state.defstrike,st.session_state.defslash,st.session_state.defpierce,
              st.session_state.defmagic,st.session_state.deffire,st.session_state.deflightning,st.session_state.defholy]
    negations=[st.session_state.negstandard,st.session_state.negstrike,st.session_state.negslash,st.session_state.negpierce,
              st.session_state.negmagic,st.session_state.negfire,st.session_state.neglightning,st.session_state.negholy]
    data=np.array([ARtoDMG(ARcalculator(st.session_state.weapon,i,stats),defenses,negations) for i in baseInfusions])
    st.table(data)
    labels=[baseInfusions[i] for i in sorted(range(len(baseInfusions)),key=data.sum(axis=1))][:10]
    st.write(f"{baseInfusions}{labels}")
    data=data[np.argsort(data.sum(axis=1))[:10]] # we sort by total and keep the top 10
    colors=["rgb(240, 242, 246)","rgb(240, 242, 246)","rgb(240, 242, 246)","rgb(240, 242, 246)","rgba(14, 90, 157, 0.3)","rgba(214, 39, 40, 0.3)","rgba(255, 225, 53, 0.3)","rgba(255, 127, 14, 0.3)"]
    fig=go.Figure()
    for i in range(8):
        fig.add_trace(go.Bar(x=data[:,i],y=labels,name=dmgTypes[i],orientation="h",text=[round(d) for d in data[:,i]],marker={"color":colors[i]}))
    fig.add_trace(go.Scatter(x=data.sum(axis=1),y=labels,text=[f"  {d:.0f}" for d in data.sum(axis=1)],mode='text',textfont={"size":12},textposition="middle right",showlegend=False))
    fig.update_layout(barmode='stack',legend_traceorder="normal")
    st.plotly_chart(fig)

with allocate:
    cols=st.columns(3)
    with cols[0]: st.selectbox("Weapon class",weaponClasses,key="class2")
    with cols[1]: st.selectbox("Weapon",weaponsOfClass(st.session_state["class2"]),key="weapon2",index=3)
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

with bic:
    cols=st.columns(5)
    with cols[0]: st.number_input("STR",1,99,66,key="STR3")
    with cols[1]: st.number_input("DEX",1,99,16,key="DEX3")
    with cols[2]: st.number_input("INT",1,99,9,key="INT3")
    with cols[3]: st.number_input("FTH",1,99,9,key="FTH3")
    with cols[4]: st.number_input("ARC",1,99,7,key="ARC3")
    cols=st.columns(3)
    with cols[0]: st.selectbox("Weapon class",weaponClasses,key="class3")
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
