import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load all CSVs into dataframes
aisles_df = pd.read_csv("../reduced_data/aisles.csv")
departments_df = pd.read_csv("../reduced_data/departments.csv")
order_prior_df = pd.read_csv("../reduced_data/order_products__prior.csv")
order_train_df = pd.read_csv("../reduced_data/order_products__train.csv")
orders_df = pd.read_csv("../reduced_data/orders.csv")
products_df = pd.read_csv("../reduced_data/products.csv")


# Quick glance at each dataset
print("Aisles Data:\n", aisles_df.head())
print("Departments Data:\n", departments_df.head())
print("Order Products Prior Data:\n", order_prior_df.head())
print("Order Products Train Data:\n", order_train_df.head())
print("Orders Data:\n", orders_df.head())
print("Products Data:\n", products_df.head())

# Merge datasets for a complete view (using order_prior and products as example)
order_products_merged = pd.merge(order_prior_df, products_df, on='product_id', how='left')
order_products_merged = pd.merge(order_products_merged, aisles_df, on='aisle_id', how='left')
order_products_merged = pd.merge(order_products_merged, departments_df, on='department_id', how='left')

# Basic statistics and insights
print("\nMerged Data Description:\n", order_products_merged.describe())

# Visualize orders per department
plt.figure(figsize=(10, 6))
order_count_by_department = order_products_merged['department'].value_counts()
sns.barplot(x=order_count_by_department.index, y=order_count_by_department.values)
plt.xticks(rotation=90)
plt.title('Number of Orders per Department')
plt.show()

# Visualize the most ordered products
plt.figure(figsize=(10, 6))
top_products = order_products_merged['product_name'].value_counts().head(10)
sns.barplot(x=top_products.index, y=top_products.values)
plt.xticks(rotation=90)
plt.title('Top 10 Most Ordered Products')
plt.show()

# Analyze order frequency by hour of day
plt.figure(figsize=(10, 6))
order_hour_distribution = orders_df['order_hour_of_day'].value_counts().sort_index()
sns.barplot(x=order_hour_distribution.index, y=order_hour_distribution.values)
plt.title('Order Frequency by Hour of the Day')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Orders')
plt.show()

# Explore reorder ratio
reorder_ratio = order_products_merged['reordered'].value_counts(normalize=True)
print("\nReorder Ratio:\n", reorder_ratio)
sns.barplot(x=reorder_ratio.index, y=reorder_ratio.values)
plt.title('Reorder vs First Time Order')
plt.xlabel('Reordered (1 = Yes, 0 = No)')
plt.ylabel('Proportion')
plt.show()
