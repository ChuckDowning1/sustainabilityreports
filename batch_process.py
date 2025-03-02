#!/usr/bin/env python3
"""
Batch process multiple sustainability reports to extract carbon emission reduction actions.
"""

import os
import argparse
import time
from typing import List, Dict, Any
from tqdm import tqdm

from extract_actions import process_report
import utils


def batch_process(input_dir: str, output_dir: str, verbose: bool = False, max_chunks: int = None) -> List[Dict[str, Any]]:
    """
    Process all PDF reports in a directory.
    
    Args:
        input_dir: Directory containing PDF reports
        output_dir: Directory to save results
        verbose: Whether to print progress information
        max_chunks: Maximum number of chunks to process per report
        
    Returns:
        List of results for each report
    """
    # Create output directory if it doesn't exist
    utils.ensure_directory(output_dir)
    
    # Get all PDF files in the input directory
    pdf_files = utils.get_pdf_files(input_dir)
    
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return []
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    # Process each report
    all_results = []
    
    for pdf_path in tqdm(pdf_files, desc="Processing reports"):
        # Extract company name from filename
        basename = os.path.basename(pdf_path)
        company_name = os.path.splitext(basename)[0]
        
        # Define output path
        output_path = os.path.join(output_dir, f"{company_name}_results.json")
        
        # Process the report
        try:
            result = process_report(pdf_path, output_path, verbose=verbose, max_chunks=max_chunks)
            all_results.append(result)
            
            # Add a small delay to avoid potential rate limiting
            time.sleep(2)
            
        except Exception as e:
            print(f"Error processing {pdf_path}: {str(e)}")
            all_results.append({
                "company": company_name,
                "error": str(e)
            })
    
    # Save a summary of all results
    summary_path = os.path.join(output_dir, "batch_summary.json")
    summary = {
        "total_reports": len(pdf_files),
        "successful_reports": sum(1 for r in all_results if "error" not in r),
        "failed_reports": sum(1 for r in all_results if "error" in r),
        "companies": [r.get("company") for r in all_results if "company" in r],
        "total_actions": sum(len(r.get("emission_reduction_actions", [])) for r in all_results)
    }
    
    utils.save_json(summary, summary_path)
    
    # Print summary
    print(f"\nProcessed {summary['total_reports']} reports")
    print(f"Successful: {summary['successful_reports']}")
    print(f"Failed: {summary['failed_reports']}")
    print(f"Total actions found: {summary['total_actions']}")
    print(f"Summary saved to: {summary_path}")
    
    return all_results


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Batch process sustainability reports to extract carbon emission reduction actions"
    )
    parser.add_argument("--input_dir", "-i", required=True, help="Directory containing PDF reports")
    parser.add_argument("--output_dir", "-o", default="results", help="Directory to save results")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed progress information")
    parser.add_argument("--max-chunks", "-m", type=int, default=3, 
                       help="Maximum number of chunks to process per report (for testing/budget reasons)")
    
    args = parser.parse_args()
    
    # Process all reports
    batch_process(args.input_dir, args.output_dir, args.verbose, args.max_chunks)


if __name__ == "__main__":
    main() 