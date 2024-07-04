import os
import requests
from PyPDF2 import PdfMerger
import streamlit as st
from io import BytesIO

# Define the URL pattern
url_pattern = "https://daf-yomi.com/Data/UploadedFiles/DY_Page/{}.pdf"

def download_and_merge_pdfs(start, end):
    # Initialize a PdfMerger object
    merger = PdfMerger()
    buffer = BytesIO()

    # Loop through the range and download each PDF
    for i in range(start, end + 1):
        url = url_pattern.format(i)
        response = requests.get(url)
        if response.status_code == 200:
            pdf_filename = f"page_{i}.pdf"
            with open(pdf_filename, 'wb') as pdf_file:
                pdf_file.write(response.content)
            merger.append(pdf_filename)
        else:
            st.warning(f"Failed to download {url}")

    # Write out the merged PDF to the buffer
    merger.write(buffer)
    merger.close()
    buffer.seek(0)
    
    # Cleanup downloaded files
    for i in range(start, end + 1):
        os.remove(f"page_{i}.pdf")

    return buffer

st.title("PDF Merger")

start = st.number_input("Start Page Number", min_value=1, value=49)
end = st.number_input("End Page Number", min_value=1, value=58)

if st.button("Download and Merge PDFs"):
    if start > end:
        st.error("Start page number must be less than or equal to end page number.")
    else:
        pdf_buffer = download_and_merge_pdfs(start, end)
        st.success("PDFs have been merged successfully!")
        st.download_button(
            label="Download Merged PDF",
            data=pdf_buffer,
            file_name="merged_document.pdf",
            mime="application/pdf"
        )
