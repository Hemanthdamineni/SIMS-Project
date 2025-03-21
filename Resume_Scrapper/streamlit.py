import streamlit as st
import pandas as pd
import os
import base64
import io
import fitz  # PyMuPDF
from PIL import Image
from typing import Dict, List, Any

# Import custom modules
import read_resume
import resume_parser
import github_downloader

# Set page config
st.set_page_config(page_title="Resume Analyzer", layout="wide")

# Create necessary directories
os.makedirs("Downloaded/resume_text", exist_ok=True)
os.makedirs("Datasets", exist_ok=True)
os.makedirs("Resumes", exist_ok=True)

def create_download_button(file_name: str, file_content: bytes) -> str:
    """Creates a styled download button with an icon."""
    b64_content = base64.b64encode(file_content).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64_content}" download="{file_name}" style="text-decoration: none;">' \
           f'<button style="background-color: #1E88E5; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">' \
           f'⬇ Download {file_name}</button></a>'
    return href

def display_github_links(github_links: List[str], resume_name: str) -> None:
    """Displays GitHub links and handles file downloads."""
    st.markdown("<h3 class='sub-header'>Found GitHub Links</h3>", unsafe_allow_html=True)
    
    # Create tabs for each GitHub repository
    if github_links:
        repo_names = [link.split("/")[-1] for link in github_links]
        tabs = st.tabs(repo_names)
        
        for i, (link, repo_name) in enumerate(zip(github_links, repo_names)):
            with tabs[i]:
                # Display the GitHub link
                st.markdown(
                    f"""
                    <div style="border: 1px solid #e1e4e8; border-radius: 6px; padding: 16px; margin-bottom: 16px;">
                        <div style="display: flex; align-items: center;">
                            <img src="https://github.githubassets.com/favicons/favicon.png" width="24" height="24" style="margin-right: 8px;">
                            <a href="{link}" target="_blank" style="font-size: 16px; color: #1E88E5; text-decoration: none;">{link}</a>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Fetch and display files in a table
                with st.spinner(f"Fetching files from {repo_name}..."):
                    try:
                        downloadable_files = github_downloader.download_github_repo(link)
                        if downloadable_files:
                            # Create a table to display files
                            st.markdown("<h4>Files in Repository</h4>", unsafe_allow_html=True)
                            
                            # Create a list to store file details
                            file_details = []
                            
                            for file_name, file_content in downloadable_files:
                                # Encode file content for download
                                b64_content = base64.b64encode(file_content).decode()
                                download_link = f'<a href="data:application/octet-stream;base64,{b64_content}" download="{file_name}" style="text-decoration: none;"><button style="background-color: #1E88E5; color: white; padding: 5px 10px; border: none; border-radius: 5px; cursor: pointer;">⬇ Download</button></a>'
                                visit_link = f'<a href="{link}" target="_blank" style="text-decoration: none;"><button style="background-color: #4CAF50; color: white; padding: 5px 10px; border: none; border-radius: 5px; cursor: pointer;">🌐 Visit</button></a>'
                                
                                # Add file details to the list
                                file_details.append({
                                    "File Name": file_name,
                                    "Download": download_link,
                                    "Visit": visit_link
                                })
                            
                            # Convert the list to a DataFrame
                            files_df = pd.DataFrame(file_details)
                            
                            # Display the table using st.markdown to render HTML
                            st.markdown(files_df.to_html(escape=False, index=False), unsafe_allow_html=True)
                        else:
                            st.warning(f"⚠ No files found in {repo_name}")
                    except Exception as e:
                        st.error(f"❌ Failed to fetch files from {repo_name}: {str(e)}")
    else:
        st.warning("No GitHub links found in the resume.")

def load_datasets():
    """Load datasets with fallback to sample data"""
    try:
        company_df = resume_parser.load_dataset('Datasets/Companies_Dataset.csv')
        skills_df = resume_parser.load_dataset('Datasets/Skills_Dataset.csv')
        universities_df = resume_parser.load_dataset('Datasets/Universities_Dataset.csv')
        
    except Exception as e:
        st.warning(f"Error loading datasets: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    return company_df, skills_df, universities_df

def display_recommendations(non_empty_sections: Dict[str, str], github_links: List[str]):
    """Display recommendations based on resume analysis"""
    st.markdown("<h2 class='sub-header'>Recommendations</h2>", unsafe_allow_html=True)
    
    recommendations = []
    
    # Generate recommendations based on analysis
    if "SKILLS" not in non_empty_sections:
        recommendations.append("Add a detailed Skills section to your resume.")
    
    if "EXPERIENCE" not in non_empty_sections:
        recommendations.append("Include more details about your work experience.")
    
    if "EDUCATION" not in non_empty_sections:
        recommendations.append("Ensure your education details are clearly listed.")
    
    if "PROJECTS" not in non_empty_sections:
        recommendations.append("Consider adding a Projects section to showcase your work.")
    
    if not github_links:
        recommendations.append("Add GitHub links to showcase your coding projects.")
    
    if len(non_empty_sections) < 5:
        recommendations.append(f"Your resume has only {len(non_empty_sections)} sections. Consider adding more sections like Summary, Certifications, or Languages.")
    
    # Display recommendations
    if recommendations:
        for rec in recommendations:
            st.warning(rec)
    else:
        st.success("Your resume looks good! No specific recommendations at this time.")

def display_pdf(file_content: bytes):
    """Display PDF content"""
    try:
        # Use io.BytesIO to read the file content
        file_content_io = io.BytesIO(file_content)
        
        # Open the PDF
        pdf_document = fitz.open(stream=file_content_io, filetype="pdf")
        
        # Display each page
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            st.image(img, use_column_width=True, caption=f"Page {page_num + 1}")
        
    except Exception as e:
        st.error(f"Error displaying PDF: {e}")

#Display the results table with action buttons
def display_results_table(results):
    # Create table header
    col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])

    with col1:
        st.markdown("**Name**")
    with col2:
        st.markdown("**Score**")
    with col3:
        st.markdown("**Experience**")
    with col4:
        st.markdown("**View PDF**")
    with col5:
        st.markdown("**Download PDF**")
    with col6:
        st.markdown("**Detailed Info**")

    st.markdown("---")  # Horizontal line

    # Create table with action buttons in columns
    for i, result in enumerate(results):
        col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])

        with col1:
            st.markdown(f"**{result['name']}**")
        with col2:
            st.markdown(f"{result['score']}")
        with col3:
            st.markdown("✅" if result['has_experience'] else "❌")
        with col4:
            if st.button("📄 View PDF", key=f"view_{i}", help=f"View {result['name']} PDF"):
                st.session_state["selected_resume"] = result['name']
                st.session_state["page"] = "view_pdf"
                st.rerun()
        with col5:
            st.download_button(
                label="⬇️ Download PDF",
                data=result['file_content'],
                file_name=result['name'],
                key=f"download_{i}",
                help=f"Download {result['name']} PDF",
            )
        with col6:
            if st.button("🔍 Details", key=f"details_{i}", help=f"View analysis details for {result['name']}"):
                st.session_state["selected_resume"] = result['name']
                st.session_state["page"] = "details"
                st.rerun()

        st.markdown("---")  # Horizontal line

def display_section_tabs(sections: Dict[str, str], resume_name: str):
    """Display resume sections in tabs"""
    # Filter out empty sections
    non_empty_sections = {k: v for k, v in sections.items() if v.strip()}
    
    if non_empty_sections:
        # Sort sections in a logical order
        section_order = [
            "BASIC_INFO", "SUMMARY", "CONTACT", "EDUCATION", "EXPERIENCE", 
            "SKILLS", "PROJECTS", "CERTIFICATIONS", "AWARDS", "PUBLICATIONS", 
            "LANGUAGES", "INTERESTS", "REFERENCES"
        ]
        
        # Create ordered list of sections that are present
        ordered_sections = [s for s in section_order if s in non_empty_sections]
        
        # Create tabs
        tabs = st.tabs(ordered_sections)
        for i, section in enumerate(ordered_sections):
            with tabs[i]:
                # Add a download button for each section
                section_content = non_empty_sections[section]
                section_filename = f"{resume_name}-{section}.txt"
                            
                # Display section content
                st.text_area(
                    "Content",
                    section_content,
                    height=200,
                    key=f"{resume_name}_{section}_content"
                )
    else:
        st.warning("No sections were extracted from the resume")
    
    return non_empty_sections

# def display_matched_items(result: Dict[str, Any], company_df: pd.DataFrame, 
#                          skills_df: pd.DataFrame, universities_df: pd.DataFrame):
#     """Display matched companies, skills, and universities"""
#     st.markdown("<h2 class='sub-header'>Matched Items</h2>", unsafe_allow_html=True)
    
#     # Companies
#     st.markdown("<h3>Companies</h3>", unsafe_allow_html=True)
#     if not result['company_matches'].empty:
#         # Merge with the full dataset to get all details
#         company_display = pd.merge(
#             result['company_matches'],
#             company_df,
#             on="Name",
#             how="left"
#         )
#         st.dataframe(company_display, use_container_width=True, key=f"{result['name']}_companies_df")
#     else:
#         st.info("No recognized companies found in your experience section")
    
#     # Skills
#     st.markdown("<h3>Skills</h3>", unsafe_allow_html=True)
#     if not result['skills_matches'].empty:
#         # Merge with the full dataset to get all details
#         skills_display = pd.merge(
#             result['skills_matches'],
#             skills_df,
#             on="Skill",
#             how="left"
#         )
#         st.dataframe(skills_display, use_container_width=True, key=f"{result['name']}_skills_df")
#     else:
#         st.info("No recognized skills found in your skills section")
    
#     # Universities
#     st.markdown("<h3>Universities</h3>", unsafe_allow_html=True)
#     if not result['university_matches'].empty:
#         # Merge with the full dataset to get all details
#         university_display = pd.merge(
#             result['university_matches'],
#             universities_df,
#             on="University",
#             how="left"
#         )
#         st.dataframe(university_display, use_container_width=True, key=f"{result['name']}_universities_df")
#     else:
#         st.info("No recognized universities found in your education section")

def page_upload(company_df: pd.DataFrame, skills_df: pd.DataFrame, universities_df: pd.DataFrame):
    """Handle upload page functionality"""
    st.markdown("<h1 class='main-header'>Resume Analyzer & Scorer</h1>", unsafe_allow_html=True)
    st.markdown("Upload your resume to get an analysis and score based on your education, skills, work experience, and more.")

    # Multiple file upload
    uploaded_files = st.file_uploader("Upload Resumes (PDF)", type="pdf", accept_multiple_files=True)
    
    if uploaded_files:
        # Save uploaded files
        for uploaded_file in uploaded_files:
            save_path = os.path.join("Resumes", uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        
        st.success(f"Uploaded {len(uploaded_files)} resumes successfully!")
        
        # Store uploaded files in session state
        st.session_state["uploaded_files"] = uploaded_files

    # Process resumes button
    if st.button("Process Resumes"):
        if "uploaded_files" in st.session_state and st.session_state["uploaded_files"]:
            # Clear previous results
            st.session_state["results"] = []
            
            # Process each resume
            with st.spinner("Processing resumes..."):
                for uploaded_file in st.session_state["uploaded_files"]:
                    resume_path = os.path.join("Resumes", uploaded_file.name)
                    
                    # Process the resume
                    score, sections, github_links = resume_parser.process_resume(
                        resume_path, company_df, skills_df, universities_df, read_resume.extract_text_and_links_from_pdf
                    )
                    
                    # Add to results
                    st.session_state["results"].append({
                        'name': uploaded_file.name,
                        'score': score,
                        'sections': sections,
                        'github_links': github_links,
                        'has_experience': bool(sections.get("EXPERIENCE", "").strip()),
                        'file_content': uploaded_file.getvalue()  # Store file content for later use
                    })
            
            # Change page to results
            st.session_state["page"] = "results"
            st.rerun()
        else:
            st.error("Please upload at least one resume.")

def page_results():
    """Handle results page functionality"""
    st.markdown("<h1>Resume Analyzer & Scorer - Results</h1>", unsafe_allow_html=True)

    # Check for results in session state
    if st.session_state["results"]:
        results = st.session_state["results"]
        
        # Sort results by score (highest first)
        results.sort(key=lambda x: x['score'], reverse=True)

        # Display results table
        display_results_table(results)

    else:
        st.error("No results available. Please upload and process resumes on the Upload page.")
    
    # Back button
    if st.button("⬅ Back to Upload"):
        st.session_state["page"] = "upload"
        st.rerun()

def page_view_pdf():
    """Handle PDF viewing page functionality"""
    resume_name = st.session_state["selected_resume"]
    if resume_name:
        # Find the resume in results
        result = next((r for r in st.session_state["results"] if r['name'] == resume_name), None)
        
        if result:
            st.markdown(f"<h1 class='main-header'>Viewing PDF: {resume_name}</h1>", unsafe_allow_html=True)
            
            # Add download button for the PDF
            file_content = result['file_content']
            st.markdown(
                create_download_button(resume_name, file_content),
                unsafe_allow_html=True
            )
            
            # Display PDF
            display_pdf(file_content)
        else:
            st.error(f"Resume '{resume_name}' not found in results.")
    else:
        st.error("No resume selected.")
    
    # Back button
    if st.button("⬅ Back to Results"):
        st.session_state["page"] = "results"
        st.rerun()

def page_details(company_df: pd.DataFrame, skills_df: pd.DataFrame, universities_df: pd.DataFrame):
    """Handle details page functionality"""
    resume_name = st.session_state["selected_resume"]
    if resume_name:
        # Find the resume in results
        result = next((r for r in st.session_state["results"] if r['name'] == resume_name), None)
        
        if result:
            st.markdown(f"<h1 class='main-header'>Resume Details: {resume_name}</h1>", unsafe_allow_html=True)
            
            # Add download button for the PDF
            file_content = result['file_content']
            
            # Display score
            st.markdown(f"<h2 class='sub-header'>Score: {result['score']}</h2>", unsafe_allow_html=True)
            
            # Display extracted sections using tabs
            st.markdown("<h2 class='sub-header'>Extracted Resume Sections</h2>", unsafe_allow_html=True)
            non_empty_sections = display_section_tabs(result['sections'], result['name'])
            
            # Display GitHub links
            if result['github_links']:
                display_github_links(result['github_links'], result['name'])
            
            # Display matched items
            # display_matched_items(result, company_df, skills_df, universities_df)
            
            # Provide recommendations
            display_recommendations(non_empty_sections, result['github_links'])
            
        else:
            st.error(f"Resume '{resume_name}' not found in results.")
    else:
        st.error("No resume selected.")
    
    # Back button
    if st.button("⬅ Back to Results"):
        st.session_state["page"] = "results"
        st.rerun()

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 36px;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #333;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .stButton button {
        background-color: #1E88E5;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton button:hover {
        background-color: #1976D2;
    }
    .results-table {
        margin-bottom: 30px;
    }
    .action-button {
        margin-right: 10px;
    }
    .view-button {
        background-color: #4CAF50 !important;
    }
    .details-button {
        background-color: #FF9800 !important;
    }
    .back-button {
        background-color: #9E9E9E !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "page" not in st.session_state:
    st.session_state["page"] = "upload"
if "selected_resume" not in st.session_state:
    st.session_state["selected_resume"] = None
if "results" not in st.session_state:
    st.session_state["results"] = []

# Main function
def main():
    # Load datasets
    company_df, skills_df, universities_df = load_datasets()
    
    # Page navigation based on session state
    page = st.session_state["page"]

    if page == "upload":
        page_upload(company_df, skills_df, universities_df)
    elif page == "results":
        page_results()
    elif page == "view_pdf":
        page_view_pdf()
    elif page == "details":
        page_details(company_df, skills_df, universities_df)

if __name__ == "__main__":
    main()
