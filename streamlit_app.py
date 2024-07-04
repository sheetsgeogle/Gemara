import streamlit as st
import os
import requests
from PyPDF2 import PdfMerger

# Streamlit app title
st.title("PDF Merger")

# Input fields for start and end numbers
start = st.number_input("Start Number", min_value=1, value=1414)
end = st.number_input("End Number", min_value=1, value=1474)

# Button to trigger the merging process
if st.button("Merge PDFs"):
    # Define the URL pattern
    url_pattern = "https://daf-yomi.com/Data/UploadedFiles/DY_Page/{:04d}.pdf"
    
    # Initialize a PdfMerger object
    merger = PdfMerger()
    
    # Get the path to the Downloads directory
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    
    # Create a directory to save individual PDFs temporarily
    temp_dir = os.path.join(downloads_path, "temp_pdfs")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Loop through the range and download each PDF
    for i in range(start, end + 1):
        url = url_pattern.format(i)
        response = requests.get(url)
        if response.status_code == 200:
            pdf_filename = os.path.join(temp_dir, f"page_{i}.pdf")
            with open(pdf_filename, 'wb') as pdf_file:
                pdf_file.write(response.content)
            merger.append(pdf_filename)
            st.write(f"Downloaded and added page {i}")
        else:
            st.write(f"Failed to download {url}")
    
    # Write out the merged PDF to the Downloads folder
    output_filename = os.path.join(downloads_path, "merged_document.pdf")
    merger.write(output_filename)
    merger.close()
    
    # Clean up temporary files
    for temp_pdf in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, temp_pdf))
    os.rmdir(temp_dir)
    
    st.success(f"Merged document saved as {output_filename}")
