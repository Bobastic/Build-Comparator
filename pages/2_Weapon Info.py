import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

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
    #best=max(range(len(dmg)),key=lambda x:sum(dmg[x]))
    #labels=[l for i,l in enumerate(dmgTypes) if dmg[best][i]!=0]
    #sizes=[s for s in dmg[best] if s!=0]
    #fig,ax=plt.subplots()
    #ax.pie(sizes,labels=labels,autopct='%1.1f%%',labeldistance=None)
    #ax.legend()
    #st.subheader(f"Best infusion: {baseInfusions[best]}")
    dmg={i:ARcalculator(st.session_state.weapon,i,[st.session_state.STR,st.session_state.DEX,st.session_state.INT,st.session_state.FTH,st.session_state.ARC]) for i in baseInfusions}
    labels=sorted(baseInfusions,key=lambda x:sum(dmg[x]),reverse=True)
    data=np.array([dmg[l] for l in labels])
    data_cum=data.cumsum(axis=1)
    colors=["silver","silver","silver","silver","blue","red","yellow","orange"]
    fig,ax=plt.subplots()
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    for i,(dmgType,color) in enumerate(zip(dmgTypes,colors)):
        widths=data[:,i]
        starts=data_cum[:,i]-widths
        rects=ax.barh(labels,widths,left=starts,height=0.5,label=dmgType,color=color)
        r,g,b,_=to_rgba(color)
        text_color="white" if r*g*b<0.5 else "darkgrey"
        ax.bar_label(rects,label_type='center',color=text_color)
    ax.legend(ncols=8,bbox_to_anchor=(0,1),loc='lower left',fontsize='small')
    st.pyplot(fig)

    
    import plotly.graph_objects as go
    colors=["rgb(240, 242, 246)","rgb(240, 242, 246)","rgb(240, 242, 246)","rgb(240, 242, 246)","rgb(14, 90, 157)","rgb(214, 39, 40)","rgb(224, 210, 104)","rgb(255, 127, 14)"]
    fig=go.Figure()
    for i in range(8):
        fig.add_trace(go.Bar(y=baseInfusions,x=data[:,i],name=dmgTypes[i],orientation="h",text=data[:,i],marker={"color":colors[i]}))
    fig.update_layout(barmode='stack')
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
