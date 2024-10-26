import requests
import json
from datetime import datetime
from typing import Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class WebScraperAgent:
    def __init__(self, store_profiles: Dict):
        self.store_profiles = store_profiles
        self.scraper_url = "http://127.0.0.1:8000/execute_task"
        
    def _extract_json_from_line(self, line: str) -> Optional[Dict]:
        """Extract JSON from a line prefixed with 'data: '"""
        prefix = "data: "
        if line.startswith(prefix):
            json_str = line[len(prefix):].strip()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON in line: {line}\nError: {e}")
        return None

    def _execute_single_command(self, command: str) -> Optional[Dict]:
        """Execute a single command and handle streaming response"""
        payload = {
            "command": command
        }
        headers = {
            "Content-Type": "application/json"
        }

        try:
            with requests.post(self.scraper_url, headers=headers, json=payload, stream=True) as response:
                response.raise_for_status()

                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        print(f"Raw response line for command '{command}': {line}")
                        json_obj = self._extract_json_from_line(line)
                        if json_obj and json_obj.get("type") == "answer":
                            return json_obj

                print(f"No 'answer' type message found for command: {command}")
                
        except requests.exceptions.RequestException as e:
            print(f"HTTP Request failed for command '{command}': {e}")
        except Exception as e:
            print(f"Unexpected error for command '{command}': {e}")

        return None

    def _generate_store_specific_commands(self, store_info: Dict) -> list:
        """Generate relevant commands based on store characteristics"""
        location = store_info['location']
        categories = store_info['popular_categories']
        demographic = store_info['demographic']
        
        commands = []
        
        # Location-based queries
        commands.append(f"Find current events and festivals happening in {location}")
        commands.append(f"Search for major construction or road work in {location}")
        
        # Category and demographic specific queries
        if demographic == "office workers":
            commands.extend([
                f"Search for office occupancy rates in {location}",
                f"Find popular lunch spots and food delivery trends in {location}"
            ])
            for category in categories:
                commands.append(f"Find popular {category} options near office areas in {location}")
        
        elif demographic == "students":
            commands.extend([
                f"Search for university events in {location}",
                f"Find student discounts and deals in {location}"
            ])
            for category in categories:
                commands.append(f"Find popular {category} among students in {location}")
        
        elif demographic == "high-income families":
            commands.extend([
                f"Search for luxury retail trends in {location}",
                f"Find premium shopping events in {location}"
            ])
            for category in categories:
                commands.append(f"Find high-end {category} trends in {location}")
        
        elif demographic == "families":
            commands.extend([
                f"Search for family events in {location}",
                f"Find school schedules and events in {location}"
            ])
            for category in categories:
                commands.append(f"Find family-friendly {category} trends in {location}")
        
        # Add weather and traffic queries for all stores
        commands.extend([
            f"Check weather forecast for {location} next 7 days",
            f"Find peak traffic hours in {location}"
        ])
        
        return commands

    def analyze_local_factors(self) -> Dict:
        """Analyze local factors for all stores"""
        all_store_factors = {}
        
        for store_id, store_info in self.store_profiles.items():
            print(f"\nAnalyzing local factors for store {store_id}: {store_info['name']}")
            store_results = []
            
            # Generate commands for this store
            commands = self._generate_store_specific_commands(store_info)
            
            # Execute each command and collect results
            for command in commands:
                print(f"\nExecuting command: {command}")
                result = self._execute_single_command(command)
                
                store_results.append({
                    "command": command,
                    "result": result if result else {"error": "No valid response received"}
                })
            
            # Store results for this store
            all_store_factors[store_id] = {
                "store_info": store_info,
                "local_factors": store_results,
                "timestamp": datetime.now().isoformat()
            }
        
        return all_store_factors

def run_web_scraper_analysis(store_profiles: Dict) -> Dict:
    """Run the complete web scraper analysis"""
    print("Starting web scraper analysis...")
    
    scraper = WebScraperAgent(store_profiles)
    factors = scraper.analyze_local_factors()
    
    # Save results
    print("\nSaving web scraper results to web_scraper_insights.json...")
    with open('web_scraper_insights.json', 'w') as f:
        json.dump(factors, f, indent=4)
    
    print("Web scraper analysis complete!")
    return factors

if __name__ == "__main__":
    # Example usage with a single store profile
    test_profile = {
        1: {
            "name": "Test Store",
            "location": "Manhattan",
            "demographic": "office workers",
            "popular_categories": ["lunch", "snacks"]
        }
    }
    
    results = run_web_scraper_analysis(test_profile)
    print("\nTest results:", json.dumps(results, indent=4))