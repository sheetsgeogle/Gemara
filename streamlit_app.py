import streamlit as st
import datetime
from hdate import HDate, HDateFormatter

# Convert Gregorian date to Hebrew date
def gregorian_to_hebrew(date):
    hebrew_date = HDate(date)
    formatter = HDateFormatter(hebrew_date)
    return formatter.format('l, j b Y')

# Streamlit app
st.title("Hebrew Date Picker")

# Date input
gregorian_date = st.date_input("Pick a date", datetime.date.today())

# Convert to Hebrew date
hebrew_date = gregorian_to_hebrew(gregorian_date)

# Display Hebrew date
st.write("Hebrew Date:", hebrew_date)
