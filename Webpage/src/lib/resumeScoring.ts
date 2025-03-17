import { supabase } from './supabase';

export async function scoreResume(resumeUrl: string): Promise<number> {
  try {
    // Download the resume from Supabase storage
    const { data: fileData, error: downloadError } = await supabase.storage
      .from('resumes')
      .download(resumeUrl);

    if (downloadError) throw downloadError;

    // Convert the file to text
    const text = await fileData.text();
    
    // Basic scoring criteria
    let score = 0;
    
    // Check for GitHub links
    const githubLinkPattern = /https:\/\/github\.com\/[a-zA-Z0-9-_]+\/[a-zA-Z0-9-_]+/g;
    const githubLinks = text.match(githubLinkPattern) || [];
    score += githubLinks.length * 10; // 10 points per GitHub project
    
    // Check for common keywords
    const keywords = [
      'javascript', 'typescript', 'python', 'react', 'node', 'express',
      'database', 'api', 'rest', 'graphql', 'aws', 'cloud', 'docker',
      'kubernetes', 'ci/cd', 'testing', 'agile', 'scrum'
    ];
    
    keywords.forEach(keyword => {
      const regex = new RegExp(keyword, 'gi');
      const matches = text.match(regex) || [];
      score += matches.length * 5; // 5 points per keyword match
    });
    
    // Normalize score to be between 0 and 100
    return Math.min(100, score);
  } catch (error) {
    console.error('Error scoring resume:', error);
    return 0;
  }
}