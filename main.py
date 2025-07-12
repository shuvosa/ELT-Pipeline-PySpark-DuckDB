import duckdb
from pyspark.sql import SparkSession

# Initialize PySpark
spark = SparkSession.builder.appName("ELT with PySpark and DuckDB").getOrCreate()

# Step 1: Extract Data
orders = spark.read.csv("data/orders.csv", header=True, inferSchema=True)
customers = spark.read.csv("data/customers.csv", header=True, inferSchema=True)
products = spark.read.csv("data/products.csv", header=True, inferSchema=True)

# Convert PySpark DataFrames to Pandas for DuckDB
orders_df = orders.toPandas()
customers_df = customers.toPandas()
products_df = products.toPandas()

# Step 2: Load Data into DuckDB
con = duckdb.connect("elt_project.duckdb")

con.register("orders_df", orders_df)
con.register("customers_df", customers_df)
con.register("products_df", products_df)

# Force recreate the tables
con.execute("DROP TABLE IF EXISTS orders")
con.execute("DROP TABLE IF EXISTS customers")
con.execute("DROP TABLE IF EXISTS products")

con.execute("CREATE TABLE orders AS SELECT * FROM orders_df")
con.execute("CREATE TABLE customers AS SELECT * FROM customers_df")
con.execute("CREATE TABLE products AS SELECT * FROM products_df")

# Step 3: Transform Data
query = """
SELECT 
    o.order_id, 
    o.customer_id, 
    c.customer_name, 
    o.email, 
    o.product_id, 
    p.product_name, 
    p.category
FROM 
    orders o
JOIN 
    customers c ON o.customer_id = c.customer_id
JOIN 
    products p ON o.product_id = p.product_id
"""

result = con.execute(query).df()

# Display Results
print(result)

# Save the results to a CSV file
result.to_csv("data/processed_orders.csv", index=False)

# Close connections
con.close()
spark.stop()
