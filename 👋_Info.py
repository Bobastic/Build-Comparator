import streamlit as st

st.set_page_config(layout='centered',page_title="Build Comparator",page_icon="⚖️")

st.sidebar.info("Hi. Check this page for some information about this tool or head straight to **Build Comparator** to figure it out by yourself.")

st.header("Hi. This is my Build Comparator.")

st.text("")

st.subheader("What is the purpose of this tool?")

st.markdown(f"""<div style='text-align: justify;'>
There are already lots of tools for build optimization, mainly in the form of spreadsheets or slugbot.
However, I could not find a way to compare whole builds together.
Usually you get tools for optimal infusion, optimal stats but always for one weapon or weapon class.
There isn't to my knowledge a way to see the damage values of a <strong>whole inventory</strong> across <strong>multiple builds</strong>. So I made one.  
</div>""",unsafe_allow_html=True)

st.text("")

st.subheader("Use case examples")

st.markdown("""
- How much more damage do I get with 69 STR compared to 54 STR on all these weapons?
- Is Cold->Lightning better than Cold->Magic for this inventory?
- Fire + Flaming Strike buff or Heavy + Lightning Grease?
- How broken is Sacred Blade?
- What is the best build for BKH and Dismounter between these three?
""")

st.text("")

st.subheader("So what does it actually do?")

st.markdown(f"""<div style='text-align: justify;'>
You input a list of <strong>weapons</strong> of your choice and as many <strong>builds</strong> and <strong>infusions</strong> as you like and you get a table with estimated damage that is widely customizable.
You can display counter damage, comparisons with the best infusion etc...
You can also export raw data as a CSV file or download the table as a HTML file.
</div>""",unsafe_allow_html=True)

st.text("")

st.subheader("Ok, how do I use it?")

st.markdown(f"""<div style='text-align: justify;'>
Input your weapons, builds, infusions and enemy stats in <strong>🛠️ Parameters</strong>.
Then go to <strong>🔬 Build Comparator</strong> to show the table and change what information you want to display.
There are already some default weapons and builds so you can go straight to <strong>🔬 Build Comparator</strong> to see what the table looks like.
</div>""",unsafe_allow_html=True)

st.text("")

st.subheader("I would like to give some feedback.")

st.markdown(f"""<div style='text-align: justify;'>
Whether it is for functionnality request, default values suggestions or anything else really, feel free to message  <strong>.smaxy.</strong> on Discord.
</div>""",unsafe_allow_html=True)
