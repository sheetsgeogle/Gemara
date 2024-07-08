import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import requests
import os
from io import BytesIO

st.title("Generate and Download PDF with Hebrew Name")

# Full Hebrew Name input with placeholder
full_hebrew_name = st.text_input("Full Hebrew Name", placeholder="מנחם מענדל")

def download_font(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)

        # Save the font file
        with open(filename, "wb") as f:
            f.write(response.content)
    except requests.RequestException as e:
        st.error(f"Failed to download font: {e}")

def reverse_hebrew(text):
    return text[::-1]

def create_pdf(name):
    pdf_file = BytesIO()  # Use BytesIO to create an in-memory PDF
    font_path = "SBL_Hbrw (1).ttf"  # Use a relative path or an appropriate location
    try:
        if os.path.exists(font_path):
            c = canvas.Canvas(pdf_file, pagesize=letter)
            width, height = letter

            # Register the SBL Hebrew font
            pdfmetrics.registerFont(TTFont('SBL_Hebrew', font_path))

            # Draw the black text
            c.setFont("SBL_Hebrew", 41)
            black_text = "םשה תויתוא לש תינשמה יקרפ"
            c.drawCentredString(width / 2, height - 100, black_text)

            # Draw the gold text adjusted upwards
            reversed_name = reverse_hebrew(name)
            c.setFont("SBL_Hebrew", 86)
            c.setFillColor(HexColor("#be9a63"))
            c.drawCentredString(width / 2, height - 180, reversed_name)  # Adjusted y-coordinate

            # Save the PDF
            c.save()
            pdf_file.seek(0)  # Rewind the BytesIO object to the beginning
            return pdf_file
        else:
            st.error(f"Font file not found at {font_path}.")
            return None
    except Exception as e:
        st.error(f"An error occurred while creating the PDF: {e}")
        return None

# URL of the SBL Hebrew font on GitHub
font_url = "https://github.com/sheetsgeogle/Gemara/raw/main/SBL_Hbrw%20(1).ttf"
font_path = "SBL_Hbrw (1).ttf"  # Use a relative path or an appropriate location
download_font(font_url, font_path)

# Generate and download PDF with a single button
if full_hebrew_name:
    pdf_file = create_pdf(full_hebrew_name)
    if pdf_file:
        st.download_button(
            label="Generate and Download PDF",
            data=pdf_file,
            file_name="Hebrew_Name.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Error generating the PDF.")
