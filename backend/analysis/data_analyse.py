import autogen
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import os 
from dotenv import load_dotenv

load_dotenv()

@dataclass
class MarketInsight:
    """Structure for market insights"""
    category: str
    insight_type: str
    description: str
    value: float
    confidence: float
    recommendation: str
    timestamp: datetime

class MarketAnalysisAgent:
    """
    Enhanced Market Analysis Agent for Quick Commerce
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.insights: List[MarketInsight] = []
        
    def load_and_prepare_data(self, 
                            orders_path: str,
                            products_path: str,
                            order_products_path: str,
                            departments_path: str,
                            aisles_path: str) -> Dict[str, pd.DataFrame]:
        """Load and prepare all required datasets with memory optimization"""
        try:
            # Load datasets with specific dtypes to reduce memory usage
            orders_df = pd.read_csv(orders_path, dtype={
                'order_id': np.int32,
                'order_hour_of_day': np.int8,
                'days_since_prior_order': np.float32
            })
            
            products_df = pd.read_csv(products_path, dtype={
                'product_id': np.int32,
                'aisle_id': np.int32,
                'department_id': np.int32
            })
            
            order_products_df = pd.read_csv(order_products_path, dtype={
                'order_id': np.int32,
                'product_id': np.int32,
                'add_to_cart_order': np.int16,
                'reordered': np.int8
            })
            
            departments_df = pd.read_csv(departments_path, dtype={
                'department_id': np.int32
            })
            
            aisles_df = pd.read_csv(aisles_path, dtype={
                'aisle_id': np.int32
            })
            
            # Merge for complete view
            merged_df = self._merge_datasets(
                orders_df,
                products_df,
                order_products_df,
                departments_df,
                aisles_df
            )
            
            return {
                'orders': orders_df,
                'products': products_df,
                'order_products': order_products_df,
                'merged': merged_df
            }
            
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            raise
            
    def _merge_datasets(self, orders_df, products_df, order_products_df, 
                    departments_df, aisles_df) -> pd.DataFrame:
        """Merge all datasets with proper joins and memory optimization"""
        # Select only necessary columns
        orders_df = orders_df[['order_id', 'order_hour_of_day', 'days_since_prior_order']]
        products_df = products_df[['product_id', 'product_name', 'aisle_id', 'department_id']]
        order_products_df = order_products_df[['order_id', 'product_id', 'add_to_cart_order', 'reordered']]
        
        # Merge order products with products
        merged = pd.merge(
            order_products_df, 
            products_df, 
            on='product_id', 
            how='left'
        )
        
        # Add aisle information
        merged = pd.merge(
            merged,
            aisles_df[['aisle_id', 'aisle']],
            on='aisle_id',
            how='left'
        )
        
        # Add department information
        merged = pd.merge(
            merged,
            departments_df[['department_id', 'department']],
            on='department_id',
            how='left'
        )
        
        # Add order information
        merged = pd.merge(
            merged,
            orders_df,
            on='order_id',
            how='left'
        )
        
        # Free up memory
        del orders_df, products_df, order_products_df, departments_df, aisles_df
        
        return merged

    def analyze_hourly_patterns(self, orders_df: pd.DataFrame) -> Dict:
        """Analyze hourly order patterns"""
        hourly_stats = orders_df.groupby('order_hour_of_day').agg({
            'order_id': 'count',
            'days_since_prior_order': ['mean', 'std']
        }).round(2)
        
        peak_hours = hourly_stats['order_id']['count'].nlargest(3)
        slow_hours = hourly_stats['order_id']['count'].nsmallest(3)
        
        return {
            'peak_hours': peak_hours.to_dict(),
            'slow_hours': slow_hours.to_dict(),
            'hourly_stats': hourly_stats.to_dict(),
            'visualization': self._create_hourly_visualization(hourly_stats)
        }
    
    def analyze_department_performance(self, merged_df: pd.DataFrame) -> Dict:
        """Analyze performance by department"""
        dept_stats = merged_df.groupby('department').agg({
            'order_id': 'count',
            'reordered': ['mean', 'count'],
            'add_to_cart_order': ['mean', 'std']
        }).round(2)
        
        top_departments = dept_stats['order_id']['count'].nlargest(5)
        reorder_leaders = dept_stats['reordered']['mean'].nlargest(5)
        
        return {
            'top_departments': top_departments.to_dict(),
            'reorder_leaders': reorder_leaders.to_dict(),
            'department_stats': dept_stats.to_dict(),
            'visualization': self._create_department_visualization(dept_stats)
        }
    
    def analyze_product_performance(self, merged_df: pd.DataFrame) -> Dict:
        """Analyze product level performance"""
        product_stats = merged_df.groupby('product_name').agg({
            'order_id': 'count',
            'reordered': ['mean', 'sum'],
            'add_to_cart_order': 'mean'
        }).round(2)
        
        top_products = product_stats['order_id']['count'].nlargest(10)
        most_reordered = product_stats['reordered']['mean'].nlargest(10)
        
        return {
            'top_products': top_products.to_dict(),
            'most_reordered': most_reordered.to_dict(),
            'product_stats': product_stats.to_dict()
        }
    
    def analyze_basket_patterns(self, merged_df: pd.DataFrame) -> Dict:
        """Analyze shopping basket patterns with memory efficient approach"""
        # Calculate average basket size
        basket_sizes = merged_df.groupby('order_id').size()
        
        # Find common product pairs more efficiently
        # First, get orders with their products
        order_products = merged_df[['order_id', 'product_id', 'product_name']].copy()
        
        # Initialize storage for product pairs
        pair_counts = {}
        
        # Process each order group
        for order_id, group in order_products.groupby('order_id'):
            # Get products in this order
            products = group[['product_id', 'product_name']].values.tolist()
            
            # Create pairs within this order
            for i in range(len(products)):
                for j in range(i + 1, len(products)):
                    # Ensure consistent ordering of product IDs
                    if products[i][0] < products[j][0]:
                        pair = (products[i][1], products[j][1])
                    else:
                        pair = (products[j][1], products[i][1])
                    
                    # Increment count for this pair
                    pair_counts[pair] = pair_counts.get(pair, 0) + 1
        
        # Convert to series and get top pairs
        common_pairs = pd.Series(pair_counts).nlargest(10)
        
        return {
            'avg_basket_size': basket_sizes.mean(),
            'basket_size_std': basket_sizes.std(),
            'common_pairs': common_pairs.to_dict(),
            'visualization': self._create_basket_visualization(basket_sizes)
        }

    
    def analyze_reorder_patterns(self, merged_df: pd.DataFrame) -> Dict:
        """Analyze reorder patterns"""
        reorder_stats = merged_df.groupby(['department', 'aisle']).agg({
            'reordered': ['mean', 'count'],
            'days_since_prior_order': ['mean', 'std']
        }).round(2)
        
        high_reorder_categories = reorder_stats['reordered']['mean'].nlargest(10)
        
        return {
            'reorder_stats': reorder_stats.to_dict(),
            'high_reorder_categories': high_reorder_categories.to_dict(),
            'visualization': self._create_reorder_visualization(reorder_stats)
        }
    
    def _create_hourly_visualization(self, hourly_stats: pd.DataFrame) -> str:
        """Create hourly pattern visualization"""
        plt.figure(figsize=(12, 6))
        sns.barplot(x=hourly_stats.index, 
                   y=hourly_stats['order_id']['count'])
        plt.title('Orders by Hour of Day')
        plt.xlabel('Hour')
        plt.ylabel('Number of Orders')
        
        # Save plot to string
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()
        
        return base64.b64encode(image_png).decode()
    
    def _create_department_visualization(self, dept_stats: pd.DataFrame) -> str:
        """Create department performance visualization"""
        plt.figure(figsize=(12, 6))
        sns.barplot(x=dept_stats.index, 
                   y=dept_stats['order_id']['count'])
        plt.xticks(rotation=45)
        plt.title('Orders by Department')
        plt.xlabel('Department')
        plt.ylabel('Number of Orders')
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()
        
        return base64.b64encode(image_png).decode()
    
    def _create_basket_visualization(self, basket_sizes: pd.Series) -> str:
        """Create basket size distribution visualization"""
        plt.figure(figsize=(10, 6))
        sns.histplot(data=basket_sizes, bins=30)
        plt.title('Distribution of Basket Sizes')
        plt.xlabel('Number of Items')
        plt.ylabel('Frequency')
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()
        
        return base64.b64encode(image_png).decode()
    
    def _create_reorder_visualization(self, reorder_stats: pd.DataFrame) -> str:
        """Create reorder patterns visualization"""
        plt.figure(figsize=(12, 6))
        sns.barplot(x=reorder_stats.index.get_level_values('department'), 
                   y=reorder_stats['reordered']['mean'])
        plt.xticks(rotation=45)
        plt.title('Reorder Rates by Department')
        plt.xlabel('Department')
        plt.ylabel('Reorder Rate')
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close()
        
        return base64.b64encode(image_png).decode()
    
    def generate_insights(self, analysis_results: Dict) -> List[MarketInsight]:
        """Generate actionable insights from analysis results"""
        insights = []
        
        # Hourly pattern insights
        peak_hours = analysis_results['hourly_patterns']['peak_hours']
        insights.append(
            MarketInsight(
                category="Timing",
                insight_type="Peak Hours",
                description=f"Peak order hours identified at {list(peak_hours.keys())}",
                value=max(peak_hours.values()),
                confidence=0.95,
                recommendation="Increase staffing during peak hours",
                timestamp=datetime.now()
            )
        )
        
        # Department insights
        top_depts = analysis_results['department_performance']['top_departments']
        insights.append(
            MarketInsight(
                category="Department",
                insight_type="Popular Departments",
                description=f"Top performing departments: {list(top_depts.keys())[:3]}",
                value=max(top_depts.values()),
                confidence=0.90,
                recommendation="Optimize inventory for top departments",
                timestamp=datetime.now()
            )
        )
        
        # Reorder insights
        high_reorder = analysis_results['reorder_patterns']['high_reorder_categories']
        insights.append(
            MarketInsight(
                category="Reorders",
                insight_type="High Reorder Categories",
                description=f"Categories with highest reorder rates: {list(high_reorder.keys())[:3]}",
                value=max(high_reorder.values()),
                confidence=0.85,
                recommendation="Maintain strong stock levels for high-reorder items",
                timestamp=datetime.now()
            )
        )
        
        return insights

# Create AutoGen agent configuration
config_list_market = [{
    "model" : "gpt-4o",
    "temperature" : "0.9",
    "api_key": os.getenv("AUTOGEN_MODEL_API_KEY")
}]

# Create the AutoGen Market Analyst Agent
market_analyst_agent = autogen.AssistantAgent(
    name="market_analyst",
    system_message="""You are a Market Analysis agent specialized in quick commerce data.
    You analyze:
    1. Hourly demand patterns
    2. Department performance
    3. Product popularity
    4. Reorder patterns
    5. Basket combinations
    
    You should:
    - Focus on actionable insights
    - Identify clear patterns
    - Suggest specific improvements
    - Flag potential issues""",
    llm_config={
        "model": "gpt-4o",
        "temperature": 0.9,
        "api_key": os.getenv("AUTOGEN_MODEL_API_KEY")
    }
)

# Test function
def test_market_analysis():
    """Test the market analysis agent with sample data"""
    try:
        analyst = MarketAnalysisAgent()
        
        # Load data (using your paths)
        data = analyst.load_and_prepare_data(
            "../data/orders.csv/orders.csv",
            "../data/products.csv/products.csv",
            "../data/order_products__prior.csv/order_products__prior.csv",
            "../data/departments.csv/departments.csv",
            "../data/aisles.csv/aisles.csv"
        )
        
        # Run analysis
        analysis_results = {
            'hourly_patterns': analyst.analyze_hourly_patterns(data['orders']),
            'department_performance': analyst.analyze_department_performance(data['merged']),
            'product_performance': analyst.analyze_product_performance(data['merged']),
            'basket_patterns': analyst.analyze_basket_patterns(data['merged']),
            'reorder_patterns': analyst.analyze_reorder_patterns(data['merged'])
        }
        
        # Generate insights
        insights = analyst.generate_insights(analysis_results)
        
        return {
            'analysis_results': analysis_results,
            'insights': insights
        }
        
    except Exception as e:
        print(f"Error in test: {e}")
        raise

if __name__ == "__main__":
    # Run test
    results = test_market_analysis()
    
    # Print some results
    print("\nAnalysis Results:")
    for category, analysis in results['analysis_results'].items():
        print(f"\n{category.upper()}:")
        for key, value in analysis.items():
            if key != 'visualization':
                print(f"{key}: {value}")
    
    print("\nKey Insights:")
    for insight in results['insights']:
        print(f"\nCategory: {insight.category}")
        print(f"Type: {insight.insight_type}")
        print(f"Description: {insight.description}")
        print(f"Recommendation: {insight.recommendation}")