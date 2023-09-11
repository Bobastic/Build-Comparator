import streamlit as st
import numpy as np
import plotly.graph_objects as go

from utils.utils import baseInfusions,weaponClasses,weaponsOfClass,ARcalculator,ARtoDMG,dmgTypes
from utils.defaults import setDefaultDefStats,setDefaultCalcParams

st.set_page_config(layout='wide',page_title="Weapon Optimizer",page_icon="⚖️")

if "wClass" not in st.session_state:
    setDefaultDefStats()
    setDefaultCalcParams()

if "weapon" not in st.session_state:
    st.write("coucou")

def updateState(key):
    st.session_state[key.replace("_","")]=st.session_state[key]

st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.5rem;
        }
        div[data-testid="column"]:nth-of-type(3) {
            display: flex;
            align-items: end;
        }
        h3 {
            text-align: center;
        }
        .appview-container .main .block-container {
            padding-top: 3rem;
        }
    </style>
""",unsafe_allow_html=True)

cols=st.columns([8,8,1])
with cols[0]: wClass=st.selectbox("Weapon class",weaponClasses)
with cols[1]: weapon=st.selectbox("Weapon",weaponsOfClass(wClass))
with cols[2]: twoH=st.toggle("2H")
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

bestInf,_,_,bestStats=st.columns([20,1,1,20])

with bestInf:
    st.subheader("Best infusion for stats")
    cols=st.columns(5)
    with cols[0]: st.number_input("STR",1,99,st.session_state.STR,key="STR_",on_change=updateState,args=("STR_",))
    with cols[1]: st.number_input("DEX",1,99,st.session_state.DEX,key="DEX_",on_change=updateState,args=("DEX_",))
    with cols[2]: st.number_input("INT",1,99,st.session_state.INT,key="INT_",on_change=updateState,args=("INT_",))
    with cols[3]: st.number_input("FTH",1,99,st.session_state.FTH,key="FTH_",on_change=updateState,args=("FTH_",))
    with cols[4]: st.number_input("ARC",1,99,st.session_state.ARC,key="ARC_",on_change=updateState,args=("ARC_",))
    plot=st.empty()
    cols=st.columns(3)
    with cols[0]: hardtear=st.toggle("Opaline Hardtear",value=True)
    with cols[1]: st.toggle("Counter Hits",key="counter_")
    with cols[2]: st.toggle("Weapon Buffs",key="buffs_")
    with plot:
        stats=[st.session_state.STR,st.session_state.DEX,st.session_state.INT,st.session_state.FTH,st.session_state.ARC]
        defenses=[st.session_state.defstandard,st.session_state.defstrike,st.session_state.defslash,st.session_state.defpierce,
                  st.session_state.defmagic,st.session_state.deffire,st.session_state.deflightning,st.session_state.defholy]
        negations=[st.session_state.negstandard,st.session_state.negstrike,st.session_state.negslash,st.session_state.negpierce,
                  st.session_state.negmagic,st.session_state.negfire,st.session_state.neglightning,st.session_state.negholy]
        nBest=10
        weapon=f"{'2H ' if twoH else ''}{weapon}"
        data=np.array([ARtoDMG(ARcalculator(weapon,i,stats),defenses,negations) for i in baseInfusions])
        data=data[~np.all(data==0,axis=1)]
        st.markdown(data)
        labels=baseInfusions if len(data)>1 else ["Standard"]
        labels=[labels[i] for i in sorted(range(len(labels)),key=lambda x:sum(data[x,:]))][-nBest:]
        data=data[np.argsort(data.sum(axis=1))[-nBest:]] # we sort by total and keep the best
        colors=["rgb(240, 242, 246)","rgb(240, 242, 246)","rgb(240, 242, 246)","rgb(240, 242, 246)","rgba(14, 90, 157, 0.3)","rgba(214, 39, 40, 0.3)","rgba(255, 225, 53, 0.3)","rgba(255, 127, 14, 0.3)"]
        width=[0.8]*len(labels) if len(labels)>1 else [0.15]
        fig=go.Figure()
        for i in range(8):
            fig.add_trace(go.Bar(x=data[:,i],y=labels,name=dmgTypes[i],orientation="h",width=width,
                                 text=[round(d) for d in data[:,i]],marker={"color":colors[i]},showlegend=bool(data[:,i].sum()!=0),insidetextfont={"size":14},textangle=0))
        fig.add_trace(go.Scatter(x=data.sum(axis=1),y=labels,text=[f"  {d:.0f}" for d in data.sum(axis=1)],mode='text',textfont={"size":14},textposition="middle right",showlegend=False))
        fig.update_layout(barmode='stack',legend_traceorder="normal",margin=go.layout.Margin(l=0,r=0,b=0,t=0),legend={"orientation":"h","yanchor":"bottom","y":1.02}) #autosize=False,height=350
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

with bestStats:
    st.subheader("Best stats for infusion")
    cols=st.columns(5)
    with cols[0]: st.number_input("Base STR",1,99,st.session_state.baseSTR,key="baseSTR_",on_change=updateState,args=("baseSTR_",))
    with cols[1]: st.number_input("Base DEX",1,99,st.session_state.baseDEX,key="baseDEX_",on_change=updateState,args=("baseDEX_",))
    with cols[2]: st.number_input("Base INT",1,99,st.session_state.baseINT,key="baseINT_",on_change=updateState,args=("baseINT_",))
    with cols[3]: st.number_input("Base FTH",1,99,st.session_state.baseFTH,key="baseFTH_",on_change=updateState,args=("baseFTH_",))
    with cols[4]: st.number_input("Base ARC",1,99,st.session_state.baseARC,key="baseARC_",on_change=updateState,args=("baseARC_",))
    cols=st.columns(3)
    with cols[0]: st.selectbox("Infusion",baseInfusions,key="infusion__",on_change=updateState,args=("infusion__",))
    with cols[1]: pts=st.number_input("Stat points to allocate",0,813,st.session_state.pts,key="pts_",on_change=updateState,args=("pts_",))
    with cols[2]: st.info("A base Vagabond with 60 VIG and 27 END has 55 points left for RL 125.")
    stats_=[st.session_state.baseSTR,st.session_state.baseDEX,st.session_state.baseINT,st.session_state.baseFTH,st.session_state.baseARC]
    dmg=0
    while pts>0:
        for i,stat in enumerate(stats):
            tmpDmg=ARtoDMG(ARcalculator(weapon,st.session_state.infusion,stats_),defenses,negations)
            if tmpDmg>dmg:
                dmg=tmpDmg
                lvlUp=i
        stats[i]+=1
        pts-=1
    st.markdown(stats)
