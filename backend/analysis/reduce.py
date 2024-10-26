import pandas as pd
import numpy as np
from pathlib import Path
import os

def reduce_dataset(reduction_factor):
    """
    Reduce the Instacart dataset size while maintaining distributions
    
    Parameters:
    reduction_factor: float, fraction of data to keep (e.g., 0.5 for half)
    """
    
    # Hardcoded paths as per your original code
    input_paths = {
        'aisles': "../data/aisles.csv/aisles.csv",
        'departments': "../data/departments.csv/departments.csv",
        'order_products_prior': "../data/order_products__prior.csv/order_products__prior.csv",
        'order_products_train': "../data/order_products__train.csv/order_products__train.csv",
        'orders': "../data/orders.csv/orders.csv",
        'products': "../data/products.csv/products.csv"
    }
    
    # Create output directory
    output_base = "../reduced_data"
    os.makedirs(output_base, exist_ok=True)
    
    print(f"Starting dataset reduction with factor: {reduction_factor}")
    
    # 1. First load the smaller, reference tables completely
    print("Loading reference tables...")
    departments_df = pd.read_csv(input_paths['departments'])
    aisles_df = pd.read_csv(input_paths['aisles'])
    products_df = pd.read_csv(input_paths['products'])
    
    # Save reference tables as is - they're small and needed for references
    departments_df.to_csv(f"{output_base}/departments.csv", index=False)
    aisles_df.to_csv(f"{output_base}/aisles.csv", index=False)
    products_df.to_csv(f"{output_base}/products.csv", index=False)
    
    # 2. Sample orders first - this will drive other reductions
    print("Processing orders...")
    orders_df = pd.read_csv(input_paths['orders'])
    
    # Stratified sampling by eval_set to maintain train/prior/test proportions
    sampled_orders = orders_df.groupby('eval_set', group_keys=False).apply(
        lambda x: x.sample(frac=reduction_factor, random_state=42)
    )
    
    # Save reduced orders
    sampled_orders.to_csv(f"{output_base}/orders.csv", index=False)
    
    # Get sampled order IDs for filtering other datasets
    sampled_order_ids = set(sampled_orders['order_id'].values)
    
    # 3. Process order_products_prior
    print("Processing order_products_prior...")
    chunk_size = 1000000  # Process 1 million rows at a time
    
    # Process in chunks to handle large file
    chunks = pd.read_csv(input_paths['order_products_prior'], chunksize=chunk_size)
    
    first_chunk = True
    for chunk in chunks:
        reduced_chunk = chunk[chunk['order_id'].isin(sampled_order_ids)]
        
        mode = 'w' if first_chunk else 'a'
        header = first_chunk
        
        reduced_chunk.to_csv(f"{output_base}/order_products__prior.csv",
                           mode=mode, header=header, index=False)
        first_chunk = False
    
    # 4. Process order_products_train similarly
    print("Processing order_products_train...")
    chunks = pd.read_csv(input_paths['order_products_train'], chunksize=chunk_size)
    
    first_chunk = True
    for chunk in chunks:
        reduced_chunk = chunk[chunk['order_id'].isin(sampled_order_ids)]
        
        mode = 'w' if first_chunk else 'a'
        header = first_chunk
        
        reduced_chunk.to_csv(f"{output_base}/order_products__train.csv",
                           mode=mode, header=header, index=False)
        first_chunk = False
    
    # 5. Print statistics and verify distributions
    print("\nDataset reduction complete. Summary:")
    
    # Size reduction statistics
    original_orders = len(orders_df)
    reduced_orders = len(sampled_orders)
    print(f"Orders reduction: {original_orders} → {reduced_orders} "
          f"({reduced_orders/original_orders:.2%})")
    
    # Verify key distributions
    print("\nDistribution Comparisons:")
    
    # Order hour distribution
    original_hour_dist = orders_df['order_hour_of_day'].value_counts(normalize=True)
    reduced_hour_dist = sampled_orders['order_hour_of_day'].value_counts(normalize=True)
    hour_dist_diff = (original_hour_dist - reduced_hour_dist).abs().mean()
    print(f"Order hour distribution difference: {hour_dist_diff:.4f}")
    
    # Eval set distribution
    original_eval_dist = orders_df['eval_set'].value_counts(normalize=True)
    reduced_eval_dist = sampled_orders['eval_set'].value_counts(normalize=True)
    eval_dist_diff = (original_eval_dist - reduced_eval_dist).abs().mean()
    print(f"Eval set distribution difference: {eval_dist_diff:.4f}")

if __name__ == "__main__":
    # Get reduction factor from user
    while True:
        try:
            reduction_factor = float(input("Enter reduction factor (0-1, e.g., 0.5 for half size): "))
            if 0 < reduction_factor < 1:
                break
            else:
                print("Please enter a value between 0 and 1")
        except ValueError:
            print("Please enter a valid number")
    
    # Run reduction
    reduce_dataset(reduction_factor)