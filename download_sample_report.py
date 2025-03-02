#!/usr/bin/env python3
"""
Download a sample sustainability report for testing.
"""

import os
import requests
from tqdm import tqdm
import utils

# Sample sustainability report URLs
SAMPLE_REPORTS = {
    "apple": "https://www.apple.com/environment/pdf/Apple_Environmental_Progress_Report_2023.pdf",
    "microsoft": "https://query.prod.cms.rt.microsoft.com/cms/api/am/binary/RE5bNuP",  # Microsoft 2022 Environmental Sustainability Report
}

def download_file(url, destination):
    """
    Download a file with progress bar.
    
    Args:
        url: URL to download
        destination: Where to save the file
    """
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    print(f"Downloading to {destination}...")
    
    with open(destination, 'wb') as file, tqdm(
        desc=os.path.basename(destination),
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

def main():
    """Main function to download sample reports."""
    print("Downloading sample sustainability reports for testing...")
    
    # Create reports directory
    utils.ensure_directory("reports")
    
    # Download each report
    for company, url in SAMPLE_REPORTS.items():
        destination = f"reports/{company}.pdf"
        if os.path.exists(destination):
            print(f"{destination} already exists. Skipping download.")
            continue
        
        try:
            download_file(url, destination)
            print(f"Successfully downloaded {company} report.")
        except Exception as e:
            print(f"Failed to download {company} report: {str(e)}")
    
    print("\nDownload complete!")
    print("You can now run the example.py script to analyze these reports.")

if __name__ == "__main__":
    main() 