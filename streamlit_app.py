import streamlit as st
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript

st.title("Hebrew Date Picker")

# URL to the raw HTML file on GitHub
html_url = "https://raw.githubusercontent.com/sheetsgeogle/Gemara/main/hebrew_date_picker.html"

# Render the HTML file from GitHub
components.iframe(html_url, height=500)

# JavaScript to receive the selected date
selected_date = st_javascript("""
    return new Promise((resolve) => {
        window.addEventListener("message", (event) => {
            resolve(event.data);
        });
    });
""")

# Display the selected date
if selected_date:
    st.write("Selected Hebrew Date:", selected_date)
