import os
import requests
from PyPDF2 import PdfMerger
import streamlit as st

# Define the URL pattern
url_pattern = "https://daf-yomi.com/Data/UploadedFiles/DY_Page/{}.pdf"

def download_and_merge_pdfs(start, end):
    # Initialize a PdfMerger object
    merger = PdfMerger()

    # Get the path to the Downloads directory
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

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

    # Write out the merged PDF to the Downloads folder
    output_filename = os.path.join(downloads_path, "merged_document.pdf")
    merger.write(output_filename)
    merger.close()

    return output_filename

st.title("PDF Merger")

start = st.number_input("Start Page Number", min_value=1, value=49)
end = st.number_input("End Page Number", min_value=1, value=58)

if st.button("Download and Merge PDFs"):
    if start > end:
        st.error("Start page number must be less than or equal to end page number.")
    else:
        output_filename = download_and_merge_pdfs(start, end)
        st.success(f"Merged document saved as {output_filename}")
