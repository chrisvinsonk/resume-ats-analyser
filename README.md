
# ATS Resume Analyzer

This project is an **ATS (Applicant Tracking System) Resume Analyzer** that helps job seekers improve their resumes based on a specific job description. By uploading your resume in PDF format and providing the job description, the system evaluates your resume's relevance and suggests missing keywords, helping you increase your chances of passing ATS filters.

## Features

- Upload your resume (PDF format)
- Provide a job description
- Get a match percentage between your resume and the job description
- Identify missing keywords
- Receive a profile summary to improve your resume
- Real-time analysis using Google Gemini AI

## Live Demo

[ATS Resume Analyzer Live](https://resume-ats-analyser.vercel.app/) 

## Getting Started

Follow these instructions to run the project locally or contribute.

### Prerequisites

Make sure you have the following installed:

- [Node.js](https://nodejs.org/)
- [Python](https://www.python.org/)
- [Vercel CLI](https://vercel.com/download)
- A [Google Gemini API key](https://developers.generativeai.google/)

### Project Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/ats-resume-analyzer.git
   cd ats-resume-analyzer
   ```

2. Install the required dependencies:

   ```bash
   npm install
   ```

3. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   Create a `.env` file in the project root and add your Gemini API key:

   ```
   GEMINI_API_KEY=your-gemini-api-key
   ```

5. Run the application locally:

   ```bash
   vercel dev
   ```

   The project should now be running on `http://localhost:3000`.

## Contributing

Feel free to fork the project and submit pull requests for new features or improvements. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
