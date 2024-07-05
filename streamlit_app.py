import streamlit as st

# Hebrew months
months = ["ניסן", "אייר", "סיון", "תמוז", "אב", "אלול", 
          "תשרי", "חשון", "כסלו", "טבת", "שבט", "אדר"]

# Hebrew days
days = ["א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט", 
        "י", "יא", "יב", "יג", "יד", "טו", "טז", 
        "יז", "יח", "יט", "כ", "כא", "כב", "כג", 
        "כד", "כה", "כו", "כז", "כח", "כט", "ל"]

st.title("Select Hebrew Date")

col1, col2 = st.columns(2)

with col1:
    month = st.selectbox('Month', months)

with col2:
    day = st.selectbox('Day', days)

st.write(f'Selected Date: {day} {month}')
