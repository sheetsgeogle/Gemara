import streamlit as st
import datetime
import convertdate.hebrew as hebrew
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import requests
import os

# Hebrew months
months = ["ניסן", "אייר", "סיון", "תמוז", "אב", "אלול", 
          "תשרי", "חשון", "כסלו", "טבת", "שבט", "אדר"]

# Hebrew days
days = ["א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט", 
        "י", "יא", "יב", "יג", "יד", "טו", "טז", 
        "יז", "יח", "יט", "כ", "כא", "כב", "כג", 
        "כד", "כה", "כו", "כז", "כח", "כט", "ל"]

st.title("Select Date")

# Full Hebrew Name input with placeholder
full_hebrew_name = st.text_input("Full Hebrew Name", placeholder="מנחם מענדל")

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

    # Convert to Hebrew date
    hebrew_date = hebrew.from_gregorian(english_date.year, english_date.month, english_date.day)
    hebrew_day = days[hebrew_date[2] - 1]
    hebrew_month = months[hebrew_date[1] - 1]

    st.write(f'Selected Hebrew Date: {hebrew_day} {hebrew_month}')

if full_hebrew_name:
    def download_font(url, filename):
        if not os.path.exists(filename):
            response = requests.get(url)
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
            else:
                st.error("Failed to download font. Please check the URL or your internet connection.")
        else:
            st.info("Font already downloaded.")

    def create_pdf(name):
        pdf_file = "/mnt/data/Hebrew_Name.pdf"
        c = canvas.Canvas(pdf_file, pagesize=letter)
        width, height = letter

        # Register the SBL Hebrew font
        font_path = "/mnt/data/SBL_Hbrw.ttf"
        pdfmetrics.registerFont(TTFont('SBL_Hebrew', font_path))

        # Draw the black text
        c.setFont("SBL_Hebrew", 41)
        c.drawString(100, height - 100, "פרקי המשנית של אותיות השם")

        # Draw the gold text
        c.setFont("SBL_Hebrew", 86)
        c.setFillColor(HexColor("#be9a63"))
        c.drawString(100, height - 200, name)

        c.save()
        return pdf_file

    # URL of the SBL Hebrew font on GitHub
    font_url = "https://github.com/sheetsgeogle/Gemara/raw/main/SBL_Hbrw%20(1).ttf"
    font_path = "/mnt/data/SBL_Hbrw.ttf"
    download_font(font_url, font_path)

    try:
        pdf_file = create_pdf(full_hebrew_name)
        st.write(f"Generated PDF for: {full_hebrew_name}")
        with open(pdf_file, "rb") as f:
            st.download_button(label="Download PDF", file_name="Hebrew_Name.pdf", data=f, mime="application/pdf")
    except Exception as e:
        st.error(f"An error occurred while generating the PDF: {e}")
