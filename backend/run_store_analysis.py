from agents.enhanced_prediction_agent import run_enhanced_prediction_analysis, PopulationAnalyzer
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import shutil
import re

def clear_autogen_cache():
    """Clear AutoGen chat cache and workspace"""
    workspace_dir = "analysis_workspace"
    if os.path.exists(workspace_dir):
        shutil.rmtree(workspace_dir)
        print("Cleared AutoGen workspace")
    
    cache_dir = os.path.expanduser("~/.cache/autogen")
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        print("Cleared AutoGen cache")

def load_json_file(filename: str) -> dict:
    """Load and validate JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Required file {filename} not found!")
        raise
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filename}!")
        raise

def extract_store_locations(historical_insights: dict) -> dict:
    """Extract store locations with proper mapping"""
    store_locations = {}
    
    # Mapping that matches the PopulationAnalyzer's nyc_demographic_patterns
    location_map = {
        "1": {
            "location": "Financial District, Manhattan",
            "type": "young_professionals"
        },
        "2": {
            "location": "Upper East Side, Manhattan",
            "type": "affluent_families"
        },
        "3": {
            "location": "Greenwich Village, Manhattan",
            "type": "students"
        },
        "4": {
            "location": "Park Slope, Brooklyn",
            "type": "families"
        },
        "5": {
            "location": "Chelsea, Manhattan",
            "type": "mixed"
        },
        "6": {
            "location": "Upper West Side, Manhattan",
            "type": "young_professionals"
        }
    }
    
    for store_id in historical_insights.keys():
        store_locations[int(store_id)] = location_map.get(str(store_id), {
            "location": "Manhattan",  # Default location
            "type": "mixed"
        })
    
    return store_locations

def analyze_population_trends(store_locations: dict) -> dict:
    """Analyze population trends for all locations"""
    analyzer = PopulationAnalyzer()
    population_insights = {}
    
    for store_id, location_info in store_locations.items():
        print(f"\nAnalyzing population trends for store {store_id}...")
        location = location_info['location']
        trends = analyzer.analyze_location_trends(location)
        population_insights[store_id] = trends
    
    return population_insights

def run_complete_analysis():
    """Load existing files and generate predictions with population analysis"""
    print("Starting complete market analysis...")
    
    # Clear AutoGen cache
    clear_autogen_cache()
    
    try:
        # Load existing JSON files
        print("\nLoading historical insights...")
        historical_insights = load_json_file('dark_store_insights.json')
        
        print("Loading scraper insights...")
        scraper_insights = load_json_file('web_scraper_insights.json')
        
        # Extract store locations and analyze population trends
        store_locations = extract_store_locations(historical_insights)
        
        print("\nAnalyzing population trends...")
        population_insights = analyze_population_trends(store_locations)
        
        # Generate predictions
        print("\nGenerating enhanced predictions...")
        predictions = run_enhanced_prediction_analysis(
            historical_insights=historical_insights,
            local_factors=scraper_insights,
            store_locations=store_locations
        )
        
        # Save predictions separately
        print("\nSaving predictions...")
        with open('enhanced_store_predictions.json', 'w') as f:
            json.dump(predictions, f, indent=4)
        
        # Save population insights
        print("\nSaving population insights...")
        with open('population_insights.json', 'w') as f:
            json.dump(population_insights, f, indent=4)
        
        # Create final report
        final_report = {
            'historical_analysis': historical_insights,
            'local_factors': scraper_insights,
            'population_insights': population_insights,
            'predictions': predictions,
            'timestamp': datetime.now().isoformat(),
            'metadata': {
                'version': '1.0',
                'analysis_type': 'complete_market_analysis',
                'source': 'combined_analysis'
            }
        }
        
        # Save final report
        print("\nSaving final report...")
        with open('final_market_analysis.json', 'w') as f:
            json.dump(final_report, f, indent=4)
        
        print("\nComplete market analysis finished successfully!")
        return final_report
        
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        raise

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Ensure API key is set
    if not os.getenv("AUTOGEN_MODEL_API_KEY"):
        print("Error: AUTOGEN_MODEL_API_KEY not found in environment variables!")
        exit(1)
    
    try:
        # Run the analysis
        insights = run_complete_analysis()
    except FileNotFoundError:
        print("\nError: Make sure required JSON files exist:")
        print("- dark_store_insights.json")
        print("- web_scraper_insights.json")
        exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        exit(1)