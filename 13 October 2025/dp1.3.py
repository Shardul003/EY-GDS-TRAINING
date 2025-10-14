import pandas as pd
from datetime import datetime

products_df = pd.read_csv('product.csv')
customers_df = pd.read_csv('customer.csv')
orders_df = pd.read_csv('order.csv')

order_cust = pd.merge(orders_df, customers_df, on = 'CustomerID')
df = pd.merge(order_cust, products_df, on = 'ProductID')

df['TotalAmount'] = df['Quantity'] * df['Price']

df['OrderMonth'] = pd.to_datetime(df['OrderDate']).dt.month_name()

df = df[df['Quantity'] >= 2]

df = df[(df['Country'] == 'UAE') | (df['Country'] == 'India')]
category_df = df.groupby('Category')['TotalAmount'].sum().reset_index()
segment_df = df.groupby('Segment')['TotalAmount'].sum().reset_index()

df = df.sort_values(by = "TotalAmount", ascending = False)
df.to_csv('processed_orders.csv', index=False)
category_df.to_csv('category_summary.csv', index=False)
segment_df.to_csv('segment_summary.csv', index=False)
