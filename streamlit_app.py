import streamlit as st
import streamlit.components.v1 as components

st.title("Hebrew Date Picker")

# Load the HTML file
with open("hebrew_date_picker.html") as f:
    html_code = f.read()

# Render the HTML file
date = components.html(html_code, height=500, scrolling=True)

# Display the selected date
if date:
    st.write("Selected Hebrew Date:", date)
