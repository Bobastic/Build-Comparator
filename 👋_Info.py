import streamlit as 

for k in st.session_state:
    st.session_state[k] = st.session_state[k]

st.set_page_config(layout='centered', page_title="Build Comparator", page_icon="⚖️")

st.html("""
<style>
    p {
        text-align: justify;
    }
    /* Removes useless space on top */
    .appview-container .main .block-container {
        padding-top: 4rem;
    }
</style>
""")

st.sidebar.info("Hi. Check this page for some information about this tool or head straight to **🔬 Build Comparator** or **⚖️ Weapon Optimizer** to figure it out by yourself.")

st.subheader("What is the purpose of this tool?")

st.markdown("""
There are already lots of tools for build optimization, mainly in the form of spreadsheets or Slugbot.
However, I could not find a way to compare whole builds together.
Usually you get tools for optimal infusion, optimal stats but always for one weapon or weapon class.
There isn't to my knowledge a way to see the damage values of a **whole inventory** across **multiple builds**. So I made one.
I also added other functionalities like an infusion optimizer or a stat allocator.
""")

st.subheader("Use case examples")

st.markdown("""
- How much more damage do I get with 69 STR compared to 54 STR on all these weapons?
- Lightning or Keen?
- Is Cold -> Lightning better than Cold -> Magic for this inventory?
- Fire + Flaming Strike buff or Heavy + Lightning Grease?
- How broken is Sacred Blade?
- What is the best build for Star Fists between these three?
- Best infusion and stat spread for Shamshir?
""")

st.subheader("**🔬 Build Comparator**")

st.markdown("""
Input a list of **weapons** of your choice and as many **builds** and **infusions** as you like and you get a table with estimated damage that is widely customizable.
You can display counter damage, comparisons with the best infusion etc...
There are already some default weapons and builds so you can go straight to any page to see what this tool can do.
""")

st.subheader("**⚖️ Weapon Optimizer**")

st.markdown("""
Pick a weapon and you'll have estimated damage for each infusion with the specified stat spread.
On the right you will find the optimal stat spread for the infusion of your choice as well as the damage difference with your current stats.
""")

st.subheader("I would like to give some feedback.")

st.markdown("""
Whether it is for functionnality request, default values suggestions or anything else really, feel free to message **.smaxy.** on Discord.
If you have general questions on the technical apsects of this game head to the [ERPvP Discord](https://discord.gg/erpvp) where you will find lots of knowledgeable people.
""")
