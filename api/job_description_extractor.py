import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def scrape_job_posting(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # This is a generic scraping method. You might need to adjust it based on the specific website structure.
        job_description = soup.find('div', class_='job-description')
        return job_description.get_text() if job_description else "Could not find job description"
    except Exception as e:
        return f"Error scraping job posting: {str(e)}"

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def extract_job_description(url):
    scraped_data = scrape_job_posting(url)
    print(scraped_data)
    prompt = f"""
    Given the following job posting content, please extract and summarize the following information:
    1. Job Role
    2. Required Experience
    3. Required Skills
    4. Job Description Summary

    Please format the output as a JSON string with the following structure:
    {{
        "role": "Extracted job role",
        "experience": "Summarized required experience",
        "skills": ["Skill 1", "Skill 2", "Skill 3", ...],
        "description": "Summarized job description"
    }}

    Job Posting Content:
    {scraped_data}
    """

    response = get_gemini_response(prompt)
    return response

# Test the function
if __name__ == "__main__":
    # test_url = "https://www.linkedin.com/jobs/view/4047800476/" 
    test_url = "https://www.naukri.com/job-listings-analyst-data-science-assimilate-solutions-bengaluru-0-to-2-years-141024500349?src=drecomm_apply&sid=17292292744648238&xp=1&px=1" # Replace with an actual job posting URL
    result = extract_job_description(test_url)
    print(result)