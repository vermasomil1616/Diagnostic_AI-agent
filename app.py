import streamlit as st
from PIL import Image
from google import genai
from fpdf import FPDF
import datetime
import re

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Medical AI Analyst", layout="wide")

# --- CUSTOM CSS (Dark Mode Compatible) ---
st.markdown("""
    <style>
    .report-container {
        background-color: #1E1E1E;
        color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #444;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 Medical Image Analysis & Disease Detection")
st.markdown("---")

# --- SIDEBAR: CONFIGURATION ---
st.sidebar.header("1. Configuration")
api_key = st.sidebar.text_input("Enter Google API Key", type="password")

st.sidebar.header("2. Patient Details")
patient_name = st.sidebar.text_input("Patient Name", "John Doe")
patient_age = st.sidebar.number_input("Age", min_value=0, max_value=120, value=45)
patient_gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])

# --- DYNAMIC MODEL SELECTOR ---
available_models = []
if api_key:
    try:
        client = genai.Client(api_key=api_key)
        for m in client.models.list():
            if "generateContent" in m.supported_actions:
                available_models.append(m.name)
    except Exception as e:
        st.sidebar.error(f"Error fetching models: {e}")

if available_models:
    model_choice = st.sidebar.selectbox("3. Select Model", available_models, index=0)
else:
    model_choice = st.sidebar.text_input("3. Enter Model Name", "gemini-1.5-flash")

# --- PDF GENERATION LOGIC ---
def create_pdf(report_text, patient_name, patient_age, patient_gender, image_filename):
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 20)
            self.cell(0, 10, 'Universal Medical Center', 0, 1, 'C')
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, 'Radiology Department | AI Diagnostic Unit', 0, 1, 'C')
            self.line(10, 30, 200, 30)
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # 1. PATIENT INFO BLOCK
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "PATIENT DETAILS", 0, 1)
    pdf.set_font("Arial", size=10)
    
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    pdf.cell(40, 6, f"Name: {patient_name}", 0, 0)
    pdf.cell(40, 6, f"Age: {patient_age}", 0, 0)
    pdf.cell(40, 6, f"Gender: {patient_gender}", 0, 1)
    pdf.cell(40, 6, f"Date: {date_str}", 0, 0)
    pdf.cell(40, 6, f"Image: {image_filename}", 0, 1)
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)

    # 2. ANALYSIS REPORT BODY
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 8, "DIAGNOSTIC REPORT", 0, 1)
    pdf.ln(3)
    
    # Clean up the text first to ensure newlines exist
    # This fixes the "blob of text" issue
    clean_report = report_text.replace("* **", "\n* **").replace("- **", "\n- **")
    
    lines = clean_report.split('\n')
    for line in lines:
        line = line.encode('latin-1', 'replace').decode('latin-1')
        line = line.strip()
        
        if not line:
            continue
            
        # Headers
        if line.startswith('#'):
            clean_line = line.replace('#', '').strip()
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 12)
            pdf.set_text_color(0, 51, 102)
            pdf.cell(0, 8, clean_line, 0, 1)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", size=10)
            
        # Bullet Points (Fixed Alignment)
        elif line.startswith('*') or line.startswith('-'):
            clean_line = line.replace('*', '').replace('-', '').strip()
            clean_line = clean_line.replace('**', '') # Remove markdown bolding
            
            pdf.set_x(15) # Indent
            pdf.cell(5, 5, chr(149), 0, 0) # Bullet
            pdf.multi_cell(0, 5, clean_line)
            
        # Normal Text
        else:
            pdf.set_x(10)
            pdf.multi_cell(0, 5, line)

    pdf.ln(10)

    # 3. DISCLAIMER & SIGNATURE
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 8, "_" * 30, 0, 1, 'R')
    pdf.cell(0, 5, "Authorized Signature", 0, 1, 'R')
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 5, "AI Diagnostic Assistant", 0, 1, 'R')
    
    return pdf.output(dest='S').encode('latin-1')

# --- ANALYSIS FUNCTION ---
def analyze_image(image_file, model_name, key):
    try:
        client = genai.Client(api_key=key)
        img = Image.open(image_file)
        
        # STRICT PROMPT FOR NEWLINES
        prompt = """
        You are an expert Radiologist. Analyze the image.
        
        FORMATTING RULES:
        1. Use clear headings with '##'.
        2. Put every single bullet point on a NEW LINE.
        3. Do not combine multiple findings into one line.
        
        REQUIRED OUTPUT FORMAT:
        
        ## 1. Scan Type & Region
        - **Modality:** [Modality Name]
        - **Region:** [Region Name]
        - **View:** [View Name]
        
        ## 2. Key Findings
        - **Finding 1:** [Detail]
        - **Finding 2:** [Detail]
        
        ## 3. Diagnosis
        - **Primary:** [Diagnosis]
        - **Confidence:** [Level]
        
        ## 4. Recommendations
        - [Recommendation 1]
        """
        
        response = client.models.generate_content(
            model=model_name,
            contents=[img, prompt]
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"

# --- MAIN UI ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Image")
    uploaded_file = st.file_uploader("Upload Medical Scan", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

with col2:
    st.subheader("📋 Analysis Report")
    
    if uploaded_file and api_key:
        if st.button("Analyze Image", type="primary"):
            with st.spinner("Analyzing..."):
                result = analyze_image(uploaded_file, model_choice, api_key)
                st.session_state.analysis_result = result
        
        if "analysis_result" in st.session_state and st.session_state.analysis_result:
            # Display text on web
            st.markdown(f'<div class="report-container">{st.session_state.analysis_result}</div>', unsafe_allow_html=True)
            
            # Generate PDF
            pdf_data = create_pdf(
                st.session_state.analysis_result, 
                patient_name, patient_age, patient_gender, 
                uploaded_file.name
            )
            
            st.download_button(
                label="📄 Download Official PDF Report",
                data=pdf_data,
                file_name=f"Medical_Report_{patient_name}.pdf",
                mime="application/pdf"
            )