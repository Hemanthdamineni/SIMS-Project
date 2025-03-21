import os
import re
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any

import re
import os
from typing import Dict

def parse_resume_sections(resume_text: str, resume_name: str, 
                         base_path: str = "Downloaded/resume_text/") -> Dict[str, str]:
    """
    Parses different sections from a resume text.
    
    Args:
        resume_text: The full text of the resume
        resume_name: Name of the resume file
        base_path: Directory to save extracted sections
        
    Returns:
        Dictionary with section names as keys and content as values
    """
    # Define section keywords mapping
    section_keywords = {
        "EDUCATION": ["EDUCATION", "ACADEMIC"],
        "EXPERIENCE": ["EXPERIENCE", "EMPLOYMENT", "WORK HISTORY", "PROFESSIONAL BACKGROUND"],
        "SKILLS": ["SKILLS", "SKILL SUMMARY", "TECHNOLOGIES", "TECHNICAL SKILLS", "COMPETENCIES"],
        "PROJECTS": ["PROJECTS", "PROJECT", "PORTFOLIO"],
        "CERTIFICATIONS": ["CERTIFICATION", "CREDENTIAL", "QUALIFICATION", "PROFESSIONAL DEVELOPMENT"],
        "AWARDS": ["AWARD", "HONOR", "ACHIEVEMENT", "RECOGNITION"],
        "PUBLICATIONS": ["PUBLICATION", "RESEARCH", "ARTICLE", "JOURNAL"],
        "SUMMARY": ["SUMMARY", "PROFILE", "OBJECTIVE", "ABOUT"],
        "CONTACT": ["CONTACT", "INFORMATION", "PERSONAL", "DETAILS"],
        "LANGUAGES": ["LANGUAGE", "LINGUISTIC"],
        "INTERESTS": ["INTEREST", "HOBBY", "ACTIVITY"],
        "REFERENCES": ["REFERENCE", "RECOMMENDATION"]
    }
    
    # Initialize sections dictionary
    sections = {key: "" for key in section_keywords}
    
    # Normalize text: remove special characters and handle hyphenated line breaks
    normalized_text = re.sub(r'[\r\u2022\u200b]', '', resume_text)
    normalized_text = re.sub(r'-\n', '', normalized_text)
    normalized_text = "\n" + normalized_text + "\n"
    
    # Find section positions
    section_positions = []
    for section, keywords in section_keywords.items():
        for keyword in keywords:
            pattern = re.compile(rf'\n\s*{keyword}[\s:•\-]*\n+', re.IGNORECASE)
            for match in pattern.finditer(normalized_text):
                section_positions.append((match.start(), section))
    
    # Sort positions by their appearance in the text
    section_positions.sort()
    
    # Extract content between sections
    prev_end, prev_section = 0, "BASIC_INFO"
    sections[prev_section] = ""  # Initialize BASIC_INFO section
    
    for start, section in section_positions:
        sections[prev_section] = normalized_text[prev_end:start].strip()
        prev_end = start
        prev_section = section
    
    # Add the last section
    sections[prev_section] = normalized_text[prev_end:].strip()
    
    # Create directory if it doesn't exist
    os.makedirs(base_path, exist_ok=True)
    
    # Save non-empty sections to files
    for section_name, content in sections.items():
        if content.strip():  # Only save non-empty sections
            filename = f"{section_name.replace(' ', '_')}.txt"
            section_file = f"{base_path}/{resume_name}-{filename}"
            with open(section_file, 'w', encoding='utf-8') as f:
                f.write(content)
    
    return sections

def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Loads a dataset from a CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Pandas DataFrame containing the dataset
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading dataset from {file_path}: {e}")
        return pd.DataFrame()  # Return empty dataframe on error

def match_keywords(text: str, dataset: pd.DataFrame, 
                  keyword_col: str, score_col: str) -> pd.DataFrame:
    """
    Finds matching entries from a dataset in the given text.
    
    Args:
        text: Text to search for keywords
        dataset: DataFrame containing keywords to match
        keyword_col: Column name containing keywords
        score_col: Column name containing scores/ranks
        
    Returns:
        DataFrame with matching entries and a 'Found' column
    """
    results = []
    text = text.lower()
    
    for _, row in dataset.iterrows():
        keyword = str(row[keyword_col]).lower()
        if keyword in text:
            results.append({
                keyword_col: row[keyword_col],
                score_col: row[score_col],
                'Found': True
            })
    
    return pd.DataFrame(results, columns=[keyword_col, score_col, 'Found'])

def calculate_resume_score(company_matches: pd.DataFrame, skills_matches: pd.DataFrame, 
                          university_matches: pd.DataFrame, github_links: List[str], 
                          sections: Dict[str, str]) -> float:
    """
    Calculates the resume score based on different weighted factors.
    
    Args:
        company_matches: DataFrame with matched companies
        skills_matches: DataFrame with matched skills
        university_matches: DataFrame with matched universities
        github_links: List of GitHub links found in the resume
        sections: Dictionary of resume sections
        
    Returns:
        The calculated resume score
    """
    score = 0
    
    # Add points for matched companies
    if not company_matches.empty:
        score += company_matches[company_matches.columns[1]].sum() * 5
    
    # Add points for matched skills
    if not skills_matches.empty:
        score += skills_matches[skills_matches.columns[1]].sum() * 3
    
    # Add points for matched universities
    if not university_matches.empty:
        score += university_matches[university_matches.columns[1]].sum() * 8
    
    # Apply penalty if no work experience
    if not sections.get("EXPERIENCE", "").strip():
        score *= 0.8  # Reduce score by 20%
    
    scaled_score = round(score / 10, 2) // 2  # Adjust scaling factor as needed
    return scaled_score

def process_resume(pdf_path: str, company_df: pd.DataFrame, 
                  skills_df: pd.DataFrame, universities_df: pd.DataFrame,
                  text_extractor=None) -> Tuple[float, Dict[str, str], List[str], 
                                               pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Processes a resume and returns its analysis.
    
    Args:
        pdf_path: Path to the resume PDF
        company_df: DataFrame with company rankings
        skills_df: DataFrame with skill scores
        universities_df: DataFrame with university rankings
        text_extractor: Function to extract text from PDF (optional)
        
    Returns:
        Tuple containing (score, sections, github_links, company_matches, skills_matches, university_matches)
    """
    try:
        # Import text extractor function if not provided
        if text_extractor is None:
            from read_resume import extract_text_and_links_from_pdf as text_extractor
            
        # Extract text and links
        resume_text, links = text_extractor(pdf_path)
        
        # Extract resume name from path
        resume_name = os.path.basename(pdf_path)
        
        # Parse resume into sections
        sections = parse_resume_sections(resume_text, resume_name)
        
        # Filter for GitHub links
        github_links = [link for link in links if "github.com" in link.lower()]
        
        # # Match keywords in sections
        company_matches = match_keywords(sections.get("EXPERIENCE", ""), company_df, 'Name', 'Rank')
        skills_matches = match_keywords(sections.get("SKILLS", ""), skills_df, 'Skill', 'Score')
        university_matches = match_keywords(sections.get("EDUCATION", ""), universities_df, 'University', 'ranking')
        
        # Calculate score
        score = calculate_resume_score(company_matches, skills_matches, university_matches, github_links, sections)
        
        return score, sections, github_links, 
            # company_matches, skills_matches, university_matches
        
    except Exception as e:
        print(f"Error processing resume: {e}")
        return 0, {}, [], pd.DataFrame(), pd.DataFrame(), pd.DataFrame()