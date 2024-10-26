import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class DarkStoreProfile:
    def __init__(
        self,
        store_id: int,
        name: str,
        peak_hours: List[int],
        product_weights: Dict[str, float],
        order_size_params: Tuple[float, float]
    ):
        self.store_id = store_id
        self.name = name
        self.peak_hours = peak_hours
        self.product_weights = product_weights
        self.order_size_params = order_size_params  # (mean, std) for order size distribution

class DarkStoreDistributor:
    def __init__(self, orders_df: pd.DataFrame, products_df: pd.DataFrame, departments_df: pd.DataFrame):
        self.orders_df = orders_df
        self.products_df = products_df
        self.departments_df = departments_df
        self.store_profiles = self._create_store_profiles()
        
    def _create_store_profiles(self) -> List[DarkStoreProfile]:
        """Create profiles for each dark store with distinct characteristics"""
        return [
            DarkStoreProfile(
                store_id=1,
                name="Business District Hub",
                peak_hours=[11, 12, 13, 14, 15],  # Lunch hours
                product_weights={
                    'prepared soups salads': 2.0,
                    'instant foods': 1.8,
                    'beverages': 1.5
                },
                order_size_params=(3, 1)  # Smaller, quick orders
            ),
            DarkStoreProfile(
                store_id=2,
                name="Premium Residential",
                peak_hours=[9, 10, 17, 18, 19],
                product_weights={
                    'specialty cheeses': 2.0,
                    'organic products': 1.8,
                    'fresh fruits': 1.6
                },
                order_size_params=(5, 2)  # Larger, planned orders
            ),
            DarkStoreProfile(
                store_id=3,
                name="University Zone",
                peak_hours=[14, 15, 16, 20, 21, 22, 23],
                product_weights={
                    'snacks': 2.0,
                    'energy drinks': 1.8,
                    'instant foods': 1.5
                },
                order_size_params=(2, 1)  # Small, frequent orders
            ),
            DarkStoreProfile(
                store_id=4,
                name="Family Suburb",
                peak_hours=[9, 10, 11, 17, 18, 19],
                product_weights={
                    'baby food formula': 2.0,
                    'fresh vegetables': 1.8,
                    'bulk items': 1.6
                },
                order_size_params=(7, 2)  # Large family orders
            ),
            DarkStoreProfile(
                store_id=5,
                name="Mixed Commercial",
                peak_hours=[10, 11, 12, 13, 14, 15, 16, 17],
                product_weights={},  # Balanced weights
                order_size_params=(4, 2)  # Medium varied orders
            ),
            DarkStoreProfile(
                store_id=6,
                name="Urban Residential",
                peak_hours=[18, 19, 20, 21],
                product_weights={
                    'ready meals': 1.5,
                    'fresh produce': 1.4,
                    'dairy eggs': 1.3
                },
                order_size_params=(3, 1)  # Medium-small orders
            )
        ]

    def assign_orders_to_stores(self) -> pd.DataFrame:
        """Distribute orders among dark stores based on profiles"""
        
        # Create a copy of orders DataFrame to add store assignments
        orders_with_stores = self.orders_df.copy()
        
        # Initialize store assignment column
        orders_with_stores['dark_store_id'] = None
        
        # Calculate store assignment probabilities based on hour of day
        def assign_store(row):
            hour = row['order_hour_of_day']
            probabilities = self._calculate_store_probabilities(hour)
            return np.random.choice(
                [profile.store_id for profile in self.store_profiles],
                p=probabilities
            )
        
        # Assign stores to orders
        orders_with_stores['dark_store_id'] = orders_with_stores.apply(
            assign_store, axis=1
        )
        
        return orders_with_stores
    
    def _calculate_store_probabilities(self, hour: int) -> List[float]:
        """Calculate probability distribution for store assignment based on hour"""
        probabilities = []
        
        for profile in self.store_profiles:
            # Base probability
            prob = 1.0
            
            # Increase probability during peak hours
            if hour in profile.peak_hours:
                prob *= 2.0
            
            probabilities.append(prob)
        
        # Normalize probabilities
        total = sum(probabilities)
        return [p/total for p in probabilities]
    
    def get_store_statistics(self, orders_with_stores: pd.DataFrame) -> pd.DataFrame:
        """Generate statistics for each store"""
        stats = []
        
        for profile in self.store_profiles:
            store_orders = orders_with_stores[
                orders_with_stores['dark_store_id'] == profile.store_id
            ]
            
            stats.append({
                'store_id': profile.store_id,
                'store_name': profile.name,
                'total_orders': len(store_orders),
                'avg_order_hour': store_orders['order_hour_of_day'].mean(),
                'peak_hour': store_orders['order_hour_of_day'].mode().iloc[0],
                'orders_per_day': len(store_orders) / store_orders['order_dow'].nunique()
            })
        
        return pd.DataFrame(stats)

def create_distributed_dataset(
    orders_df: pd.DataFrame,
    products_df: pd.DataFrame,
    departments_df: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Create a distributed dataset across dark stores
    Returns:
        - Orders with store assignments
        - Store statistics
    """
    distributor = DarkStoreDistributor(orders_df, products_df, departments_df)
    orders_with_stores = distributor.assign_orders_to_stores()
    store_stats = distributor.get_store_statistics(orders_with_stores)
    
    return orders_with_stores, store_stats