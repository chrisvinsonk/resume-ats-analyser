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


# from flask import Flask, request, jsonify
# import google.generativeai as genai
# import PyPDF2 as pdf
# import json
# import os
# import requests
# from bs4 import BeautifulSoup

# app = Flask(__name__)

# # Configure the Gemini API
# genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# def get_gemini_response(input):
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content(input)
#     return response.text

# def input_pdf_text(file):
#     reader = pdf.PdfReader(file)
#     text = ""
#     for page in range(len(reader.pages)):
#         text += reader.pages[page].extract_text()
#     return text

# def extract_job_description(url):
#     try:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # Extract all text from the page
#         page_text = soup.get_text()

#         # Create a prompt for Gemini to extract job information
#         extraction_prompt = f"""
#         Extract the following information from the job posting text below:
#         1. Job Role
#         2. Required Experience
#         3. Required Skills
#         4. Job Description

#         Please format the output as a JSON string with keys: "role", "experience", "skills", and "description".

#         Job Posting Text:
#         {page_text}
#         """

#         # Get Gemini's response
#         extracted_info = get_gemini_response(extraction_prompt)

#         # Parse the JSON string
#         job_info = json.loads(extracted_info)

#         # Format the extracted information into a single string
#         formatted_job_info = f"""
#         Role: {job_info['role']}

#         Experience: {job_info['experience']}

#         Skills: {job_info['skills']}

#         Description: {job_info['description']}
#         """

#         return formatted_job_info

#     except Exception as e:
#         return f"Error extracting job description: {str(e)}"

# input_prompt = """
# Hey Act Like a skilled or very experience ATS(Application Tracking System) with a deep understanding of tech field,software engineering,data science ,data analyst and big data engineer. Your task is to evaluate the resume based on the given job description. You must consider the job market is very competitive and you should provide best assistance for improving thr resumes. Assign the percentage Matching based on Jd and the missing keywords with high accuracy resume:{text} description:{jd}

# I want the response in one single string having the structure {{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
# """

# @app.route('/api/analyze', methods=['POST'])
# def analyze():
#     if 'resume' not in request.files:
#         return jsonify({"error": "No file part"})
#     file = request.files['resume']
#     job_url = request.form['job_url']
    
#     if file.filename == '':
#         return jsonify({"error": "No selected file"})
    
#     if file and job_url:
#         try:
#             resume_text = input_pdf_text(file)
#             job_description = extract_job_description(job_url)
#             final_prompt = input_prompt.format(text=resume_text, jd=job_description)
#             response = get_gemini_response(final_prompt)
            
#             response_dict = json.loads(response)
            
#             return jsonify(response_dict)
#         except Exception as e:
#             return jsonify({"error": str(e)})

# if __name__ == "__main__":
#     app.run(debug=True)