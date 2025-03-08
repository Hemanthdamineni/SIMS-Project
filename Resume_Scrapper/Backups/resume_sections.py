import read_resume
import File_downloader_from_github as file_downloader
import re
import os
import pandas as pd
from collections import Counter

keywords = {'Summary' : 0, 
            'Projects' : 0, 
            'Experience' : 0, 
            'Education' : 0, 
            'Skills' : 0,
            'Abstract' : 0
}

# Example tier mappings
company_tiers = {
    (1, 10): 100, (11, 50): 90, (51, 100): 80, (101, 1000): 70, 
    (1001, 5000): 60, (5001, 20000): 50, (20001, 50000): 40, (50001, 100000): 30, 
    (100001, 200000): 20, (200001, float('inf')): 10
}

university_tiers = {
    (1, 10): 100, (11, 50): 90, (51, 100): 80, (101, 250): 70, 
    (251, 500): 60, (501, 1000): 50, (1001, 1500): 40, (1501, 2000): 30, 
    (2001, 3000): 20, (3001, float('inf')): 10
}

def load_rankings(company_csv, university_csv, skills_csv):
    """
    Loads company, university rankings, and skills from CSV files.
    """
    company_df = pd.read_csv(company_csv).dropna(subset=['Name', 'Rank'])
    university_df = pd.read_csv(university_csv).dropna(subset=['University', 'ranking'])
    skills_df = pd.read_csv(skills_csv).dropna(subset=['Skill', 'Score'])

    company_ranking = {name.strip().lower(): int(rank) for name, rank in zip(company_df['Name'], company_df['Rank'])}
    university_ranking = {name.strip().lower(): int(rank) for name, rank in zip(university_df['University'], university_df['ranking'])}
    skill_scores = {skill.strip().lower(): float(score) for skill, score in zip(skills_df['Skill'], skills_df['Score'])}

    return company_ranking, university_ranking, skill_scores

def Resume_Section_Divider(resume_text):
    section_headers = ["SUMMARY", "CONTACT", "OBJECTIVE", "REFERENCES", "SKILLS", "EDUCATION", "EXPERIENCE", "PROJECTS"]
    
    # Preprocess text for consistent matching
    normalized_text = re.sub(r'[\r\u2022\u200b]', '', resume_text)  # Remove special chars
    normalized_text = re.sub(r'-\n', '', normalized_text)  # Handle hyphenated line breaks
    normalized_text = "\n" + normalized_text + "\n"  # Add buffer for boundary matches
    
    # Find all section positions
    section_positions = []
    for header in section_headers:
        pattern = re.compile(
            rf'\n\s*{re.escape(header)}\s*\n',
            re.IGNORECASE | re.DOTALL
        )
        for match in pattern.finditer(normalized_text):
            section_positions.append((match.start(), header.upper()))
    
    # Sort sections by appearance order
    section_positions.sort()
    sorted_sections = [header for _, header in section_positions]
    
    # Add Basic Info as first section if no sections found
    if not sorted_sections:
        sorted_sections = ["BASIC_INFO"]
    
    # Extract content between sections
    sections = {}
    prev_end = 0
    prev_header = "BASIC_INFO"
    
    for start, header in section_positions:
        sections[prev_header] = normalized_text[prev_end:start].strip()
        prev_end = start
        prev_header = header
    
    # Add final section
    sections[prev_header] = normalized_text[prev_end:].strip()
    
    # Save to files
    os.makedirs("Resume_Scrapper/Downloaded/resume_text", exist_ok=True)
    for section, content in sections.items():
        filename = f"{section.replace(' ', '_')}.txt"
        with open(f'Resume_Scrapper/Downloaded/resume_text/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"✅ Extracted sections: {list(sections.keys())}")

def Resume_score_calc_new(resume_text):
    # Exhaustive list of section headers
    section_headers = [
        # Core sections
        "CONTACT INFORMATION", "SUMMARY", "PROFESSIONAL SUMMARY", "OBJECTIVE",
        "EXPERIENCE", "WORK EXPERIENCE", "EMPLOYMENT HISTORY",
        "EDUCATION", "ACADEMIC BACKGROUND",
        "SKILLS", "TECHNICAL SKILLS", "KEY SKILLS",
        
        # Common specialized sections
        "PROJECTS", "KEY PROJECTS", "CERTIFICATIONS", "LICENSES",
        "AWARDS", "HONORS", "ACHIEVEMENTS", "PUBLICATIONS", "RESEARCH EXPERIENCE",
        "VOLUNTEER EXPERIENCE", "LANGUAGES", "INTERESTS", "HOBBIES",
        
        # Tech/Engineering specific
        "TECHNICAL EXPERTISE", "PROGRAMMING SKILLS", "FRAMEWORKS", "TOOLS", "DATABASES",
        
        # Academic/Research specific
        "TEACHING EXPERIENCE", "CONFERENCE PRESENTATIONS", "GRANTS", "FELLOWSHIPS", "PATENTS",
        
        # Industry specific
        "CLEARANCES", "SAFETY CERTIFICATIONS", "CLINICAL EXPERIENCE",
        
        # Creative fields
        "PORTFOLIO", "EXHIBITIONS", "PERFORMANCES",
        
        # Corporate fields
        "LEADERSHIP EXPERIENCE", "MANAGEMENT EXPERIENCE", "CLIENT ENGAGEMENTS",
        
        # Alternative names
        "CAREER HIGHLIGHTS", "PROFESSIONAL DEVELOPMENT", "CORE COMPETENCIES",
        
        # Military/Govt
        "SECURITY CLEARANCE", "MILITARY SERVICE",
        
        # Catch-all for remaining content
        "ADDITIONAL INFORMATION", "REFERENCES"
    ]
    
    # Preprocess text for consistent matching
    normalized_text = re.sub(r'[\r\u2022\u200b]', '', resume_text)  # Remove special chars
    normalized_text = re.sub(r'-\n', '', normalized_text)  # Handle hyphenated line breaks
    normalized_text = "\n" + normalized_text + "\n"  # Add buffer for boundary matches
    
    # Create regex patterns for each header
    patterns = {}
    for header in section_headers:
        # Allow for: "SKILLS", "SKILLS:", "SKILLS -", "SKILLS •"
        pattern_str = re.escape(header) + r'[\s:•\-]*'
        patterns[header] = re.compile(
            rf'\n\s*{pattern_str}\s*\n+',
            re.IGNORECASE | re.DOTALL
        )
    
    # Find all section positions
    section_positions = []
    for header, pattern in patterns.items():
        for match in pattern.finditer(normalized_text):
            section_positions.append((match.start(), header.upper()))
    
    # Sort sections by appearance order
    section_positions.sort()
    sorted_sections = [header for _, header in section_positions]
    
    # Add Basic Info as first section if no sections found
    if not sorted_sections:
        sorted_sections = ["BASIC_INFO"]
    
    # Extract content between sections
    sections = {}
    prev_end = 0
    prev_header = "BASIC_INFO"
    
    for start, header in section_positions:
        sections[prev_header] = normalized_text[prev_end:start].strip()
        prev_end = start
        prev_header = header
    
    # Add final section
    sections[prev_header] = normalized_text[prev_end:].strip()
    
    # Save to files
    os.makedirs("Resume_Scrapper/Downloaded/resume_text", exist_ok=True)
    for section, content in sections.items():
        filename = f"{section.replace(' ', '_')}.txt"
        with open(f'Resume_Scrapper/Downloaded/resume_text/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"✅ Extracted sections: {list(sections.keys())}")

if __name__ == "__main__":
    resume_name = 'Resume.pdf'
    pdf_path = "Resume_Scrapper/Resumes/" + resume_name
    resume_name = resume_name[:-4]

    resume_text, extracted_links = read_resume.extract_text_and_links_from_pdf(pdf_path)

    with open('Resume_Scrapper/Downloaded/resume_text/' + resume_name + ".txt", "wb") as f:
        f.write(resume_text.encode('utf-8'))
    print(f"Downloaded: {resume_name}.txt")

    print("Extracted Links:")
    for link in extracted_links:
        print(link)

    for link in extracted_links:
        if "github" in link:
            file_downloader.Downloader(link)
    
    company_csv = "Resume_Scrapper/Datasets/Companies_Dataset.csv"
    university_csv = "Resume_Scrapper/Datasets/Universities_Dataset.csv"
    skills_csv = "Resume_Scrapper/Datasets/Skills_Dataset.csv"

    company_ranking, university_ranking, skill_scores = load_rankings(company_csv, university_csv, skills_csv)

    Resume_Section_Divider(resume_text)
    # Resume_score_calc_new(resume_text)
