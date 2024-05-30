import streamlit as st

def setDefaultBuilds():
    st.session_state.nBuilds = 4
    st.session_state["name0"] = "FS abuser"
    st.session_state["str0"] = 65
    st.session_state["dex0"] = 13
    st.session_state["int0"] = 9
    st.session_state["fth0"] = 9
    st.session_state["arc0"] = 7
    st.session_state["infusions0"] = ["Heavy"]
    st.session_state["name1"] = "Lightning abuser"
    st.session_state["str1"] = 14
    st.session_state["dex1"] = 65
    st.session_state["int1"] = 9
    st.session_state["fth1"] = 9
    st.session_state["arc1"] = 7
    st.session_state["infusions1"] = ["Keen", "Lightning"]
    st.session_state["name2"] = "Phalanx abuser"
    st.session_state["str2"] = 18
    st.session_state["dex2"] = 18
    st.session_state["int2"] = 50
    st.session_state["fth2"] = 9
    st.session_state["arc2"] = 7
    st.session_state["infusions2"] = ["Magic", "Cold"]
    st.session_state["name3"] = "SB abuser"
    st.session_state["str3"] = 18
    st.session_state["dex3"] = 18
    st.session_state["int3"] = 9
    st.session_state["fth3"] = 50
    st.session_state["arc3"] = 7
    st.session_state["infusions3"] = ["Sacred"]

def setDefaultWeapons():
    st.session_state.weapons = ["2H Shamshir", "Banished Knight's Halberd", "2H Estoc", "Wakizashi",
                              "Lance", "Noble's Slender Sword", "Iron Spear", "Star Fist"]

def setDefaultCalcParams():
    st.session_state.STR = 65
    st.session_state.DEX = 13
    st.session_state.INT = 9
    st.session_state.FTH = 9
    st.session_state.ARC = 7
    st.session_state.baseSTR = 14
    st.session_state.baseDEX = 13
    st.session_state.baseINT = 9
    st.session_state.baseFTH = 9
    st.session_state.baseARC = 7
    st.session_state.pts = 55

def setDefaultDefStats():
    st.session_state.defstandard = 140
    st.session_state.defstrike = 140
    st.session_state.defslash = 140
    st.session_state.defpierce = 140
    st.session_state.defmagic = 155
    st.session_state.deffire = 187
    st.session_state.deflightning = 127
    st.session_state.defholy = 155
    setNegations("beastmaster")

def setNegations(armorSet):
    negations = {
        "beastmaster": [33.0, 30.7, 34.7, 34.5, 25.8, 27.7, 25.4, 26.6],
        "fullgoat": [38.5, 38.2, 35.0, 35.0, 26.2, 26.5, 29.0, 25.4],
        "lionel": [33.6, 31.6, 36.5, 37.3, 26.5, 29.0, 25.6, 26.5]
    }[armorSet]
    st.session_state.negstandard = negations[0]
    st.session_state.negstrike = negations[1]
    st.session_state.negslash = negations[2]
    st.session_state.negpierce = negations[3]
    st.session_state.negmagic = negations[4]
    st.session_state.negfire = negations[5]
    st.session_state.neglightning = negations[6]
    st.session_state.negholy = negations[7]

def setDefaultTableOptions():
    st.session_state.compareBuilds = True
    st.session_state.compareClass = True
    st.session_state.hardtear = True
    st.session_state.eleTear = False
    st.session_state.greaseBuffs = True
    st.session_state.aowBuffs = True
    st.session_state.counterHits = True
    st.session_state.multicolor = True
    st.session_state.displayDmg = True
    st.session_state.displayPct = True
    st.session_state.showWeaponClass = False
    st.session_state.showStats = True
