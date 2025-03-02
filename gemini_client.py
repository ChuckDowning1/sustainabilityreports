"""
Gemini client module for interacting with Google's Gemini model.
"""

import os
import json
from typing import List, Dict, Any, Optional
import re
from tqdm import tqdm
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiClient:
    """Client for interacting with Google's Gemini API for sustainability report analysis."""
    
    def __init__(self, api_key: str, model_name: str = "models/gemini-2.0-flash"):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Google API key for authentication
            model_name: Name of the Gemini model to use
        """
        # Configure the API with the provided API key
        genai.configure(api_key=api_key)
        
        # Initialize the model with appropriate settings
        generation_config = {
            "temperature": 0.2,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192
        }
        
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
        
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # Store parameters
        self.model_name = model_name
    
    def extract_emission_actions(self, text_chunk: str, prompt_template: str) -> List[Dict[str, Any]]:
        """
        Extract carbon emission reduction actions from a text chunk using the Gemini API.
        
        Args:
            text_chunk: A chunk of text from a sustainability report
            prompt_template: The prompt template to use for extraction
            
        Returns:
            A list of dictionaries containing the extracted actions
        """
        # Create the prompt by inserting the text chunk into the template
        prompt = prompt_template.replace("{TEXT_CHUNK}", text_chunk)
        
        try:
            # Generate content using the Gemini model
            response = self.model.generate_content(prompt)
            
            # Extract and parse the JSON response
            response_text = response.text
            
            # Find the JSON content in the response (it might be wrapped in ```json ... ```)
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response_text)
            if json_match:
                json_str = json_match.group(1).strip()
            else:
                json_str = response_text.strip()
            
            # Handle empty responses
            if not json_str or json_str == "[]":
                return []
                
            # Parse the JSON
            try:
                actions = json.loads(json_str)
                
                # Make sure we have a list
                if not isinstance(actions, list):
                    if isinstance(actions, dict) and "actions" in actions:
                        actions = actions["actions"]
                    elif isinstance(actions, dict):
                        actions = [actions]
                
                return actions
                
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                # Try more aggressive parsing by extracting JSON-like content
                json_pattern = re.search(r'(\[[\s\S]*\])', json_str, re.DOTALL)
                if json_pattern:
                    try:
                        extracted_json = json_pattern.group(1)
                        actions = json.loads(extracted_json)
                        
                        if not isinstance(actions, list):
                            if isinstance(actions, dict) and "actions" in actions:
                                actions = actions["actions"]
                            elif isinstance(actions, dict):
                                actions = [actions]
                        
                        return actions
                    except:
                        pass
                
                return []
                
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return []
    
    def merge_results(self, results: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Merge results from multiple chunks, eliminating duplicates.
        
        Args:
            results: List of results from each chunk
            
        Returns:
            Merged results with duplicate actions removed
        """
        # Flatten all actions from all chunks
        all_actions = []
        for chunk_result in results:
            all_actions.extend(chunk_result)
        
        # Use a set to track unique actions by their description to eliminate duplicates
        unique_actions = {}
        for action in all_actions:
            # Skip if no action field
            if not action.get("action"):
                continue
                
            action_key = action.get("action", "").strip().lower()
            if action_key and action_key not in unique_actions:
                unique_actions[action_key] = action
            elif action_key:
                # If we have a duplicate, keep the one with more details
                existing = unique_actions[action_key]
                if (action.get("details") and not existing.get("details")) or \
                   (action.get("impact") and not existing.get("impact")) or \
                   (action.get("timeline") and not existing.get("timeline")):
                    unique_actions[action_key] = {**existing, **{k: v for k, v in action.items() if v and not existing.get(k)}}
        
        # Convert back to list
        final_actions = list(unique_actions.values())
        
        return {
            "emission_reduction_actions": final_actions,
            "total_unique_actions": len(final_actions)
        } 