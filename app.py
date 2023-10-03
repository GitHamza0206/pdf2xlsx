import streamlit as st
import pandas as pd
from tabula import read_pdf
import base64

def get_table_download_link(df, file_format):
    if file_format == 'CSV':
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="extracted_data.csv">Download Data as CSV</a>'
    elif file_format == 'Excel':
        excel = df.to_excel(index=False)
        b64 = base64.b64encode(excel.encode()).decode()
        href = f'<a href="data:file/excel;base64,{b64}" download="extracted_data.xlsx">Download Data as Excel</a>'
    return href

# Title of the Web App
st.title('PDF Table Extractor')

# Upload the PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Extract the table from the PDF file
    try:
        extracted_table = read_pdf(uploaded_file, pages='all', multiple_tables=False)
        df = extracted_table[0] # Get the first table
        st.dataframe(df) # Display the table
        
        # Choose file format to download
        file_format = st.selectbox('Select file format to download:', ('CSV', 'Excel'))
        
        # Download link for the extracted data
        st.markdown(get_table_download_link(df, file_format), unsafe_allow_html=True)
    except Exception as e:
        st.write("Error:", str(e))
