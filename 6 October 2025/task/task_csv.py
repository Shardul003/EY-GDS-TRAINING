import csv
import logging

# Configure logging
logging.basicConfig(filename='task_csv.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

try:
    with open('sales_data.csv', 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                product = row['product']
                price = float(row['price'])
                quantity = int(row['quantity'])
                total = price * quantity
                print(f"{product} total = {int(total)}")
                logging.info(f"{product} total sales {int(total)}")
            except ValueError:
                logging.error(f"Invalid numeric value in row: {row}")

except FileNotFoundError:
    logging.error("sales_data.csv not found")
    print("Error: sales_data.csv not found")
