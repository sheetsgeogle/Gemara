import streamlit as st
from hdate import HebrewDate

def hebrew_date_picker(label):
    selected_date = st.date_input(f"Select {label} Date (Gregorian)")

    # Convert Gregorian date to Hebrew date
    hebrew_date = HebrewDate.from_pydate(selected_date)
    hebrew_day = hebrew_date.day
    hebrew_month = hebrew_date.month_name()
    hebrew_year = hebrew_date.year

    st.write(f"Selected {label} Date (Gregorian): {selected_date}")
    st.write(f"Selected {label} Date (Hebrew): {hebrew_day} {hebrew_month} {hebrew_year} AM")

# Streamlit app
st.title("Hebrew Date Picker")

st.write("Select a Gregorian date:")
hebrew_date_picker("Start")
