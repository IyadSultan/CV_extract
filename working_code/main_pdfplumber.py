import pdfplumber
from typing import Optional, List
from pydantic import BaseModel
from pydantic_ai import Agent
import re
from dotenv import load_dotenv
import os
import time
import csv
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PDFReader

load_dotenv()

class TechnicalSkills(BaseModel):
    python_experience: str
    other_languages: List[str]
    github_repos: Optional[List[str]]
    github_profile: Optional[str]
    django_experience: Optional[str]
    sql_experience: Optional[str]
    azure_experience: Optional[str]
    aws_experience: Optional[str]

class Education(BaseModel):
    bachelors: Optional[str]
    masters: Optional[str]
    phd: Optional[str]
    awards: Optional[List[str]]

class Experience(BaseModel):
    data_science_experience: Optional[str]
    healthcare_experience: Optional[str]
    total_years: Optional[float]
    important_projects: Optional[List[str]]

class SocialLinks(BaseModel):
    linkedin_url: Optional[str]
    github_url: Optional[str]

class ContactInfo(BaseModel):
    """Contact information from the resume"""
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]

class ResumeAnalysis(BaseModel):
    """Complete analysis of a candidate's resume"""
    contact_info: ContactInfo  # Added contact info
    technical_skills: TechnicalSkills
    education: Education
    experience: Experience
    social_links: SocialLinks
    overall_fit_score: float
    fit_justification: str

# Create the agent
resume_agent = Agent(
    'gpt-4o-mini',
    result_type=ResumeAnalysis,
    # api_key=os.getenv('OPENAI_API_KEY'),
    system_prompt="""
    You are an expert resume analyzer for a Lead Data Scientist position. Your task is to thoroughly analyze resumes 
    and extract specific information. Focus on these key areas:

    Contact Information:
    - Extract the candidate's full name
    - Find email address
    - Identify phone number
    
    Technical Skills Analysis:
    - Identify specific Python experience, including frameworks and libraries
    - List all programming languages mentioned
    - Find Django-related experience
    - Evaluate SQL and database experience
    - Assess Azure cloud services experience and expertise
    - Evaluate AWS cloud platform experience and expertise
    - Extract GitHub repositories or project links

    Education Analysis:
    - Extract all degrees (Bachelor's, Master's, PhD)
    - Note the universities and graduation years
    - Identify relevant awards, honors, or certifications

    Experience Analysis:
    - Calculate total years of relevant experience
    - Identify data science and machine learning projects
    - Note any healthcare industry experience
    - Extract significant projects and their impacts
    - Look for leadership or team management experience

    Provide a fit score (0-10) based on:
    - Technical expertise (including cloud platforms) (40%)
    - Relevant experience (30%)
    - Education (20%)
    - Leadership potential (10%)

    Be precise and factual. If information is not explicitly stated, mark as None.
    For cloud experience, note specific services used and level of expertise.
    For experience calculations, use concrete dates and roles mentioned.
    """
)

def clean_text(text: str) -> str:
    """Clean and normalize the extracted text"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,;()-@]', '', text)
    # Normalize line breaks
    text = text.replace('\n', ' ').strip()
    return text

def extract_info_from_pdf(file_path: str) -> Optional[ResumeAnalysis]:
    """
    Extract and analyze information from a PDF resume using LlamaParse
    Returns None if analysis fails
    """
    try:
        print(f"Extracting text from: {file_path}")
        # Extract text using LlamaParse
        reader = PDFReader()
        documents = reader.load_data(file_path)
        text = " ".join([doc.text for doc in documents])

        if not text.strip():
            print("Warning: No text extracted from PDF")
            return None

        # Clean the extracted text
        cleaned_text = clean_text(text)
        print("Text extraction and cleaning completed successfully")
        
        # Retry logic for API calls
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"Attempting analysis (attempt {attempt + 1})")
                result = resume_agent.run_sync(cleaned_text)
                print("Analysis completed successfully")
                return result.data
            except Exception as api_error:
                if attempt == max_retries - 1:  # Last attempt
                    print(f"Failed after {max_retries} attempts: {str(api_error)}")
                    return None
                print(f"Attempt {attempt + 1} failed, retrying... Error: {str(api_error)}")
                time.sleep(2)  # Wait 2 seconds before retrying

    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return None

def print_analysis(analysis: ResumeAnalysis):
    """Print the analysis in a well-formatted way"""
    print("\n📋 Resume Analysis Report")
    print("=" * 50)

    print("\n👤 Contact Information")
    print("-" * 30)
    print(f"Name: {analysis.contact_info.name}")
    print(f"Email: {analysis.contact_info.email}")
    print(f"Phone: {analysis.contact_info.phone}")

    print("\n🔧 Technical Skills")
    print("-" * 30)
    print(f"Python Experience: {analysis.technical_skills.python_experience}")
    print(f"Other Languages: {', '.join(analysis.technical_skills.other_languages)}")
    print(f"Django Experience: {analysis.technical_skills.django_experience}")
    print(f"SQL Experience: {analysis.technical_skills.sql_experience}")
    print(f"Azure Experience: {analysis.technical_skills.azure_experience}")
    print(f"AWS Experience: {analysis.technical_skills.aws_experience}")
    if analysis.technical_skills.github_repos:
        print(f"GitHub Repos: {', '.join(analysis.technical_skills.github_repos)}")
    if analysis.technical_skills.github_profile:
        print(f"GitHub Profile: {analysis.technical_skills.github_profile}")

    # Add social links section
    print("\n🔗 Social Links")
    print("-" * 30)
    if analysis.social_links.linkedin_url:
        print(f"LinkedIn: {analysis.social_links.linkedin_url}")
    if analysis.social_links.github_url:
        print(f"GitHub: {analysis.social_links.github_url}")

    print("\n🎓 Education")
    print("-" * 30)
    print(f"Bachelor's: {analysis.education.bachelors}")
    print(f"Master's: {analysis.education.masters}")
    print(f"PhD: {analysis.education.phd}")
    if analysis.education.awards:
        print(f"Awards: {', '.join(analysis.education.awards)}")

    print("\n💼 Experience")
    print("-" * 30)
    print(f"Data Science Experience: {analysis.experience.data_science_experience}")
    print(f"Healthcare Experience: {analysis.experience.healthcare_experience}")
    print(f"Total Years: {analysis.experience.total_years}")
    if analysis.experience.important_projects:
        print("\nKey Projects:")
        for project in analysis.experience.important_projects:
            print(f"• {project}")

    print("\n🎯 Overall Fit Assessment")
    print("-" * 30)
    print(f"Score: {analysis.overall_fit_score}/10")
    print(f"Justification: {analysis.fit_justification}")

def save_analysis_to_markdown(analyses: List[tuple[str, ResumeAnalysis]], output_file: str):
    """Save multiple resume analyses to a markdown file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Resume Analysis Report\n\n")
        
        for filename, analysis in analyses:
            f.write(f"## {os.path.basename(filename)}\n\n")
            
            # Add contact information section
            f.write("### 👤 Contact Information\n\n")
            f.write(f"- **Name:** {analysis.contact_info.name}\n")
            f.write(f"- **Email:** {analysis.contact_info.email}\n")
            f.write(f"- **Phone:** {analysis.contact_info.phone}\n\n")
            
            # Add social links section
            f.write("### 🔗 Social Links\n\n")
            if analysis.social_links.linkedin_url:
                f.write(f"- [LinkedIn Profile]({analysis.social_links.linkedin_url})\n")
            if analysis.social_links.github_url:
                f.write(f"- [GitHub Profile]({analysis.social_links.github_url})\n")
            f.write("\n")
            
            f.write("### 🔧 Technical Skills\n\n")
            f.write(f"- **Python Experience:** {analysis.technical_skills.python_experience}\n")
            f.write(f"- **Other Languages:** {', '.join(analysis.technical_skills.other_languages)}\n")
            f.write(f"- **Django Experience:** {analysis.technical_skills.django_experience}\n")
            f.write(f"- **SQL Experience:** {analysis.technical_skills.sql_experience}\n")
            f.write(f"- **Azure Experience:** {analysis.technical_skills.azure_experience}\n")
            f.write(f"- **AWS Experience:** {analysis.technical_skills.aws_experience}\n")
            if analysis.technical_skills.github_repos:
                f.write(f"- **GitHub Repos:** {', '.join(analysis.technical_skills.github_repos)}\n")
            if analysis.technical_skills.github_profile:
                f.write(f"- **GitHub Profile:** {analysis.technical_skills.github_profile}\n")

            f.write("\n### 🎓 Education\n\n")
            f.write(f"- **Bachelor's:** {analysis.education.bachelors}\n")
            f.write(f"- **Master's:** {analysis.education.masters}\n")
            f.write(f"- **PhD:** {analysis.education.phd}\n")
            if analysis.education.awards:
                f.write(f"- **Awards:** {', '.join(analysis.education.awards)}\n")
            
            f.write("\n### 💼 Experience\n\n")
            f.write(f"- **Data Science Experience:** {analysis.experience.data_science_experience}\n")
            f.write(f"- **Healthcare Experience:** {analysis.experience.healthcare_experience}\n")
            f.write(f"- **Total Years:** {analysis.experience.total_years}\n")
            if analysis.experience.important_projects:
                f.write("\n**Key Projects:**\n")
                for project in analysis.experience.important_projects:
                    f.write(f"- {project}\n")
            
            f.write("\n### 🎯 Overall Fit Assessment\n\n")
            f.write(f"**Score:** {analysis.overall_fit_score}/10\n\n")
            f.write(f"**Justification:** {analysis.fit_justification}\n\n")
            
            f.write("---\n\n")  # Separator between resumes

def save_analysis_to_csv(analyses: List[tuple[str, ResumeAnalysis]], output_file: str):
    """Save multiple resume analyses to a CSV file"""
    fieldnames = [
        'filename',
        'name',           # Added
        'email',          # Added
        'phone',          # Added
        'python_experience',
        'other_languages',
        'django_experience',
        'sql_experience',
        'azure_experience',
        'aws_experience',
        'github_repos',
        'github_profile',
        'linkedin_url',
        'github_url',
        'bachelors',
        'masters',
        'phd',
        'awards',
        'data_science_experience',
        'healthcare_experience',
        'total_years',
        'important_projects',
        'overall_fit_score',
        'fit_justification'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for filename, analysis in analyses:
            writer.writerow({
                'filename': os.path.basename(filename),
                'name': analysis.contact_info.name,
                'email': analysis.contact_info.email,
                'phone': analysis.contact_info.phone,
                'python_experience': analysis.technical_skills.python_experience,
                'other_languages': ', '.join(analysis.technical_skills.other_languages),
                'django_experience': analysis.technical_skills.django_experience,
                'sql_experience': analysis.technical_skills.sql_experience,
                'azure_experience': analysis.technical_skills.azure_experience,
                'aws_experience': analysis.technical_skills.aws_experience,
                'github_repos': ', '.join(analysis.technical_skills.github_repos) if analysis.technical_skills.github_repos else '',
                'github_profile': analysis.technical_skills.github_profile,
                'linkedin_url': analysis.social_links.linkedin_url,
                'github_url': analysis.social_links.github_url,
                'bachelors': analysis.education.bachelors,
                'masters': analysis.education.masters,
                'phd': analysis.education.phd,
                'awards': ', '.join(analysis.education.awards) if analysis.education.awards else '',
                'data_science_experience': analysis.experience.data_science_experience,
                'healthcare_experience': analysis.experience.healthcare_experience,
                'total_years': analysis.experience.total_years,
                'important_projects': ', '.join(analysis.experience.important_projects) if analysis.experience.important_projects else '',
                'overall_fit_score': analysis.overall_fit_score,
                'fit_justification': analysis.fit_justification
            })

def main():
    # Directory containing CVs
    cv_directory = r'C:\Users\isult\OneDrive\Documents\CV_extract\CVs\cv_leads'
    markdown_file = 'resume_analysis_results.md'
    csv_file = 'resume_analysis_results.csv'
    
    # List to store all analyses
    all_analyses = []
    failed_files = []
    
    try:
        # Process all PDF files in the directory
        for filename in os.listdir(cv_directory):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(cv_directory, filename)
                print(f"\nProcessing: {filename}")
                
                # Extract and analyze the resume
                analysis = extract_info_from_pdf(pdf_path)
                
                if analysis is not None:
                    all_analyses.append((filename, analysis))
                    print_analysis(analysis)
                else:
                    failed_files.append(filename)
                    print(f"Skipping {filename} due to processing errors")
        
        # Save analyses to both markdown and CSV if we have any successful analyses
        if all_analyses:
            save_analysis_to_markdown(all_analyses, markdown_file)
            save_analysis_to_csv(all_analyses, csv_file)
            print(f"\nAnalyses saved to {markdown_file} and {csv_file}")
        
        # Report failed files
        if failed_files:
            print("\nFailed to process the following files:")
            for failed_file in failed_files:
                print(f"- {failed_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
