import pdfplumber
import re
import pandas as pd

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def parse_resume_sections(resume_text):
    sections = {
        'Summary': '',
        'Skills': '',
        'Education': '',
        'Work Experience': '',
        'Projects': ''
    }
    
    # Improved regex to handle section extraction
    summary_match = re.search(r'Summary(.*?)(Skills|Education|Work Experience|Projects)', resume_text, re.DOTALL)
    if summary_match:
        sections['Summary'] = summary_match.group(1).strip()
    
    skills_match = re.search(r'Skills(.*?)(Education|Work Experience|Projects)', resume_text, re.DOTALL)
    if skills_match:
        sections['Skills'] = skills_match.group(1).strip()
    
    education_match = re.search(r'Education(.*?)(Work Experience|Projects)', resume_text, re.DOTALL)
    if education_match:
        sections['Education'] = education_match.group(1).strip()
    
    experience_match = re.search(r'Work Experience(.*?)Projects', resume_text, re.DOTALL)
    if experience_match:
        sections['Work Experience'] = experience_match.group(1).strip()
    
    projects_match = re.search(r'Projects(.*?)$', resume_text, re.DOTALL)
    if projects_match:
        sections['Projects'] = projects_match.group(1).strip()
    
    return sections

def save_sections_to_files(sections):
    for section_name, section_content in sections.items():
        with open(f'{section_name.lower().replace(" ", "_")}.txt', 'w') as file:
            file.write(section_content)

def load_dataset(file_path):
    return pd.read_csv(file_path)

def compare_and_extract_metrics(section_file, dataset, column_name, metric_column):
    with open(section_file, 'r') as file:
        section_content = file.read()
    
    # Find matches where the column_name appears in the section content
    matches = dataset[dataset[column_name].apply(lambda x: str(x).lower() in section_content.lower())]
    return matches[[metric_column]]

def calculate_resume_score(company_ranks, skills_scores, university_rankings, has_work_experience):
    # Use raw scores instead of normalized scores
    company_score = company_ranks['Rank'].min() if not company_ranks.empty else 0
    skills_score = skills_scores['Score'].sum() if not skills_scores.empty else 0
    university_score = university_rankings['ranking'].min() if not university_rankings.empty else 0
    
    # Assign weights
    company_weight = 2.0  # Adjust as needed
    skills_weight = 1.5   # Skills might be more important
    university_weight = 1.0  # Universities might be less important
    
    # Calculate weighted total score
    total_score = (
        (company_score * company_weight) +
        (skills_score * skills_weight) +
        (university_score * university_weight)
    )
    
    # Apply penalty for resumes without work experience
    if not has_work_experience:
        total_score *= 0.8  # Reduce score by 20% if no work experience
    
    # Scale the final score to a range of 0 to 100
    scaled_score = (total_score / 10)  # Adjust the divisor based on expected score range
    return round(scaled_score, 2)

# Function to process a resume and return its score
def process_resume(pdf_path):
    # Extract text from PDF
    resume_text = extract_text_from_pdf(pdf_path)
    
    # Parse resume sections
    resume_sections = parse_resume_sections(resume_text)
    
    # Save sections to files
    save_sections_to_files(resume_sections)
    
    # Load datasets
    company_df = load_dataset('Resume_Scrapper/Datasets/Companies_Dataset.csv')
    skills_df = load_dataset('Resume_Scrapper/Datasets/Skills_Dataset.csv')
    universities_df = load_dataset('Resume_Scrapper/Datasets/Universities_Dataset.csv')
    
    # Compare and extract metrics
    company_ranks = compare_and_extract_metrics('work_experience.txt', company_df, 'Name', 'Rank')
    skills_scores = compare_and_extract_metrics('skills.txt', skills_df, 'Skill', 'Score')
    university_rankings = compare_and_extract_metrics('education.txt', universities_df, 'University', 'ranking')
    
    # Check if work experience exists
    has_work_experience = bool(resume_sections['Work Experience'])
    
    # Calculate resume score
    resume_score = calculate_resume_score(company_ranks, skills_scores, university_rankings, has_work_experience)
    
    return resume_score

# List of resume files
resume_files = [
    'Resume_Scrapper/Resumes/autoCV (4).pdf',
    'Resume_Scrapper/Resumes/autoCV (3).pdf',
    'Resume_Scrapper/Resumes/autoCV (2).pdf',
    'Resume_Scrapper/Resumes/autoCV (1).pdf',
    'Resume_Scrapper/Resumes/resume_2 (1).pdf',
    'Resume_Scrapper/Resumes/Resume.pdf',
    'Resume_Scrapper/Resumes/Resume_2.pdf'
]

# Calculate scores for all resumes
resume_scores = []
for resume_file in resume_files:
    score = process_resume(resume_file)
    resume_scores.append((resume_file, score))  # Store as (resume_file, score) tuple

# Sort resumes by score (highest to lowest)
resume_scores.sort(key=lambda x: x[1], reverse=True)

# Print ranked resumes
print("Ranked Resumes (Highest to Lowest):")
for rank, (resume_file, score) in enumerate(resume_scores, start=1):
    print(f"Rank {rank}: {resume_file[24:]} (Score: {score})")