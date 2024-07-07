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

st.title("Generate PDF with Hebrew Name")

# Full Hebrew Name input with placeholder
full_hebrew_name = st.text_input("Full Hebrew Name", placeholder="מנחם מענדל")

if full_hebrew_name:
    def download_font(url, filename):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Save the font file
            with open(filename, "wb") as f:
                f.write(response.content)
            st.info(f"Font downloaded and saved to {filename}.")
        except requests.RequestException as e:
            st.error(f"Failed to download font: {e}")

    def download_image(url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            image = Image.open(BytesIO(response.content))
            return image
        except requests.RequestException as e:
            st.error(f"Failed to download image: {e}")
        except IOError as e:
            st.error(f"Failed to open image file: {e}")
        return None

    def reverse_hebrew(text):
        return text[::-1]

    def create_pdf(name):
        pdf_file = "Hebrew_Name.pdf"  # Use a relative path or an appropriate location
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
                image = download_image(image_url)
                if image:
                    image_path = "swirl_border.png"
                    image.save(image_path)
                    # Resize and position the image
                    c.drawImage(image_path, width / 2 - 10, height - 230, width=20, height=10)  # Slightly larger size and adjusted position

                c.save()
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

    # Check if the font file exists after download
    if os.path.exists(font_path):
        pdf_file = create_pdf(full_hebrew_name)
        if pdf_file:
            st.write(f"Generated PDF for: {full_hebrew_name}")
            with open(pdf_file, "rb") as f:
                st.download_button(label="Download PDF", file_name="Hebrew_Name.pdf", data=f, mime="application/pdf")
    else:
        st.error(f"Font file not found after download attempt: {font_path}.")
else:
    st.write("Please enter a Hebrew name to generate the PDF.")
