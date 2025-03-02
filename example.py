#!/usr/bin/env python3
"""
Example script demonstrating how to use the sustainability report analyzer.
"""

import os
from extract_actions import process_report
from batch_process import batch_process
import utils


def single_report_example():
    """Example of processing a single report."""
    # Use the Apple report we downloaded
    pdf_path = "reports/apple.pdf"
    output_path = "results/apple_results.json"
    
    print("\n=== Processing Single Report ===")
    print(f"Input: {pdf_path}")
    print(f"Output: {output_path}")
    
    # Check if the example PDF exists
    if not os.path.exists(pdf_path):
        print(f"Example PDF not found at {pdf_path}")
        print("Please run download_sample_report.py first.")
        return
    
    # Limit to processing just 3 chunks to save API credits
    max_chunks = 3
    print(f"Note: Processing only {max_chunks} chunks to save API credits. Modify max_chunks in the code to process more.")
    
    # Process the report
    results = process_report(pdf_path, output_path, verbose=True, max_chunks=max_chunks)
    
    # Print results
    actions = results.get("emission_reduction_actions", [])
    print(f"\nFound {len(actions)} carbon emission reduction actions:")
    
    for i, action in enumerate(actions, 1):
        print(f"{i}. {action.get('action', 'Unnamed Action')}")
        if action.get("impact"):
            print(f"   Impact: {action['impact']}")


def batch_processing_example():
    """Example of batch processing multiple reports."""
    # Use our reports directory with downloaded reports
    input_dir = "reports"
    output_dir = "results"
    
    print("\n=== Batch Processing Reports ===")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    
    # Check if there are any PDFs in the directory
    pdf_files = utils.get_pdf_files(input_dir)
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        print("Please run download_sample_report.py first.")
        return
    
    print(f"Found {len(pdf_files)} reports to process: {', '.join(os.path.basename(f) for f in pdf_files)}")
    
    # Limit to processing just 2 chunks per report to save API credits
    max_chunks = 2
    print(f"Note: Processing only {max_chunks} chunks per report to save API credits. Modify max_chunks in the code to process more.")
    
    # Process all reports
    batch_process(input_dir, output_dir, verbose=True, max_chunks=max_chunks)


def main():
    """Run the example."""
    print("Sustainability Report Analyzer - Example Usage")
    print("---------------------------------------------")
    
    # Choose which example to run
    choice = input("Run: (1) Single report example or (2) Batch processing example? [1/2]: ")
    
    if choice == "2":
        batch_processing_example()
    else:
        single_report_example()
    
    print("\nExample complete! Check the 'results' directory for output files.")


if __name__ == "__main__":
    main() 