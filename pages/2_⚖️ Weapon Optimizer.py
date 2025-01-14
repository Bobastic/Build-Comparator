import streamlit as 
import numpy as np
import plotly.graph_objects as go

from utils.utils import weaponsOfClass, ARcalculator, ARtoDMG, isInfusable
from utils.defaults import setDefaultDefStats, setDefaultCalcParams
from utils.constants import baseInfusions, weaponClasses, dmgTypes

for k in st.session_state:
    st.session_state[k] = st.session_state[k]

st.set_page_config(layout='wide', page_title="Weapon Optimizer", page_icon="⚖️")

if "defstandard" not in st.session_state:
    setDefaultDefStats()

if "reinforcementLvl" not in st.session_state:
    st.session_state.reinforcementLvl = 25

if "STR" not in st.session_state:
    setDefaultCalcParams()

st.html("""
<style>
    /* Center Best Infusion and Optimal Stats */
    h3 {
        text-align: center;
    }
    /* Drag the 2H switch down */
    div[data-testid="column"]:nth-of-type(4) {
        display: flex;
        flex-direction: column-reverse;       /* evil css hack */
    }
    /* Center text in metrics cards */
    div[data-testid="stMetric"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    /* Removes useless space on top */
    .appview-container .main .block-container {
        padding-top: 4rem;
    }
</style>
""")

st.sidebar.info("Default enemy defenses are the average of classic STR, DEX, INT, FTH and ARC builds.")
st.sidebar.info("Default enemy negations are Imp/Beast Champion (Altered)/Beast Champion/Beast Champion.")
st.sidebar.info("The damage you see is post enemy defenses and negations.")
st.sidebar.info("Attacks have a motion value of 100 (usually R1).")
st.sidebar.info("The physical damage type is the most common one for the weapon (Standard for Longsword, Slash for Wakizashi etc...)")

def resetWeapon():
    del st.session_state.weapon

def resetInfusion():
    del st.session_state.infusion

cols=st.columns([7,7,2,1])
with cols[0]: st.selectbox("Weapon class", weaponClasses, key="wClass", on_change=lambda : (resetWeapon(), resetInfusion()))
with cols[1]: st.selectbox("Weapon", weaponsOfClass(st.session_state.wClass), key="weapon", on_change=resetInfusion)
with cols[2]: st.number_input("Weapon Level", 0, 25, key="reinforcementLvl",
                              help="NORMAL weapon level from 0 to 25. Somber level is automatically calculated from this. Applies to all weapons.")
with cols[3]: st.toggle("2H", key="twoH")
cols=st.columns(8)
with cols[0]: st.number_input("Standard defense", 0, 400, key="defstandard")
with cols[1]: st.number_input("Strike defense", 0, 400, key="defstrike")
with cols[2]: st.number_input("Slash defense", 0, 400, key="defslash")
with cols[3]: st.number_input("Pierce defense", 0, 400, key="defpierce")
with cols[4]: st.number_input("Magic defense", 0, 400, key="defmagic")
with cols[5]: st.number_input("Fire defense", 0, 400, key="deffire")
with cols[6]: st.number_input("Lightning defense", 0, 400, key="deflightning")
with cols[7]: st.number_input("Holy defense", 0, 400, key="defholy")
cols=st.columns(8)
with cols[0]: st.number_input("Standard negation", 0., 100., key="negstandard", format="%.1f", step=0.1)
with cols[1]: st.number_input("Strike negation", 0., 100., key="negstrike", format="%.1f", step=0.1)
with cols[2]: st.number_input("Slash negation", 0., 100., key="negslash", format="%.1f", step=0.1)
with cols[3]: st.number_input("Pierce negation", 0., 100., key="negpierce", format="%.1f", step=0.1)
with cols[4]: st.number_input("Magic negation", 0., 100., key="negmagic", format="%.1f", step=0.1)
with cols[5]: st.number_input("Fire negation", 0., 100., key="negfire", format="%.1f", step=0.1)
with cols[6]: st.number_input("Lightning negation", 0., 100., key="neglightning", format="%.1f", step=0.1)
with cols[7]: st.number_input("Holy negation", 0., 100., key="negholy", format="%.1f", step=0.1)

st.divider()

infusions = baseInfusions if isInfusable(st.session_state.weapon) else ["Standard"]

bestInf, _, bestStats = st.columns([20,1,20])

with bestInf:
    st.subheader("🧪 Best Infusion 🧪")
    cols = st.columns(5)
    with cols[0]: st.number_input("STR", 1, 99, key="STR")
    with cols[1]: st.number_input("DEX", 1, 99, key="DEX")
    with cols[2]: st.number_input("INT", 1, 99, key="INT")
    with cols[3]: st.number_input("FTH", 1, 99, key="FTH")
    with cols[4]: st.number_input("ARC", 1, 99, key="ARC")
    plot = st.empty()
    #cols=st.columns(3)
    #with cols[0]: st.toggle("Opaline Hardtear", key="hardtear", value=True)
    #with cols[1]: st.toggle("Counter Hits", key="counter_")
    #with cols[2]: st.toggle("Weapon Buffs", key="buffs_")
    with plot:
        stats = [st.session_state.STR, st.session_state.DEX, st.session_state.INT, st.session_state.FTH, st.session_state.ARC]
        defenses = [st.session_state.defstandard, st.session_state.defstrike, st.session_state.defslash, st.session_state.defpierce, 
                    st.session_state.defmagic, st.session_state.deffire, st.session_state.deflightning, st.session_state.defholy]
        negations = [st.session_state.negstandard, st.session_state.negstrike, st.session_state.negslash, st.session_state.negpierce, 
                     st.session_state.negmagic, st.session_state.negfire, st.session_state.neglightning, st.session_state.negholy]
        nBest = 7
        weapon = f"{'2H ' if st.session_state.twoH else ''}{st.session_state.weapon}"
        data = np.array([ARtoDMG(ARcalculator(weapon, i, stats, st.session_state.reinforcementLvl), defenses, negations) for i in infusions])
        labels = [infusions[i] for i in sorted(range(len(infusions)), key=lambda x:sum(data[x,:]))][-nBest:]
        data = data[np.argsort(data.sum(axis=1))[-nBest:]] # we sort by total and keep the best
        colors = ["rgb(240, 242, 246)","rgb(240, 242, 246)","rgb(240, 242, 246)","rgb(240, 242, 246)","rgba(14, 90, 157, 0.3)",
                  "rgba(214, 39, 40, 0.3)","rgba(255, 225, 53, 0.3)","rgba(255, 127, 14, 0.3)"]
        width = [0.8]*len(labels) if len(labels) > 1 else [0.15]
        fig = go.Figure()
        for i in range(8):
            fig.add_trace(go.Bar(x=data[:,i], y=labels, name=dmgTypes[i], orientation="h", width=width, hoverinfo="skip",
                                 text=[round(d) for d in data[:,i]], marker={"color":colors[i]}, showlegend=bool(data[:,i].sum()!=0), insidetextfont={"size":14}, textangle=0))
        fig.add_trace(go.Scatter(x=data.sum(axis=1), y=labels, text=[f"  {d:.0f}" for d in data.sum(axis=1)],
                                 mode='text', textfont={"size":14}, textposition="middle right", showlegend=False, hoverinfo="skip"))
        fig.update_layout(barmode='stack', legend_traceorder="normal", margin=go.layout.Margin(l=0, r=0, b=0, t=0), autosize=False, height=350, legend={"orientation":"h", "yanchor":"bottom", "y":1.02})
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

with bestStats:
    st.subheader("📊 Optimal Stats 📊")
    cols = st.columns(5)
    with cols[0]: st.number_input("Base STR", 1, 99, key="baseSTR")
    with cols[1]: st.number_input("Base DEX", 1, 99, key="baseDEX")
    with cols[2]: st.number_input("Base INT", 1, 99, key="baseINT")
    with cols[3]: st.number_input("Base FTH", 1, 99, key="baseFTH")
    with cols[4]: st.number_input("Base ARC", 1, 99, key="baseARC")
    cols = st.columns(2)
    with cols[0]: st.selectbox("Infusion", infusions, key="infusion")
    with cols[1]: st.number_input("Stat points to allocate", 0, 813, key="pts")
    st.info("A base Vagabond with 60 VIG and 27 END has 55 points left to allocate to reach RL 125.")
    with st.spinner("Computing optimal stats..."):
        bestStats = [st.session_state.baseSTR, st.session_state.baseDEX, st.session_state.baseINT, st.session_state.baseFTH, st.session_state.baseARC]
        dmg = 0
        for _ in range(st.session_state.pts):
            for i in range(5):
                tmpStats = bestStats[:]
                tmpStats[i] += 1
                tmpDmg = ARtoDMG(ARcalculator(weapon, st.session_state.infusion, tmpStats, st.session_state.reinforcementLvl), defenses, negations)
                if sum(tmpDmg) > dmg:
                    dmg = sum(tmpDmg)
                    lvlUp = i
            bestStats[lvlUp] += 1
        cols = st.columns(5)
        with cols[0]: st.metric("Optimal STR", bestStats[0])
        with cols[1]: st.metric("Optimal DEX", bestStats[1])
        with cols[2]: st.metric("Optimal INT", bestStats[2])
        with cols[3]: st.metric("Optimal FTH", bestStats[3])
        with cols[4]: st.metric("Optimal ARC", bestStats[4])
        st.metric(f"Optimal Damage", int(dmg), f"{+100*dmg/sum(data[-1,:])-100:.1f}%", help="Difference with current best infusion damage.")
