import pandas as pd
from sqlalchemy import create_engine, text


#file info
orders_path = "olist_orders_dataset.csv"
customers_path = "olist_customers_dataset.csv"
items_path = "olist_order_items_dataset.csv"
products_path = "olist_products_dataset.csv"

#read order excel file
print("Reading olist files")
df_orders = pd.read_csv(orders_path)
df_customers = pd.read_csv(customers_path)
df_items = pd.read_csv(items_path)
df_products = pd.read_csv(products_path)

#df = pd.read_csv(file_path, encoding="utf-8")  # 或是 encoding="utf-8-sig"
#*   **分隔符號（Delimiter）**：標準 CSV 是用逗號 `,` 分隔，但有些系統吐出來的可能用分號 `;` 或 Tab 鍵。Pandas 預設是逗號，如果之後發現資料全部擠在同一欄，可以用 `sep` 來調整：

#df = pd.read_csv(file_path, sep=",")

#check read successfully
print(f"Successful! There's {df_orders.shape[0]} orders data")
print(f"Successful! There's {df_customers.shape[0]} customers data")
print(f"Successful! There's {df_items.shape[0]} orders items data")
print(f"Successful! There's {df_products.shape[0]} products data")


#create db connection
# 連線字串格式：postgresql://帳號:密碼@主機位置:Port/資料庫名稱
# 提示：預設的 Port 通常是 5432
db_url = "postgresql://postgres:post1234@127.0.0.1:5433/postgres"

engine = create_engine(db_url)

print("Test PostgreSQL connection...")
try:
    # 將 .connect() 改為 .begin()，這樣 block 結束時會自動自動 COMMIT，超省事！
    with engine.begin() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Connect successfully!")

        # 🟢 最安全的做法：一桌一桌檢查是否存在，在的話才清空！
        tables_to_truncate = ["raw_orders", "raw_customers", "raw_orders_items", "raw_products"]
        
        print("Truncating old raw tables if they exist...")
        for table in tables_to_truncate:
            # 檢查資料表是否已經存在於 database 中
            check_query = text(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = '{table}'
                );
            """)
            table_exists = connection.execute(check_query).scalar()
            
            if table_exists:
                connection.execute(text(f"TRUNCATE TABLE {table} CASCADE;"))
                print(f"-> Table {table} truncated.")
            else:
                print(f"-> Table {table} does not exist yet. Skip truncate.")
                
        print("Truncate process completed successfully!")

except Exception as e:
    print("Failed to connect to PostgreSQL.")
    print(f"Error message as following:{e}")
    exit(1)

#Pipeline: load data to db
df_orders.to_sql("raw_orders", con=engine, if_exists="append",index=False,method="multi",chunksize=10000)
df_customers.to_sql("raw_customers", con=engine, if_exists="append",index=False,method="multi",chunksize=10000)
df_items.to_sql("raw_orders_items", con=engine, if_exists="append",index=False,method="multi",chunksize=10000)
df_products.to_sql("raw_products", con=engine, if_exists="append",index=False,method="multi",chunksize=10000)

#check data already loaded to db
print("Checking data already loaded to db:")
with engine.connect() as connection:
    for table_name,df in [("raw_orders",df_orders),
                     ("raw_customers",df_customers),
                     ("raw_orders_items",df_items),
                     ("raw_products",df_products)]:
        #db count
        query = text(f"select count(*) from {table_name}")
        db_count = connection.execute(query).scalar() # .scalar() 可以直接拿到那個計算出來的數字
        #df count
        df_count = df.shape[0]

        #print result
        if db_count == df_count:
            print(f"{table_name} has correct records: db:{db_count} records == Python: {df_count} records")
        else:
            print(f"{table_name} has incorrect records: db:{db_count} records while Python: {df_count} records")

