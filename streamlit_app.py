import streamlit as st
from hdate import HDate
from datetime import date, datetime

st.title("Hebrew Date Picker")

# Create a Gregorian date picker
selected_date = st.date_input("Select a date", date.today())

# Convert the selected Gregorian date to Hebrew date
hebrew_date = HDate(selected_date)

st.write("Selected Gregorian Date:", selected_date)
st.write("Converted Hebrew Date:", hebrew_date.hebrew_date_long())

# Allow user to input a Hebrew date
hebrew_year = st.number_input("Hebrew Year", min_value=5000, max_value=6000, value=hebrew_date.hebrew_year())
hebrew_month = st.selectbox("Hebrew Month", list(HDate.HEBREW_MONTHS.keys()))
hebrew_day = st.number_input("Hebrew Day", min_value=1, max_value=30, value=hebrew_date.hebrew_day())

if st.button("Convert to Gregorian Date"):
    # Convert the input Hebrew date to Gregorian date
    try:
        input_hebrew_date = HDate(hebrew_day, HDate.HEBREW_MONTHS[hebrew_month], hebrew_year)
        gregorian_date = input_hebrew_date.gregorian_date
        st.write("Converted Gregorian Date:", gregorian_date)
    except Exception as e:
        st.write("Error in conversion:", e)

# Allow user to input a Hebrew date in text format
hebrew_date_text = st.text_input("Enter Hebrew date (e.g., כ\' בטבת תשפ\"ד)")
if st.button("Convert Text to Gregorian Date"):
    try:
        input_hebrew_date_text = HDate.from_hebrew_string(hebrew_date_text)
        gregorian_date_text = input_hebrew_date_text.gregorian_date
        st.write("Converted Gregorian Date:", gregorian_date_text)
    except Exception as e:
        st.write("Error in conversion:", e)
