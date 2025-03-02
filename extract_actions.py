#!/usr/bin/env python3
"""
Extract carbon emission reduction actions from a sustainability report.
"""

import os
import argparse
import json
from typing import Dict, Any
from tqdm import tqdm
from dotenv import load_dotenv

from pdf_processor import PDFProcessor
from gemini_client import GeminiClient
import utils


def process_report(pdf_path: str, output_path: str = None, verbose: bool = False, max_chunks: int = None) -> Dict[str, Any]:
    """
    Process a sustainability report to extract emission reduction actions.
    
    Args:
        pdf_path: Path to the PDF report
        output_path: Path to save the results (optional)
        verbose: Whether to print progress information
        max_chunks: Maximum number of chunks to process (for testing/budget reasons)
        
    Returns:
        Dict containing the extracted actions
    """
    if verbose:
        print(f"Processing report: {pdf_path}")
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not found. Please set it in your .env file.")
    
    # Create processor instances
    pdf_processor = PDFProcessor(chunk_size=50000, overlap=1000)  # Reduced chunk size for better compatibility
    gemini_client = GeminiClient(api_key=api_key, model_name="models/gemini-2.0-flash")
    
    # Define prompt template for extraction
    prompt_template = """
    You are an expert in environmental sustainability and corporate reporting.
    Your task is to analyze text from sustainability reports and extract specific actions
    companies are taking to reduce their carbon emissions.
    
    Focus only on concrete actions or initiatives the company is implementing to reduce emissions.
    Do not include general statements about climate change, sustainability goals without specific actions,
    or actions that don't directly impact emissions.
    
    Format your response STRICTLY as a valid JSON array with the following structure for each action:
    [
        {
            "action": "Brief description of the action",
            "details": "More detailed explanation if available",
            "impact": "Quantified impact if mentioned (e.g., '20% reduction in emissions')",
            "timeline": "Implementation timeline if mentioned",
            "status": "current/planned/completed"
        }
    ]
    
    If no actions are found, return an empty array: []
    
    Do not include any explanatory text, headers, or comments before or after the JSON.
    The entire response should be valid JSON that can be parsed with json.loads().
    
    Here is the text to analyze:
    
    {TEXT_CHUNK}
    """
    
    # Extract text from PDF
    pdf_data = pdf_processor.process_pdf(pdf_path)
    company_name = pdf_data["company"]
    
    if "error" in pdf_data:
        print(f"Error processing {company_name} report: {pdf_data['error']}")
        return {"company": company_name, "error": pdf_data["error"]}
    
    # Process each chunk with Gemini
    results = []
    chunks = pdf_data["text_chunks"]
    
    # Limit number of chunks if specified
    if max_chunks and max_chunks > 0:
        chunks = chunks[:max_chunks]
        if verbose:
            print(f"Processing {len(chunks)} of {pdf_data['total_chunks']} text chunks (limited by max_chunks)...")
    else:
        if verbose:
            print(f"Processing {len(chunks)} text chunks...")
    
    for i, chunk in enumerate(tqdm(chunks, disable=not verbose)):
        chunk_result = gemini_client.extract_emission_actions(chunk, prompt_template)
        results.append(chunk_result)
    
    # Merge results from all chunks
    final_results = gemini_client.merge_results(results)
    final_results["company"] = company_name
    final_results["source_file"] = pdf_path
    final_results["chunks_processed"] = len(chunks)
    final_results["total_chunks"] = pdf_data["total_chunks"]
    
    # Save results if output path provided
    if output_path:
        utils.save_json(final_results, output_path)
        
        # Also save a formatted summary
        summary_path = output_path.replace(".json", "_summary.md")
        summary = utils.format_report_summary(final_results, company_name)
        
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
    
    if verbose:
        action_count = len(final_results.get("emission_reduction_actions", []))
        print(f"Found {action_count} unique emission reduction actions for {company_name}")
    
    return final_results


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Extract carbon emission reduction actions from a sustainability report"
    )
    parser.add_argument("--input", "-i", required=True, help="Path to the PDF report")
    parser.add_argument("--output", "-o", help="Path to save the results JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print progress information")
    parser.add_argument("--max-chunks", "-m", type=int, default=3, 
                       help="Maximum number of chunks to process (for testing/budget reasons)")
    
    args = parser.parse_args()
    
    # Determine output path if not provided
    if not args.output:
        basename = os.path.basename(args.input)
        company_name = os.path.splitext(basename)[0]
        args.output = f"results/{company_name}_results.json"
    
    # Process the report
    results = process_report(args.input, args.output, args.verbose, args.max_chunks)
    
    # Print summary
    action_count = len(results.get("emission_reduction_actions", []))
    print(f"\nExtracted {action_count} carbon emission reduction actions")
    print(f"Results saved to: {args.output}")


if __name__ == "__main__":
    main() 