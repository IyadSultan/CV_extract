import pandas as pd
import os

def filter_and_save_high_scores(input_csv: str, output_md: str, min_score: float = 8.0):
    """
    Filter resumes with high scores and save them to a markdown file
    
    Args:
        input_csv: Path to the input CSV file
        output_md: Path to the output markdown file
        min_score: Minimum score to include (default: 8.0)
    """
    # Read the CSV file
    df = pd.read_csv(input_csv)
    
    # Filter for high scores
    high_scores = df[df['overall_fit_score'] >= min_score].sort_values(
        by='overall_fit_score', 
        ascending=False
    )
    
    # Create markdown content
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(f"# Top Candidates (Score >= {min_score})\n\n")
        
        for _, row in high_scores.iterrows():
            f.write(f"## {row['name']} (Score: {row['overall_fit_score']})\n\n")
            
            f.write("### 👤 Contact Information\n\n")
            f.write(f"- **Email:** {row['email']}\n")
            f.write(f"- **Phone:** {row['phone']}\n\n")
            
            f.write("### 🔧 Technical Skills\n\n")
            f.write(f"- **Python Experience:** {row['python_experience']}\n")
            f.write(f"- **Other Languages:** {row['other_languages']}\n")
            f.write(f"- **Django Experience:** {row['django_experience']}\n")
            f.write(f"- **SQL Experience:** {row['sql_experience']}\n")
            f.write(f"- **Azure Experience:** {row['azure_experience']}\n")
            f.write(f"- **AWS Experience:** {row['aws_experience']}\n")
            
            if pd.notna(row['github_repos']):
                f.write(f"- **GitHub Repos:** {row['github_repos']}\n")
            if pd.notna(row['github_profile']):
                f.write(f"- **GitHub Profile:** {row['github_profile']}\n")
            
            f.write("\n### 🔗 Social Links\n\n")
            if pd.notna(row['linkedin_url']):
                f.write(f"- [LinkedIn Profile]({row['linkedin_url']})\n")
            if pd.notna(row['github_url']):
                f.write(f"- [GitHub Profile]({row['github_url']})\n")
            
            f.write("\n### 🎓 Education\n\n")
            if pd.notna(row['bachelors']):
                f.write(f"- **Bachelor's:** {row['bachelors']}\n")
            if pd.notna(row['masters']):
                f.write(f"- **Master's:** {row['masters']}\n")
            if pd.notna(row['phd']):
                f.write(f"- **PhD:** {row['phd']}\n")
            if pd.notna(row['awards']):
                f.write(f"- **Awards:** {row['awards']}\n")
            
            f.write("\n### 💼 Experience\n\n")
            if pd.notna(row['data_science_experience']):
                f.write(f"- **Data Science Experience:** {row['data_science_experience']}\n")
            if pd.notna(row['healthcare_experience']):
                f.write(f"- **Healthcare Experience:** {row['healthcare_experience']}\n")
            if pd.notna(row['total_years']):
                f.write(f"- **Total Years:** {row['total_years']}\n")
            if pd.notna(row['important_projects']):
                f.write("\n**Key Projects:**\n")
                projects = row['important_projects'].split(',')
                for project in projects:
                    f.write(f"- {project.strip()}\n")
            
            f.write(f"\n### 🎯 Fit Assessment\n\n")
            f.write(f"**Score:** {row['overall_fit_score']}/10\n\n")
            f.write(f"**Justification:** {row['fit_justification']}\n\n")
            
            f.write("---\n\n")
        
        # Add summary at the end
        f.write(f"\n## Summary\n\n")
        f.write(f"Total candidates with score >= {min_score}: {len(high_scores)}\n")
        f.write(f"Average score of top candidates: {high_scores['overall_fit_score'].mean():.2f}\n")

def main():
    # Input and output files
    input_csv = 'results/resume_analysis_results_docx_pdf.csv'
    output_md = 'results/top_candidates.md'
    
    # Create results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    
    # Filter and save results
    filter_and_save_high_scores(input_csv, output_md)
    print(f"Top candidates have been saved to {output_md}")

if __name__ == "__main__":
    main() 