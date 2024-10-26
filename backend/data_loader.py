import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import os
import zipfile
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InstacartDataLoader:
    """
    Handles downloading and processing the Instacart dataset
    """
    def __init__(self, data_dir="instacart_data"):
        self.data_dir = data_dir
        self.base_url = "https://s3.amazonaws.com/instacart-datasets/instacart_online_grocery_shopping_2017.tar.gz"
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
    def download_dataset(self):
        """Download the Instacart dataset"""
        try:
            logger.info("Downloading Instacart dataset...")
            
            # Download the file
            response = requests.get(self.base_url, stream=True)
            file_path = os.path.join(self.data_dir, "instacart_data.tar.gz")
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        
            # Extract the files
            logger.info("Extracting files...")
            os.system(f"tar -xzf {file_path} -C {self.data_dir}")
            
            logger.info("Dataset downloaded and extracted successfully!")
            
        except Exception as e:
            logger.error(f"Error downloading dataset: {str(e)}")
            raise

    def load_and_process_data(self):
        """Load and process all Instacart CSV files"""
        try:
            logger.info("Loading and processing Instacart data...")
            
            # Load original Instacart files
            orders = pd.read_csv(f"{self.data_dir}/orders.csv")
            order_products = pd.read_csv(f"{self.data_dir}/order_products__prior.csv")
            products = pd.read_csv(f"{self.data_dir}/products.csv")
            departments = pd.read_csv(f"{self.data_dir}/departments.csv")
            aisles = pd.read_csv(f"{self.data_dir}/aisles.csv")
            
            # Process and enhance the data
            processed_data = self._enhance_data_for_quick_commerce(
                orders, order_products, products, departments, aisles
            )
            
            logger.info("Data processing completed!")
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            raise

    def _enhance_data_for_quick_commerce(self, orders, order_products, products, departments, aisles):
        """
        Transform Instacart data into quick-commerce format with additional fields
        """
        logger.info("Enhancing data for quick-commerce...")
        
        # 1. Enhance Orders
        enhanced_orders = self._process_orders(orders)
        
        # 2. Enhance Products
        enhanced_products = self._process_products(products, departments, aisles)
        
        # 3. Enhance Order Products
        enhanced_order_products = self._process_order_products(order_products)
        
        # 4. Create Inventory Snapshots
        inventory_snapshots = self._create_inventory_snapshots(
            enhanced_orders, enhanced_products
        )
        
        return {
            'orders': enhanced_orders,
            'products': enhanced_products,
            'order_products': enhanced_order_products,
            'inventory_snapshots': inventory_snapshots
        }

    def _process_orders(self, orders):
        """Process and enhance orders data"""
        logger.info("Processing orders...")
        
        # Copy original dataframe
        enhanced_orders = orders.copy()
        
        # Add quick-commerce specific fields
        enhanced_orders['order_timestamp'] = pd.to_datetime('2023-01-01') + pd.to_timedelta(
            enhanced_orders.index % (7*24), unit='H'
        )
        
        # Add delivery time (typically 10-30 minutes in quick commerce)
        enhanced_orders['delivery_duration_minutes'] = np.random.randint(10, 31, size=len(enhanced_orders))
        enhanced_orders['delivery_timestamp'] = enhanced_orders['order_timestamp'] + pd.to_timedelta(
            enhanced_orders['delivery_duration_minutes'], unit='minute'
        )
        
        # Add store_id (assuming multiple dark stores)
        enhanced_orders['store_id'] = np.random.randint(1, 6, size=len(enhanced_orders))
        
        # Add order status
        status_choices = ['completed', 'cancelled', 'stockout']
        status_weights = [0.92, 0.05, 0.03]  # 92% completed, 5% cancelled, 3% stockout
        enhanced_orders['order_status'] = np.random.choice(
            status_choices,
            size=len(enhanced_orders),
            p=status_weights
        )
        
        # Add total amount (random for now, will be calculated properly when joining with products)
        enhanced_orders['total_amount'] = np.random.uniform(20, 100, size=len(enhanced_orders))
        
        return enhanced_orders

    def _process_products(self, products, departments, aisles):
        """Process and enhance products data"""
        logger.info("Processing products...")
        
        # Merge with departments and aisles
        enhanced_products = products.merge(departments, on='department_id')
        enhanced_products = enhanced_products.merge(aisles, on='aisle_id')
        
        # Add quick-commerce specific fields
        enhanced_products['perishable'] = enhanced_products['aisle'].apply(
            lambda x: 1 if any(word in x.lower() for word in ['fresh', 'meat', 'dairy', 'produce']) else 0
        )
        
        # Add storage temperature requirements
        def determine_storage_temp(row):
            aisle_lower = row['aisle'].lower()
            if 'frozen' in aisle_lower:
                return 'frozen'
            elif any(word in aisle_lower for word in ['fresh', 'meat', 'dairy', 'produce']):
                return 'chilled'
            return 'ambient'
            
        enhanced_products['storage_temp'] = enhanced_products.apply(determine_storage_temp, axis=1)
        
        # Add shelf life (days)
        def determine_shelf_life(row):
            if row['storage_temp'] == 'frozen':
                return np.random.randint(60, 180)
            elif row['storage_temp'] == 'chilled':
                return np.random.randint(3, 14)
            return np.random.randint(30, 365)
            
        enhanced_products['shelf_life_days'] = enhanced_products.apply(determine_shelf_life, axis=1)
        
        # Add price and typical stock levels
        enhanced_products['price'] = np.random.uniform(2, 50, size=len(enhanced_products))
        enhanced_products['typical_stock_units'] = np.random.randint(20, 100, size=len(enhanced_products))
        
        return enhanced_products

    def _process_order_products(self, order_products):
        """Process and enhance order products data"""
        logger.info("Processing order products...")
        
        # Copy original dataframe
        enhanced_order_products = order_products.copy()
        
        # Add quantity (most quick commerce orders have 1-3 units per product)
        enhanced_order_products['quantity'] = np.random.randint(1, 4, size=len(order_products))
        
        # We'll add price-related fields after joining with products
        enhanced_order_products['unit_price'] = 0.0  # placeholder
        enhanced_order_products['total_price'] = 0.0  # placeholder
        
        return enhanced_order_products

    def _create_inventory_snapshots(self, orders, products):
        """Create inventory snapshots data"""
        logger.info("Creating inventory snapshots...")
        
        # Get unique combinations of store_id and product_id
        stores = orders['store_id'].unique()
        product_ids = products['product_id'].unique()
        
        # Create timestamps for snapshots (every hour for the past week)
        end_time = orders['order_timestamp'].max()
        start_time = end_time - pd.Timedelta(days=7)
        timestamps = pd.date_range(start=start_time, end=end_time, freq='1H')
        
        # Initialize empty list for snapshots
        snapshots = []
        
        # Create snapshots
        for store_id in stores:
            for product_id in product_ids:
                typical_stock = products.loc[
                    products['product_id'] == product_id,
                    'typical_stock_units'
                ].iloc[0]
                
                for timestamp in timestamps:
                    # Randomize stock levels around typical stock
                    current_stock = max(0, int(
                        typical_stock * np.random.normal(0.8, 0.2)
                    ))
                    
                    snapshots.append({
                        'snapshot_timestamp': timestamp,
                        'store_id': store_id,
                        'product_id': product_id,
                        'units_in_stock': current_stock,
                        'units_in_transit': np.random.randint(0, 10),
                        'stockout_last_24h': 1 if current_stock == 0 else 0,
                        'waste_units_last_24h': np.random.randint(0, 3) if products.loc[
                            products['product_id'] == product_id,
                            'perishable'
                        ].iloc[0] else 0
                    })
        
        return pd.DataFrame(snapshots)

# Example usage
if __name__ == "__main__":
    # Initialize data loader
    loader = InstacartDataLoader()
    
    # Download dataset if needed
    if not os.path.exists("instacart_data/orders.csv"):
        loader.download_dataset()
    
    # Load and process data
    processed_data = loader.load_and_process_data()
    
    # Print some statistics
    print("\nDataset Statistics:")
    for key, df in processed_data.items():
        print(f"\n{key.upper()}:")
        print(f"Shape: {df.shape}")
        print("\nSample data:")
        print(df.head())
        print("\nColumns:")
        print(df.columns.tolist())