import streamlit as st
import datetime

# Hebrew months
months = ["ניסן", "אייר", "סיון", "תמוז", "אב", "אלול", 
          "תשרי", "חשון", "כסלו", "טבת", "שבט", "אדר"]

# Hebrew days
days = ["א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט", 
        "י", "יא", "יב", "יג", "יד", "טו", "טז", 
        "יז", "יח", "יט", "כ", "כא", "כב", "כג", 
        "כד", "כה", "כו", "כז", "כח", "כט", "ל"]

st.title("Select Hebrew Date")

# Buttons for English and Hebrew date
col1, col2 = st.columns(2)

with col1:
    if st.button('English Date'):
        english_date = st.date_input('Select English Date', datetime.date.today())
        st.write(f'Selected English Date: {english_date}')

with col2:
    st.button('Hebrew Date')

# Dropdowns for Hebrew month and day
col3, col4 = st.columns(2)

with col3:
    month = st.selectbox('Month', months)

with col4:
    day = st.selectbox('Day', days)

st.write(f'Selected Hebrew Date: {day} {month}')
