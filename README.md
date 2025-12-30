# 🩺 Medical Image Analysis & Diagnostic Assistant

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![Gemini AI](https://img.shields.io/badge/AI-Google%20Gemini%201.5-orange)

An AI-powered medical imaging tool that utilizes Google's **Gemini 1.5 Flash** model to analyze medical scans (X-Rays, MRIs, CT Scans) and generate professional diagnostic reports. Designed for ease of use with a Streamlit interface and automated PDF report generation.

## 🚀 Features

* **Multi-Modality Analysis:** Supports X-Rays, MRIs, CT Scans, and Ultrasounds.
* **AI-Powered Diagnostics:** Uses Gemini 1.5 Flash for zero-shot medical image interpretation.
* **Structured Reporting:** Automatically identifies Scan Type, Key Findings, Diagnosis, and Recommendations.
* **Professional PDF Export:** Generates a downloadable PDF report with patient demographics and a digital doctor's signature.
* **Dynamic Model Selector:** Automatically detects available Google AI models for your API key.
* **Dark Mode UI:** Optimized interface for radiologists working in low-light environments.



## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/medical-ai-assistant.git](https://github.com/your-username/medical-ai-assistant.git)
    cd medical-ai-assistant
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up credentials:**
    * Get your free Google API Key from [Google AI Studio](https://aistudio.google.com/app/apikey).
    * (Optional) You can enter this key directly in the app sidebar.

## 🏃‍♂️ Usage

Run the application using Streamlit:

```bash
streamlit run app.py
