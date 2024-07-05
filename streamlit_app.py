import streamlit as st
from pyhebcal import *
from pyhebcal.dates import HDate

def hebrew_date_picker(label, min_date=None, max_date=None):
    min_date = HDate(min_date) if min_date else None
    max_date = HDate(max_date) if max_date else None

    # Generate a list of Hebrew months and days
    hebrew_months = list(range(1, 13))
    hebrew_days = list(range(1, 31))  # Hebrew calendar can have up to 30 days in a month

    selected_month = st.selectbox(f"Select {label} Month", hebrew_months)
    selected_day = st.selectbox(f"Select {label} Day", hebrew_days)

    # Convert selected Hebrew date to Gregorian for display purposes
    selected_hebrew_date = HDate(selected_day, selected_month)
    selected_gregorian_date = selected_hebrew_date.to_pydate()

    st.write(f"Selected {label} Date (Hebrew): {selected_hebrew_date}")
    st.write(f"Selected {label} Date (Gregorian): {selected_gregorian_date}")

# Streamlit app
st.title("Hebrew Date Picker")

st.write("Select a Hebrew date:")
hebrew_date_picker("Start")
