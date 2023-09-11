import streamlit as st

st.set_page_config(layout='centered',page_title="Build Comparator",page_icon="⚖️")

st.sidebar.info("Hi. Check this page for some information about this tool or head straight to **🔬 Build Comparator** or **⚖️ Weapon Optimizer** to figure it out by yourself.")

st.subheader("What is the purpose of this tool?")

st.markdown(f"""<div style='text-align: justify;'>
There are already lots of tools for build optimization, mainly in the form of spreadsheets or slugbot.
However, I could not find a way to compare whole builds together.
Usually you get tools for optimal infusion, optimal stats but always for one weapon or weapon class.
There isn't to my knowledge a way to see the damage values of a <strong>whole inventory</strong> across <strong>multiple builds</strong>. So I made one.
I also added other functionalities like an infusion optimizer or a stat allocator.
</div>""",unsafe_allow_html=True)

st.text("")

st.subheader("Use case examples")

st.markdown("""
- How much more damage do I get with 69 STR compared to 54 STR on all these weapons?
- Is Cold->Lightning better than Cold->Magic for this inventory?
- Fire + Flaming Strike buff or Heavy + Lightning Grease?
- How broken is Sacred Blade?
- What is the best build for BKH and Dismounter between these three?
- Best infusion and stat spread for Shamshir?
""")

st.text("")

st.subheader("**🔬 Build Comparator**")

st.markdown(f"""<div style='text-align: justify;'>
Input a list of <strong>weapons</strong> of your choice and as many <strong>builds</strong> and <strong>infusions</strong> as you like and you get a table with estimated damage that is widely customizable.
You can display counter damage, comparisons with the best infusion etc...
You can also export raw data as a CSV file or download the table as a HTML file.
There are already some default weapons and builds so you can go straight to any page to see what this tool can do.
</div>""",unsafe_allow_html=True)

st.text("")

st.subheader("**⚖️ Weapon Optimizer**")

st.markdown(f"""<div style='text-align: justify;'>
Pick a weapon and you'll have estimated damage for each infusion with the specified stat spread.
On the right you will find the optimal stat spread for the infusion of your choice as well as the damage difference with your current stat spread.
</div>""",unsafe_allow_html=True)

st.text("")

st.subheader("I would like to give some feedback.")

st.markdown(f"""<div style='text-align: justify;'>
Whether it is for functionnality request, default values suggestions or anything else really, feel free to message  <strong>.smaxy.</strong> on Discord.
If you have general questions on the technical apsects of this game head to the ERPvP Discord where you will find lots of knowledgeable people.
</div>""",unsafe_allow_html=True)
