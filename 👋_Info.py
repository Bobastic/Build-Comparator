import streamlit as st

st.set_page_config(layout='centered',page_title="Build Comparator",page_icon="⚖️")

def justify(text):
  return st.markdown(f"<div style='text-align: justify;'>{text}</div>",unsafe_allow_html=True)

st.sidebar.info("Hi. Check this page for some information about this tool or head straight to **Build Comparator** to figure it out by yourself.")

st.header("Hi. This is my Build Comparator.")

st.subheader("What is the purpose of this tool?")

justify("""
There are already lots of tools for build optimization, mainly in the form of spreadsheets or slugbot.
However, I could not find a way to compare whole builds together.
Usually you get tools for optimal infusion, optimal stats but always for one weapon or weapon class.
There isn't to my knowledge a way to see the damage values of a **whole inventory** across **multiple builds**. So I made one.  
""")

st.subheader("Use case examples")

justify("""
- How much more damage do I get with 69 STR compared to 54 STR on all these weapons?
- Is Cold->Keen better than Cold->Magic for this inventory?
- Fire + Flaming Strike buff or Heavy + Lightning Grease?
- How broken is Sacred Blade?
- What is the best build for BKH and Cleanrot between these three?
""")

st.subheader("So what does it actually do?")

justify("""
You input a list of **weapons** of your choice and as many **builds** and **infusions** as you like and you get a table with estimated damage that is widely customizable.
You can display counter damage, comparisons with the best infusion etc...
You can also export raw data as a CSV file or download the table as a PNG image (WIP) to get a cleaner result than screenshots.
""")

st.subheader("Ok, how do I use it?")

justify("""
Input your weapons, builds, infusions and enemy stats in **🛠️ Parameters**.
Then go to **🔬 Build Comparator** to show the table and change what information you want to display.
There are already some default weapons and builds so you can go straight to **🔬 Build Comparator** to see what the table looks like.
""")

st.subheader("I would like to give some feedback.")

justify("""
Whether it is for functionnality request, default values suggestions or anything else really, feel free to message  **.smaxy.** on Discord.
""")
