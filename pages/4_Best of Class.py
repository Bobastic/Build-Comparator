import streamlit as st
import numpy as np
import plotly.graph_objects as go

from utils.utils import baseInfusions,weaponClasses,weaponsOfClass,ARcalculator,ARtoDMG,dmgTypes
from utils.defaults import setDefaultDefStats

st.set_page_config(layout='wide',page_title="Weapon Info",page_icon="🔬")

if "wClass" not in st.session_state:
    setDefaultDefStats()
    st.session_state.STR=66
    st.session_state.DEX=16
    st.session_state.INT=9
    st.session_state.FTH=9
    st.session_state.ARC=7
    st.session_state.wClass="Halberds"
    st.session_state.weapon="Banished Knight's Halberd"

def updateState(key):
        st.session_state[key.replace("_","")]=st.session_state[key]

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
    with cols[0]: st.selectbox("Weapon class",weaponClasses,key="wClass_",on_change=updateState,args=("wClass_",))
    with cols[1]: st.selectbox("Weapon",weaponsOfClass(st.session_state["wClass"]),index=3,key="weapon_",on_change=updateState,args=("weapon_",))
    cols=st.columns(5)
    with cols[0]: st.number_input("STR",1,99,st.session_state.STR,key="STR_",on_change=updateState,args=("STR_",))
    with cols[1]: st.number_input("DEX",1,99,st.session_state.DEX,key="DEX_",on_change=updateState,args=("DEX_",))
    with cols[2]: st.number_input("INT",1,99,st.session_state.INT,key="INT_",on_change=updateState,args=("INT_",))
    with cols[3]: st.number_input("FTH",1,99,st.session_state.FTH,key="FTH_",on_change=updateState,args=("FTH_",))
    with cols[4]: st.number_input("ARC",1,99,st.session_state.ARC,key="ARC_",on_change=updateState,args=("ARC_",))
    cols=st.columns(8)
    with cols[0]: st.number_input("Standard defense",0,400,st.session_state.defstandard,key="defstandard_",on_change=updateState,args=("defstandard_",))
    with cols[1]: st.number_input("Strike defense",0,400,st.session_state.defstrike,key="defstrike_",on_change=updateState,args=("defstrike_",))
    with cols[2]: st.number_input("Slash defense",0,400,st.session_state.defslash,key="defslash_",on_change=updateState,args=("defslash_",))
    with cols[3]: st.number_input("Pierce defense",0,400,st.session_state.defpierce,key="defpierce_",on_change=updateState,args=("defpierce_",))
    with cols[4]: st.number_input("Magic defense",0,400,st.session_state.defmagic,key="defmagic_",on_change=updateState,args=("defmagic_",))
    with cols[5]: st.number_input("Fire defense",0,400,st.session_state.deffire,key="deffire_",on_change=updateState,args=("deffire_",))
    with cols[6]: st.number_input("Lightning defense",0,400,st.session_state.deflightning,key="deflightning_",on_change=updateState,args=("deflightning_",))
    with cols[7]: st.number_input("Holy defense",0,400,st.session_state.defholy,key="defholy_",on_change=updateState,args=("defholy_",))
    cols=st.columns(8)
    with cols[0]: st.number_input("Standard negation",0.,100.,st.session_state.negstandard,format="%.1f",key="negstandard_",on_change=updateState,args=("negstandard_",))
    with cols[1]: st.number_input("Strike negation",0.,100.,st.session_state.negstrike,format="%.1f",key="negstrike_",on_change=updateState,args=("negstrike_",))
    with cols[2]: st.number_input("Slash negation",0.,100.,st.session_state.negslash,format="%.1f",key="negslash_",on_change=updateState,args=("negslash_",))
    with cols[3]: st.number_input("Pierce negation",0.,100.,st.session_state.negpierce,format="%.1f",key="negpierce_",on_change=updateState,args=("negpierce_",))
    with cols[4]: st.number_input("Magic negation",0.,100.,st.session_state.negmagic,format="%.1f",key="negmagic_",on_change=updateState,args=("negmagic_",))
    with cols[5]: st.number_input("Fire negation",0.,100.,st.session_state.negfire,format="%.1f",key="negfire_",on_change=updateState,args=("negfire_",))
    with cols[6]: st.number_input("Lightning negation",0.,100.,st.session_state.neglightning,format="%.1f",key="neglightning_",on_change=updateState,args=("neglightning_",))
    with cols[7]: st.number_input("Holy negation",0.,100.,st.session_state.negholy,format="%.1f",key="negholy_",on_change=updateState,args=("negholy_",))
    st.divider()
    cols=st.columns(2)
    with cols[0]:
        stats=[st.session_state.STR,st.session_state.DEX,st.session_state.INT,st.session_state.FTH,st.session_state.ARC]
        defenses=[st.session_state.defstandard,st.session_state.defstrike,st.session_state.defslash,st.session_state.defpierce,
                  st.session_state.defmagic,st.session_state.deffire,st.session_state.deflightning,st.session_state.defholy]
        negations=[st.session_state.negstandard,st.session_state.negstrike,st.session_state.negslash,st.session_state.negpierce,
                  st.session_state.negmagic,st.session_state.negfire,st.session_state.neglightning,st.session_state.negholy]
        nBest=20
        data=np.array([ARtoDMG(ARcalculator(st.session_state.weapon,i,stats),defenses,negations) for i in baseInfusions])
        labels=[baseInfusions[i] for i in sorted(range(len(baseInfusions)),key=lambda x:sum(data[x,:]))][-nBest:]
        data=data[np.argsort(data.sum(axis=1))[-nBest:]] # we sort by total and keep the best
        colors=["rgb(240, 242, 246)","rgb(240, 242, 246)","rgb(240, 242, 246)","rgb(240, 242, 246)","rgba(14, 90, 157, 0.3)","rgba(214, 39, 40, 0.3)","rgba(255, 225, 53, 0.3)","rgba(255, 127, 14, 0.3)"]
        fig=go.Figure()
        for i in range(8):
            fig.add_trace(go.Bar(x=data[:,i],y=labels,name=dmgTypes[i],orientation="h",
                                 text=[round(d) for d in data[:,i]],marker={"color":colors[i]},showlegend=bool(data[:,i].sum()!=0),insidetextfont={"size":14},textangle=0))
        fig.add_trace(go.Scatter(x=data.sum(axis=1),y=labels,text=[f"  {d:.0f}" for d in data.sum(axis=1)],mode='text',textfont={"size":14},textposition="middle right",showlegend=False))
        fig.update_layout(barmode='stack',legend_traceorder="normal",margin=go.layout.Margin(l=0,r=0,b=0,t=0),legend={"orientation":"h","yanchor":"bottom","y":1.02}) #autosize=False,height=350
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

with allocate:
    cols=st.columns(3)
    with cols[0]: st.selectbox("Weapon class",weaponClasses,key="wClass__",on_change=updateState,args=("wClass__",))
    with cols[1]: st.selectbox("Weapon",weaponsOfClass(st.session_state["wClass"]),index=3,key="weapon__",on_change=updateState,args=("weapon__",))
    with cols[2]: st.selectbox("Infusion",baseInfusions,key="infusion__",on_change=updateState,args=("infusion__",))
    cols=st.columns(8)
    with cols[0]: st.number_input("Standard defense",0,400,st.session_state.defstandard,key="defstandard__",on_change=updateState,args=("defstandard__",))
    with cols[1]: st.number_input("Strike defense",0,400,st.session_state.defstrike,key="defstrike__",on_change=updateState,args=("defstrike__",))
    with cols[2]: st.number_input("Slash defense",0,400,st.session_state.defslash,key="defslash__",on_change=updateState,args=("defslash__",))
    with cols[3]: st.number_input("Pierce defense",0,400,st.session_state.defpierce,key="defpierce__",on_change=updateState,args=("defpierce__",))
    with cols[4]: st.number_input("Magic defense",0,400,st.session_state.defmagic,key="defmagic__",on_change=updateState,args=("defmagic__",))
    with cols[5]: st.number_input("Fire defense",0,400,st.session_state.deffire,key="deffire__",on_change=updateState,args=("deffire__",))
    with cols[6]: st.number_input("Lightning defense",0,400,st.session_state.deflightning,key="deflightning__",on_change=updateState,args=("deflightning__",))
    with cols[7]: st.number_input("Holy defense",0,400,st.session_state.defholy,key="defholy__",on_change=updateState,args=("defholy__",))
    cols=st.columns(8)
    with cols[0]: st.number_input("Standard negation",0.,100.,st.session_state.negstandard,format="%.1f",key="negstandard__",on_change=updateState,args=("negstandard__",))
    with cols[1]: st.number_input("Strike negation",0.,100.,st.session_state.negstrike,format="%.1f",key="negstrike__",on_change=updateState,args=("negstrike__",))
    with cols[2]: st.number_input("Slash negation",0.,100.,st.session_state.negslash,format="%.1f",key="negslash__",on_change=updateState,args=("negslash__",))
    with cols[3]: st.number_input("Pierce negation",0.,100.,st.session_state.negpierce,format="%.1f",key="negpierce__",on_change=updateState,args=("negpierce__",))
    with cols[4]: st.number_input("Magic negation",0.,100.,st.session_state.negmagic,format="%.1f",key="negmagic__",on_change=updateState,args=("negmagic__",))
    with cols[5]: st.number_input("Fire negation",0.,100.,st.session_state.negfire,format="%.1f",key="negfire__",on_change=updateState,args=("negfire__",))
    with cols[6]: st.number_input("Lightning negation",0.,100.,st.session_state.neglightning,format="%.1f",key="neglightning__",on_change=updateState,args=("neglightning__",))
    with cols[7]: st.number_input("Holy negation",0.,100.,st.session_state.negholy,format="%.1f",key="negholy__",on_change=updateState,args=("negholy__",))

with bic:
    st.selectbox("Weapon class",weaponClasses,key="wClass___",on_change=updateState,args=("wClass___",))
    cols=st.columns(5)
    with cols[0]: st.number_input("STR",1,99,66,key="STR___",on_change=updateState,args=("STR___",))
    with cols[1]: st.number_input("DEX",1,99,16,key="DEX___",on_change=updateState,args=("DEX___",))
    with cols[2]: st.number_input("INT",1,99,9,key="INT___",on_change=updateState,args=("INT___",))
    with cols[3]: st.number_input("FTH",1,99,9,key="FTH___",on_change=updateState,args=("FTH___",))
    with cols[4]: st.number_input("ARC",1,99,7,key="ARC___",on_change=updateState,args=("ARC___",))
    cols=st.columns(8)
    with cols[0]: st.number_input("Standard defense",0,400,st.session_state.defstandard,key="defstandard___",on_change=updateState,args=("defstandard___",))
    with cols[1]: st.number_input("Strike defense",0,400,st.session_state.defstrike,key="defstrike___",on_change=updateState,args=("defstrike___",))
    with cols[2]: st.number_input("Slash defense",0,400,st.session_state.defslash,key="defslash___",on_change=updateState,args=("defslash___",))
    with cols[3]: st.number_input("Pierce defense",0,400,st.session_state.defpierce,key="defpierce___",on_change=updateState,args=("defpierce___",))
    with cols[4]: st.number_input("Magic defense",0,400,st.session_state.defmagic,key="defmagic___",on_change=updateState,args=("defmagic___",))
    with cols[5]: st.number_input("Fire defense",0,400,st.session_state.deffire,key="deffire___",on_change=updateState,args=("deffire___",))
    with cols[6]: st.number_input("Lightning defense",0,400,st.session_state.deflightning,key="deflightning___",on_change=updateState,args=("deflightning___",))
    with cols[7]: st.number_input("Holy defense",0,400,st.session_state.defholy,key="defholy___",on_change=updateState,args=("defholy___",))
    cols=st.columns(8)
    with cols[0]: st.number_input("Standard negation",0.,100.,st.session_state.negstandard,format="%.1f",key="negstandard___",on_change=updateState,args=("negstandard___",))
    with cols[1]: st.number_input("Strike negation",0.,100.,st.session_state.negstrike,format="%.1f",key="negstrike___",on_change=updateState,args=("negstrike___",))
    with cols[2]: st.number_input("Slash negation",0.,100.,st.session_state.negslash,format="%.1f",key="negslash___",on_change=updateState,args=("negslash___",))
    with cols[3]: st.number_input("Pierce negation",0.,100.,st.session_state.negpierce,format="%.1f",key="negpierce___",on_change=updateState,args=("negpierce___",))
    with cols[4]: st.number_input("Magic negation",0.,100.,st.session_state.negmagic,format="%.1f",key="negmagic___",on_change=updateState,args=("negmagic___",))
    with cols[5]: st.number_input("Fire negation",0.,100.,st.session_state.negfire,format="%.1f",key="negfire___",on_change=updateState,args=("negfire___",))
    with cols[6]: st.number_input("Lightning negation",0.,100.,st.session_state.neglightning,format="%.1f",key="neglightning___",on_change=updateState,args=("neglightning___",))
    with cols[7]: st.number_input("Holy negation",0.,100.,st.session_state.negholy,format="%.1f",key="negholy___",on_change=updateState,args=("negholy___",))