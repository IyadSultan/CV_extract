# Resume Analysis System

A comprehensive system for analyzing resumes in both PDF and Word document formats, extracting key information, and generating detailed analysis reports.

## Features

- **Multi-format Support**: Process both PDF and Word documents (`.pdf`, `.docx`, `.doc`)
- **Intelligent Text Extraction**:
  - PDF processing using LlamaParse
  - Word document processing using python-docx
- **Comprehensive Analysis**:
  - Contact information extraction
  - Technical skills assessment
  - Education history analysis
  - Experience evaluation
  - Project analysis
  - Overall fit scoring
- **Output Formats**:
  - Detailed Markdown reports
  - CSV format for data analysis
  - Filtered reports for top candidates

## Prerequisites

```bash
pip install -r requirements.txt
```

Required packages:
- python-docx
- llama-parse
- pandas
- pydantic
- pydantic-ai
- python-dotenv
- nest-asyncio

## Environment Setup

1. Create a `.env` file in the root directory
2. Add your API keys:
```env
OPENAI_API_KEY=your_openai_api_key
LLAMA_CLOUD_API_KEY=your_llama_cloud_api_key
```

## Directory Structure

```
├── main.py                     # Main resume processing script
├── filter_high_scores.py       # Script for filtering top candidates
├── results/                    # Output directory
│   ├── resume_analysis_results.md
│   ├── resume_analysis_results.csv
│   └── top_candidates.md
├── CVs/                       # Directory containing resumes
│   └── cv_leads/             # Subdirectory for resumes
└── requirements.txt
```

## Usage

### 1. Processing Resumes

Run the main script to process all resumes:

```bash
python main.py
```

This will:
- Process all PDF and Word documents in the specified directory
- Generate detailed analysis for each resume
- Save results in both markdown and CSV formats
- Create a results directory if it doesn't exist

### 2. Filtering Top Candidates

After processing resumes, run the filtering script:

```bash
python filter_high_scores.py
```

This will:
- Read the CSV results file
- Filter candidates with scores >= 8.0
- Generate a new markdown file with detailed information about top candidates
- Include a summary of the filtering results

## Analysis Components

### Resume Analysis

The system analyzes the following aspects:

1. **Contact Information**:
   - Full name
   - Email address
   - Phone number

2. **Technical Skills**:
   - Python experience and frameworks
   - Other programming languages
   - Django experience
   - SQL proficiency
   - Cloud platform experience (Azure, AWS)
   - GitHub repositories and profiles

3. **Education**:
   - Degrees (Bachelor's, Master's, PhD)
   - Universities and graduation years
   - Awards and certifications

4. **Experience**:
   - Years of relevant experience
   - Data science projects
   - Healthcare industry experience
   - Leadership roles

5. **Scoring System**:
   - Technical expertise (40%)
   - Relevant experience (30%)
   - Education (20%)
   - Leadership potential (10%)

### Output Formats

1. **Markdown Report** (`resume_analysis_results.md`):
   - Detailed analysis for each candidate
   - Formatted sections with emojis
   - Easy to read and share

2. **CSV File** (`resume_analysis_results.csv`):
   - Structured data format
   - Easy to import into other tools
   - Suitable for further analysis

3. **Top Candidates Report** (`top_candidates.md`):
   - Filtered view of best candidates
   - Sorted by score
   - Summary statistics

## Error Handling

The system includes:
- Retry logic for API calls
- Graceful handling of missing data
- Error reporting for failed processing
- File format validation

## Customization

### Adjusting Score Threshold

In `filter_high_scores.py`, modify the `min_score` parameter:

```python
filter_and_save_high_scores(input_csv, output_md, min_score=7.0)  # Change to desired threshold
```

### Modifying Output Directory

In both scripts, update the output paths:

```python
markdown_file = 'your/custom/path/results.md'
csv_file = 'your/custom/path/results.csv'
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- LlamaParse for PDF processing
- python-docx for Word document processing
- Pandas for data manipulation 