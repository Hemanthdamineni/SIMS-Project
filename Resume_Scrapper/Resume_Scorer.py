import read_resume
import File_downloader_from_github as file_downloader
import re
import pandas as pd
from collections import Counter

def load_rankings(company_csv, university_csv):
    """
    Loads company and university rankings from CSV files.
    """
    company_df = pd.read_csv(company_csv)
    university_df = pd.read_csv(university_csv)
    
    company_ranking = dict(zip(company_df['company'].str.lower(), company_df['rank']))
    university_ranking = dict(zip(university_df['university'].str.lower(), university_df['rank']))
    
    return company_ranking, university_ranking

def get_tier_score(entity, ranking_dict, tier_mapping):
    """
    Assigns a score based on the entity's ranking.
    """
    rank = ranking_dict.get(entity, None)
    if rank is None:
        return 0  # Entity not ranked
    
    for tier, score in tier_mapping.items():
        if tier[0] <= rank <= tier[1]:
            return score
    return 0

def calculate_resume_score(resume_text, company_csv, university_csv, skills_list, company_tiers, university_tiers):
    """
    Computes the weighted resume score based on extracted entities.
    """
    # Load rankings from CSV files
    company_ranking, university_ranking = load_rankings(company_csv, university_csv)
    
    # Tokenize resume text
    words = re.findall(r'\w+', resume_text.lower())
    word_counts = Counter(words)
    
    # Extract and score companies
    company_scores = [get_tier_score(company, company_ranking, company_tiers) for company in company_ranking if company in word_counts]
    
    # Extract and score universities
    university_scores = [get_tier_score(university, university_ranking, university_tiers) for university in university_ranking if university in word_counts]
    
    # Extract and score skills
    skill_scores = [10 for skill in skills_list if skill in word_counts]  # Simple fixed score per skill
    
    # Compute dynamic weights
    total_mentions = len(company_scores) + len(university_scores) + len(skill_scores)
    
    if total_mentions == 0:
        return 0  # No relevant data in resume
    
    company_weight = len(company_scores) / total_mentions
    university_weight = len(university_scores) / total_mentions
    skill_weight = len(skill_scores) / total_mentions
    
    # Compute final weighted score
    final_score = (
        sum(company_scores) * company_weight +
        sum(university_scores) * university_weight +
        sum(skill_scores) * skill_weight
    )
    
    return round(final_score, 2)

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

if __name__ == "__main__":  
    resume_name = 'autoCV (1).pdf'
    pdf_path = "Resume_Scrapper/Resumes/"+resume_name

    resume_text, extracted_links = read_resume.extract_text_and_links_from_pdf(pdf_path)
    
    # print(f"Extractd Text: {resume_text}")

    # print("Extracted Links:")
    # for link in extracted_links:
    #     print(link)
    # print("\n")

    with open("Resume_Scrapper/Downloaded/code_files"+resume_name, "wb") as f:
        f.write(resume_text)
    print(f"Downloaded: {resume_name}")
    
    for link in extracted_links:
        if "github" in link:
            file_downloader.Downloader(link)
    
    final_resume_score = calculate_resume_score(resume_text, company_csv, university_csv, skills_list, company_tiers, university_tiers)
    print("Final Resume Score:", final_resume_score)

    company_csv = "company_rankings.csv"
    university_csv = "university_rankings.csv"
    skills_list = ["python", "machine learning", "data science", "java"]
