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

st.title("Select Date")

# Options for Hebrew and English
option = st.radio("Select Date Type", ('Hebrew', 'English'))

if option == 'Hebrew':
    col1, col2 = st.columns(2)

    with col1:
        month = st.selectbox('Month', months)

    with col2:
        day = st.selectbox('Day', days)

    st.write(f'Selected Hebrew Date: {day} {month}')

elif option == 'English':
    english_date = st.date_input('Select English Date', datetime.date.today())
    st.write(f'Selected English Date: {english_date}')
