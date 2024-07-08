import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import requests
import os
from io import BytesIO
from PIL import Image
import re

st.title("Mishnayos for Yahrtzeit")

# Full Hebrew Name input with placeholder
full_hebrew_name = st.text_input("Full Hebrew Name", placeholder="e.g. מנחם מענדל")

def is_hebrew(text):
    # Check if the text contains Hebrew characters
    return bool(re.search(r'[\u0590-\u05FF]', text))

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

def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return BytesIO(response.content)
    except requests.RequestException as e:
        st.error(f"Failed to download image: {e}")
        return None

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

            # Download and draw the swirl border image
            image_url = "https://github.com/sheetsgeogle/Gemara/raw/main/test2.png"
            image_file = download_image(image_url)
            if image_file:
                image = Image.open(image_file).convert("RGBA")
                # Save the image temporarily to calculate size
                temp_image_path = "temp_swirl_border.png"
                image.save(temp_image_path)

                # Get the size of the image
                img_width, img_height = image.size

                # Determine scale to fit the image in the desired area while preserving aspect ratio
                max_width = 0.07 * width  # Increased size
                max_height = 0.02 * height  # Increased size
                aspect_ratio = img_width / img_height

                if img_width > max_width or img_height > max_height:
                    if max_width / aspect_ratio <= max_height:
                        img_width = max_width
                        img_height = max_width / aspect_ratio
                    else:
                        img_height = max_height
                        img_width = max_height * aspect_ratio
                else:
                    img_width = img_width
                    img_height = img_height

                # Draw the image on the PDF
                c.drawImage(temp_image_path, width / 2 - img_width / 2, height - 0.3 * height, width=img_width, height=img_height, mask='auto')

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

# Validate and generate PDF
if full_hebrew_name:
    if is_hebrew(full_hebrew_name):
        pdf_file = create_pdf(full_hebrew_name)
        if pdf_file:
            st.download_button(
                label="Download PDF",
                data=pdf_file,
                file_name="Hebrew_Name.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Error generating the PDF.")
    else:
        st.error("Please enter a name in Hebrew.")
