import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

load_dotenv()

# fix @ symbol in password
password = quote_plus(os.getenv('DB_PASSWORD'))

# database connection
engine = create_engine(
    f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{password}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}",
    pool_pre_ping=True
)

# all 9 CSV files
csv_files = {
    "olist_customers_dataset.csv":           "customers",
    "olist_geolocation_dataset.csv":         "geolocation",
    "olist_orders_dataset.csv":              "orders",
    "olist_order_items_dataset.csv":         "order_items",
    "olist_order_payments_dataset.csv":      "order_payments",
    "olist_order_reviews_dataset.csv":       "order_reviews",
    "olist_products_dataset.csv":            "products",
    "olist_sellers_dataset.csv":             "sellers",
    "product_category_name_translation.csv": "product_category_translation"
}

for filename, tablename in csv_files.items():
    try:
        filepath = f"data/raw/{filename}"
        print(f"Loading {filename} → table: {tablename} ...")
        df = pd.read_csv(filepath, encoding='utf-8')

        # use a fresh connection for each table
        with engine.begin() as conn:
            df.to_sql(
                name=tablename,
                con=conn,
                if_exists="replace",
                index=False,
                chunksize=1000
            )
        print(f" {tablename} loaded — {len(df)} rows")

    except Exception as e:
        print(f" Error loading {tablename}: {e}")
        continue

print("\n All tables processed!")