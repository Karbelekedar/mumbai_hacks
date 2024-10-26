import autogen
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

def sample_data(orders_df: pd.DataFrame, 
                order_products_df: pd.DataFrame,
                products_df: pd.DataFrame,
                sample_size: int = 1000) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Sample data while maintaining relationships between dataframes
    """
    print("Sampling data...")
    
    # Sample orders first
    sampled_orders = orders_df.sample(n=sample_size, random_state=42)
    
    # Get related order_products
    sampled_order_products = order_products_df[
        order_products_df['order_id'].isin(sampled_orders['order_id'])
    ]
    
    # Get related products
    sampled_products = products_df[
        products_df['product_id'].isin(sampled_order_products['product_id'])
    ]
    
    print(f"Sampled data sizes:")
    print(f"Orders: {len(sampled_orders)}")
    print(f"Order Products: {len(sampled_order_products)}")
    print(f"Products: {len(sampled_products)}")
    
    return sampled_orders, sampled_order_products, sampled_products

class DarkStoreDistributor:
    def __init__(self):
        self.store_profiles = {
            1: {
                "name": "Business District Hub",
                "location": "Financial District, Manhattan",  # 40.7075° N, 74.0021° W
                "peak_hours": [11, 12, 13, 14, 15],
                "demographic": "office workers",
                "popular_categories": ["prepared meals", "beverages", "snacks"]
            },
            2: {
                "name": "Premium Residential",
                "location": "Upper East Side, Manhattan",  # 40.7736° N, 73.9566° W
                "peak_hours": [9, 10, 17, 18, 19],
                "demographic": "high-income families",
                "popular_categories": ["organic", "premium", "specialty"]
            },
            3: {
                "name": "University Zone",
                "location": "Greenwich Village, Manhattan",  # 40.7320° N, 74.0027° W
                "peak_hours": [14, 15, 16, 20, 21, 22, 23],
                "demographic": "students",
                "popular_categories": ["snacks", "instant foods", "beverages"]
            },
            4: {
                "name": "Family Suburb",
                "location": "Park Slope, Brooklyn",  # 40.6710° N, 73.9766° W
                "peak_hours": [9, 10, 11, 17, 18, 19],
                "demographic": "families",
                "popular_categories": ["groceries", "household", "baby products"]
            },
            5: {
                "name": "Mixed Commercial",
                "location": "Chelsea, Manhattan",  # 40.7430° N, 74.0018° W
                "peak_hours": [10, 11, 12, 13, 14, 15, 16, 17],
                "demographic": "mixed",
                "popular_categories": ["mixed", "general", "convenience"]
            },
            6: {
                "name": "Urban Residential",
                "location": "Upper West Side, Manhattan",  # 40.7870° N, 73.9754° W
                "peak_hours": [18, 19, 20, 21],
                "demographic": "young professionals",
                "popular_categories": ["ready meals", "fresh produce", "convenience"]
            }
        }

    def assign_dark_store(self, order_row: pd.Series) -> int:
        """
        Assign a dark store to an order based on time and order characteristics
        """
        hour = order_row['order_hour_of_day']
        dow = order_row['order_dow']
        
        # Calculate probability for each store based on hour and day
        probabilities = []
        for store_id, profile in self.store_profiles.items():
            prob = 1.0
            
            # Higher probability during peak hours
            if hour in profile['peak_hours']:
                prob *= 2.0
                
            # Weekend adjustments
            if dow in [5, 6]:  # Weekend
                if profile['demographic'] in ['office workers']:
                    prob *= 0.5
                elif profile['demographic'] in ['families', 'mixed']:
                    prob *= 1.5
                    
            probabilities.append(prob)
            
        # Normalize probabilities
        probabilities = np.array(probabilities) / sum(probabilities)
        
        # Return assigned store ID (1-6)
        return np.random.choice(list(self.store_profiles.keys()), p=probabilities)

def prepare_historical_data(orders_df: pd.DataFrame, 
                          order_products_df: pd.DataFrame,
                          products_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Prepare historical data by assigning orders to dark stores and creating analysis
    """
    # Sample the data first
    sampled_orders, sampled_order_products, sampled_products = sample_data(
        orders_df, order_products_df, products_df
    )
    
    # Initialize distributor
    distributor = DarkStoreDistributor()
    
    # Assign dark stores to orders
    sampled_orders['dark_store_id'] = sampled_orders.apply(distributor.assign_dark_store, axis=1)
    
    # Merge with products data
    order_details = pd.merge(sampled_order_products, sampled_products, on='product_id')
    full_orders = pd.merge(sampled_orders, order_details, on='order_id')
    
    # Create store metadata
    store_metadata = distributor.store_profiles
    
    # Print distribution summary
    print("\nOrders distribution across stores:")
    print(full_orders['dark_store_id'].value_counts())
    
    return full_orders, store_metadata

# Autogen Configuration
config_list = [
    {
        "model": "gpt-4o",
        "api_key": os.getenv("AUTOGEN_MODEL_API_KEY")
    }
]

class HistoricalDataAnalysis:
    def __init__(self, config_list):
        self.assistant = autogen.AssistantAgent(
            name="historical_analyst",
            llm_config={
                "config_list": config_list,
                "temperature": 0.9
            },
            system_message="""
            You are an expert analyst specializing in hyperlocal commerce patterns.
            Your role is to analyze historical order data from dark stores and identify:
            1. Temporal patterns (hourly, daily, weekly)
            2. Product affinity patterns
            3. Location-specific trends
            4. Customer behavior patterns
            5. Inventory movement patterns
            
            Provide detailed insights that can be used for predictive modeling.
            """
        )
        
        self.user_proxy = autogen.UserProxyAgent(
            name="data_provider",
            code_execution_config={"work_dir": "analysis_workspace"}
        )

    def analyze_store_data(self, 
                          full_orders: pd.DataFrame, 
                          store_metadata: Dict,
                          store_id: int) -> Dict:
        """
        Analyze patterns for a specific store using Autogen
        """
        # Filter data for specific store
        store_orders = full_orders[full_orders['dark_store_id'] == store_id]
        store_info = store_metadata[store_id]
        
        # Prepare analysis message
        analysis_request = f"""
        Analyze the following dark store data:
        
        Store Profile:
        - Location: {store_info['location']}
        - Target Demographic: {store_info['demographic']}
        - Peak Hours: {store_info['peak_hours']}
        
        Order Statistics:
        - Total Orders: {len(store_orders)}
        - Unique Products: {store_orders['product_id'].nunique()}
        - Average Order Size: {store_orders.groupby('order_id')['product_id'].count().mean():.2f}
        - Reorder Rate: {store_orders['reordered'].mean():.2%}
        
        Please provide detailed insights about:
        1. Customer behavior patterns
        2. Product preferences
        3. Temporal patterns
        4. Reorder behaviors
        5. Unique characteristics of this store
        
        Format the response as a structured JSON with clear insights.
        """
        
        # Initiate analysis conversation
        # self.user_proxy.initiate_chat(
        #     self.assistant,
        #     message=analysis_request,
        #     max_turns=1
        # )
        
        analysis_response = self.assistant.generate_reply(messages=[{"content": analysis_request, "role": "user"}])
        
        # Define a regular expression pattern to extract JSON content
        json_pattern = r"```json\s*(\{.*\})\s*```"
        match = re.search(json_pattern, analysis_response, re.DOTALL)
        
        if match:
            # Extract the JSON string from the code block
            json_str = match.group(1)
        else:
            # If no code block is found, assume the entire response is JSON
            json_str = analysis_response.strip()
        
        try:
            # Parse the JSON string into a Python dictionary
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # Handle JSON parsing errors
            print("Failed to parse JSON:", e)
            
            print(f"JSON : {analysis_response}")
            return None

def run_historical_analysis(
    orders_file: str = "../reduced_data/orders.csv",
    order_products_file: str = "../reduced_data/order_products__prior.csv",
    products_file: str = "../reduced_data/products.csv"
) -> Dict:
    """
    Run the complete historical data analysis pipeline
    """
    print("Starting historical analysis...")
    
    # Load data
    print("Loading data files...")
    orders_df = pd.read_csv(orders_file)
    order_products_df = pd.read_csv(order_products_file)
    products_df = pd.read_csv(products_file)
    
    # Prepare data with dark store assignments
    print("Preparing and distributing data...")
    full_orders, store_metadata = prepare_historical_data(
        orders_df, order_products_df, products_df
    )
    
    # Initialize analysis system
    print("Initializing Autogen analysis...")
    analyzer = HistoricalDataAnalysis(config_list)
    
    # Analyze each store
    print("Analyzing store patterns...")
    store_insights = {}
    for store_id in range(1, 7):
        print(f"\nAnalyzing store {store_id}: {store_metadata[store_id]['name']}")
        store_insights[store_id] = analyzer.analyze_store_data(
            full_orders, store_metadata, store_id
        )
    
    # Save insights
    print("\nSaving insights to dark_store_insights.json...")
    with open('dark_store_insights.json', 'w') as f:
        json.dump(store_insights, f, indent=4)
    
    print("Analysis complete!")
    return store_insights

if __name__ == "__main__":
    # Set your API key
    os.environ["AUTOGEN_MODEL_API_KEY"] = "your_api_key_here"
    
    # Run the analysis
    insights = run_historical_analysis()
    print("\nAnalysis completed successfully!")