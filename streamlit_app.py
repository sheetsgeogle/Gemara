import streamlit as st
import streamlit.components.v1 as components

st.title("Hebrew Date Picker")

# Render the HTML file
components.iframe(src="hebrew_date_picker.html", height=500)

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
