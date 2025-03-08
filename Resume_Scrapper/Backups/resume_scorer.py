import pdfplumber
import read_resume
import File_downloader_from_github
import re
import pandas as pd

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using pdfplumber."""
    with pdfplumber.open(pdf_path) as pdf:
        text = "".join(page.extract_text() or "" for page in pdf.pages)
    return text

def parse_resume_sections(resume_text, resume_name):
    """Parses different sections from a resume text."""
    section_headers = ["SUMMARY", "CONTACT", "OBJECTIVE", "REFERENCES", "SKILLS", "EDUCATION", "EXPERIENCE", "PROJECTS"]
    normalized_text = re.sub(r'[\r\u2022\u200b]', '', resume_text)  # Remove special characters
    normalized_text = re.sub(r'-\n', '', normalized_text)  # Fix line breaks
    normalized_text = "\n" + normalized_text + "\n"  # Buffer for boundary matching
    
    sections = {}
    section_positions = []
    for header in section_headers:
        pattern = re.compile(rf'\n\s*{re.escape(header)}[\s:•\-]*\n+', re.IGNORECASE)
        for match in pattern.finditer(normalized_text):
            section_positions.append((match.start(), header))
    
    section_positions.sort()
    prev_end, prev_header = 0, "BASIC_INFO"
    
    for start, header in section_positions:
        sections[prev_header] = normalized_text[prev_end:start].strip()
        prev_end = start
        prev_header = header.upper()
    
    sections[prev_header] = normalized_text[prev_end:].strip()
    
    print(f"✅ Extracted sections of {resume_name}: {list(sections.keys())}")
    return sections

def load_dataset(file_path):
    """Loads a dataset from a CSV file."""
    return pd.read_csv(file_path)

def match_keywords(section_text, dataset, column_name, metric_column):
    """Finds matching entries from a dataset in the given section text."""
    if not section_text:
        return pd.DataFrame(columns=[metric_column])
    section_text = section_text.lower()
    return dataset[dataset[column_name].str.lower().apply(lambda x: x in section_text)][[metric_column]]

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

def process_resume(pdf_path, company_df, skills_df, universities_df):
    """Processes a resume and returns its score."""
    resume_text =  read_resume.extract_text_and_links_from_pdf(pdf_path)
    resume_sections = parse_resume_sections(resume_text, pdf_path.split("/")[-1])
    
    company_ranks = match_keywords(resume_sections.get("EXPERIENCE", ""), company_df, 'Name', 'Rank')
    skills_scores = match_keywords(resume_sections.get("SKILLS", ""), skills_df, 'Skill', 'Score')
    university_rankings = match_keywords(resume_sections.get("EDUCATION", ""), universities_df, 'University', 'ranking')
    
    has_experience = "EXPERIENCE" in resume_sections and bool(resume_sections["EXPERIENCE"].strip())
    
    return calculate_resume_score(company_ranks, skills_scores, university_rankings, has_experience)

if __name__ == "__main__":
    company_df = load_dataset('/workspaces/SIMS-Project/Resume_Scrapper/Datasets/Companies_Dataset.csv')
    skills_df = load_dataset('/workspaces/SIMS-Project/Resume_Scrapper/Datasets/Skills_Dataset.csv')
    universities_df = load_dataset('/workspaces/SIMS-Project/Resume_Scrapper/Datasets/Universities_Dataset.csv')
    
    resume_files = [
        '/workspaces/SIMS-Project/Resume_Scrapper/Resumes/autoCV (1).pdf',
        '/workspaces/SIMS-Project/Resume_Scrapper/Resumes/autoCV (2).pdf',
        '/workspaces/SIMS-Project/Resume_Scrapper/Resumes/autoCV (3).pdf',
        '/workspaces/SIMS-Project/Resume_Scrapper/Resumes/autoCV (4).pdf',
        '/workspaces/SIMS-Project/Resume_Scrapper/Resumes/autoCV (5).pdf',
        '/workspaces/SIMS-Project/Resume_Scrapper/Resumes/me.pdf',
        '/workspaces/SIMS-Project/Resume_Scrapper/Resumes/autoCV.pdf',
        '/workspaces/SIMS-Project/Resume_Scrapper/Resumes/Resume_2.pdf',
        '/workspaces/SIMS-Project/Resume_Scrapper/Resumes/Resume.pdf'
    ]
    
    resume_scores = [(file, process_resume(file, company_df, skills_df, universities_df)) for file in resume_files]
    resume_scores.sort(key=lambda x: x[1], reverse=True)
    
    # print("Extracted Links:")
    # for link in extracted_links:
    #     print(link)

    # for link in extracted_links:
    #     if "github" in link:
    #         file_downloader.Downloader(link)
    
    print("Ranked Resumes (Highest to Lowest):")
    for rank, (file, score) in enumerate(resume_scores, start=1):
        print(f"Rank {rank}: {file[24:]} (Score: {score})")
