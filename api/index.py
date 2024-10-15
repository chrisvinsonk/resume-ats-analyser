from flask import Flask, request, jsonify
import google.generativeai as genai
import PyPDF2 as pdf
import json
import os

app = Flask(__name__)

# Configure the Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(file):
    reader = pdf.PdfReader(file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

input_prompt = """
Hey Act Like a skilled or very experience ATS(Application Tracking System) with a deep understanding of tech field,software engineering,data science ,data analyst and big data engineer. Your task is to evaluate the resume based on the given job description. You must consider the job market is very competitive and you should provide best assistance for improving thr resumes. Assign the percentage Matching based on Jd and the missing keywords with high accuracy resume:{text} description:{jd}

I want the response in one single string having the structure {{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['resume']
    jd = request.form['jd']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file:
        try:
            resume_text = input_pdf_text(file)
            final_prompt = input_prompt.format(text=resume_text, jd=jd)
            response = get_gemini_response(final_prompt)
            
            response_dict = json.loads(response)
            
            return jsonify(response_dict)
        except Exception as e:
            return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)