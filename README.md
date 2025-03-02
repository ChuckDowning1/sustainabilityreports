# Sustainability Reports Analyzer

This project analyzes corporate sustainability reports to extract actions companies are taking to reduce their carbon emissions. It uses Google's Gemini model to process text and provide structured insights.

## Features

- Extract specific carbon emission reduction actions from PDF sustainability reports
- Process individual reports or batch-process multiple reports
- Generate structured JSON output with action details
- Create markdown summaries of findings
- Control processing depth to manage API usage

## Setup

### Prerequisites

- Python 3.8 or higher
- Google AI Studio API key (see below)
- PDF sustainability reports to analyze

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/ChuckDowning1/sustainabilityreports.git
   cd sustainabilityreports
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Get a Google API key:
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create or sign in to your Google account
   - Create a new API key
   - Copy the key for the next step

4. Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

5. Download sample reports (or add your own to the `reports` folder):
   ```
   python download_sample_report.py
   ```

## Usage

### Quick Start with Example Script

Run the example script to test the functionality:

```
python example.py
```

This interactive script allows you to:
- Process a single report (Apple's sustainability report)
- Batch process all reports in the `reports` directory
- View extracted carbon emission reduction actions

### Process a Single Report

```
python extract_actions.py --input reports/company_report.pdf --output results/company_results.json --verbose
```

Options:
- `--input`, `-i`: Path to the PDF report (required)
- `--output`, `-o`: Path to save the results (optional)
- `--verbose`, `-v`: Print progress information
- `--max-chunks`, `-m`: Maximum number of chunks to process (default: 3)

### Batch Process Multiple Reports

```
python batch_process.py --input_dir reports/ --output_dir results/ --verbose
```

Options:
- `--input_dir`, `-i`: Directory containing PDF reports (required)
- `--output_dir`, `-o`: Directory to save results (default: results/)
- `--verbose`, `-v`: Print detailed progress information
- `--max-chunks`, `-m`: Maximum number of chunks to process per report (default: 3)

## Output

The tool generates two types of output files for each processed report:

1. JSON file with structured data:
   - List of unique emission reduction actions
   - Details, impact, timeline, and status for each action
   - Metadata about the processing

2. Markdown summary file:
   - Formatted list of all actions
   - Impact information when available
   - Easy-to-read format for presentations or sharing

## Project Structure

- `extract_actions.py`: Main script for processing a single report
- `batch_process.py`: Process multiple reports in a directory
- `example.py`: Interactive example script
- `pdf_processor.py`: Handles reading and processing PDF files
- `gemini_client.py`: Manages interactions with the Gemini API
- `utils.py`: Utility functions
- `download_sample_report.py`: Downloads example reports

## Troubleshooting

- **API Key Issues**: Ensure your `.env` file contains a valid Google API key
- **PDF Processing Errors**: Check that the PDF is not password-protected
- **JSON Parsing Errors**: The model may occasionally return improperly formatted responses; try processing the report again

## GitHub Repository

This project is available on GitHub at [ChuckDowning1/sustainabilityreports](https://github.com/ChuckDowning1/sustainabilityreports).

## License

This project is licensed under the MIT License - see the LICENSE file for details. 