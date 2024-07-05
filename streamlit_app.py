import streamlit as st
from hdate import HebrewDate

# Define Hebrew months with their characteristics
hebrew_months = [
    {"name": "Nisan", "hebrew_name": "נִיסָן", "days": 30, "time_of_year": "March–April", "notes": "Month of Passover"},
    {"name": "Iyar", "hebrew_name": "אִייָר", "days": 29, "time_of_year": "April–May", "notes": "Pre-exile name Ziv ('light')"},
    {"name": "Sivan", "hebrew_name": "סִיוָן", "days": 30, "time_of_year": "May–June", "notes": "Month of Shavuot"},
    {"name": "Tammuz", "hebrew_name": "תַּמּוּז", "days": 29, "time_of_year": "June–July"},
    {"name": "Ab", "hebrew_name": "אָב", "days": 30, "time_of_year": "July–August", "notes": "Month of Tisha B'Av"},
    {"name": "Elul", "hebrew_name": "אֱלוּל", "days": 29, "time_of_year": "August–September"},
    {"name": "Tishrei", "hebrew_name": "תִּשְׁרֵי", "days": 30, "time_of_year": "September–October", "notes": "Month of Rosh Hashanah, Yom Kippur and Sukkot"},
    {"name": "Heshvan", "hebrew_name": "מַרְחֶשְׁוָן", "days": 29, "time_of_year": "October–November", "notes": "Pre-exile name Bul"},
    {"name": "Kislev", "hebrew_name": "כִּסְלֵו", "days": 30, "time_of_year": "November–December", "notes": "Month of Hanukkah"},
    {"name": "Tevet", "hebrew_name": "טֵבֵת", "days": 29, "time_of_year": "December–January"},
    {"name": "Shevat", "hebrew_name": "שְׁבָט", "days": 30, "time_of_year": "January–February"},
    {"name": "Adar", "hebrew_name": "אֲדָר", "days": 29, "time_of_year": "February–March", "notes": "Month of Purim"}
]

def hebrew_date_picker(label):
    selected_month = st.selectbox(f"Select {label} Month", [month["hebrew_name"] for month in hebrew_months])
    selected_month_index = next((i for i, month in enumerate(hebrew_months) if month["hebrew_name"] == selected_month), None)
    
    selected_day = st.selectbox(f"Select {label} Day", list(range(1, hebrew_months[selected_month_index]["days"] + 1)))

    st.write(f"Selected {label} Date (Hebrew): {selected_day} {selected_month}")
    st.write(f"Time of Year: {hebrew_months[selected_month_index]['time_of_year']}")
    if 'notes' in hebrew_months[selected_month_index]:
        st.write(f"Notes: {hebrew_months[selected_month_index]['notes']}")

# Streamlit app
st.title("Hebrew Date Picker")

st.write("Select a Hebrew date:")
hebrew_date_picker("Start")
