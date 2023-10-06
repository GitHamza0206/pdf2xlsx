import streamlit as st
import pandas as pd
import io 
import base64
import camelot 


def get_table_download_link(df, file_format, filename):
    filename = filename.split('.')[0]
    if file_format == 'CSV':
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="'+filename+'.csv">Download Data as CSV</a>'
    elif file_format == 'Excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)
        excel_data = output.getvalue()
        b64 = base64.b64encode(excel_data).decode() 
        #href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}" target="_blank">{text}</a>'
        href = f'<a href="data:file/excel;base64,{b64}" download="'+filename+'.xlsx">Download Data as Excel</a>'
    return href

def display_pdf(pdf_file):
    with open(pdf_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)


def extract_tables(pdf_file):
    all_tables = []
    with pdfplumber.open(pdf_file) as f:
        # Loop through all the pages
        for page in f.pages:
            # Extract tables from the page
            tables = page.extract_tables()
            
            # Loop through all the tables
            for table in tables:
                # Convert the table data into a DataFrame
                df = pd.DataFrame(table)
                
                # Append the data to the all_tables DataFrame
                all_tables.append(df)
    return all_tables 

def concatenated_data(tables):
    return pd.concat(tables, ignore_index=True)

def extract_table_camelot(pdf_file):
    return camelot.read_pdf(pdf_file,pages="all",flavor='stream')


# Title of the Web App
st.title('PDF Table Extractor')

# Upload the PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Extract the table from the PDF file
    try:
        # Save the uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Display the PDF
        display_pdf("temp.pdf")

        extracted_table = extract_table_camelot('temp.pdf')

        dfs= []
        for i,df in enumerate(extracted_table):
            df = extracted_table[i].df # Get the first table
            dfs.append(df)
            #st.write(f'page {i}')
            #st.dataframe(df,use_container_width=True) # Display the table


        st.markdown("""
        <div style="text-align: center; color: blue; font-size: 24px; font-weight: bold;">
            Excel result
        </div>
        """, unsafe_allow_html=True)

        concatenated_tables = concatenated_data(dfs)
        st.dataframe(concatenated_tables,use_container_width=True)

        # Choose file format to download
        file_format = st.selectbox('Select file format to download:', ('CSV', 'Excel'))
        
        # Download link for the extracted data
        st.markdown(get_table_download_link(concatenated_tables, file_format, uploaded_file.name), unsafe_allow_html=True)
    except Exception as e:
        st.write("Error:", str(e))
