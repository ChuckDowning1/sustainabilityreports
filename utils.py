"""
Utility functions for the sustainability report analyzer.
"""

import os
import json
from typing import Dict, Any, List
import datetime


def ensure_directory(directory_path: str) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory_path: Path to the directory
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def save_json(data: Dict[str, Any], file_path: str) -> None:
    """
    Save data as a JSON file.
    
    Args:
        data: Data to save
        file_path: Path to save the file
    """
    ensure_directory(os.path.dirname(file_path))
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(file_path: str) -> Dict[str, Any]:
    """
    Load data from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary containing the loaded data
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_pdf_files(directory: str) -> List[str]:
    """
    Get all PDF files in a directory.
    
    Args:
        directory: Directory to search
        
    Returns:
        List of paths to PDF files
    """
    pdf_files = []
    
    for filename in os.listdir(directory):
        if filename.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(directory, filename))
    
    return pdf_files


def format_report_summary(data: Dict[str, Any], company_name: str) -> str:
    """
    Format the emission reduction actions for display.
    
    Args:
        data: The results data
        company_name: Name of the company
        
    Returns:
        Formatted summary text
    """
    actions = data.get("emission_reduction_actions", [])
    
    if not actions:
        return f"No emission reduction actions found for {company_name}."
    
    summary = [f"# Carbon Emission Reduction Actions for {company_name}"]
    summary.append(f"Extracted on: {datetime.datetime.now().strftime('%Y-%m-%d')}")
    summary.append(f"Total actions found: {len(actions)}")
    summary.append("\n## Actions:")
    
    for i, action in enumerate(actions, 1):
        summary.append(f"\n### {i}. {action.get('action', 'Unnamed Action')}")
        
        if action.get("details"):
            summary.append(f"**Details**: {action['details']}")
        
        if action.get("impact"):
            summary.append(f"**Impact**: {action['impact']}")
        
        if action.get("timeline"):
            summary.append(f"**Timeline**: {action['timeline']}")
        
        if action.get("status"):
            summary.append(f"**Status**: {action['status']}")
    
    return "\n".join(summary) 