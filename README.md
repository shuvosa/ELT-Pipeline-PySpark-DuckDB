# ELT-Pipeline-PySpark-DuckDB

A forward-thinking, scalable ELT (Extract-Load-Transform) project leveraging **PySpark** for large-scale extraction and **DuckDB** for in-process analytics and transformations. This repository ingests raw CSV data, loads it into DuckDB, runs SQL transformations, and exports processed results.

---

## 🚀 Features

- **Distributed Extraction** with PySpark  
- **In-Process Analytics** using DuckDB  
- Schema-on-read: no upfront DDL required  
- Zero-copy CSV ingestion for sub-second loads  
- Modular design: easy to extend ETL steps  
- CLI and notebook-friendly  

---

## 📂 Repository Structure

```
elt_project/
│
├── data/
│ ├── orders.csv
│ ├── customers.csv
│ ├── products.csv
│ └── processed_orders.csv # Output from the transformation step
│
├── main.py # ELT orchestration script
├── requirements.txt # Python dependencies
├── elt_project.duckdb # DuckDB database file
└── README.md # This file
```

yaml


---

## 🛠️ Prerequisites
```
- Python 3.8+
- Java 8+ (for PySpark)
- `pip` or `conda` for package management
```
---

## ⚙️ Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-org/elt-project.git
   cd elt-project
Create a virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```
Install dependencies

```
pip install -r requirements.txt
requirements.txt:

pyspark>=3.0.0
duckdb>=0.7.0
pandas>=1.2.0
```
▶️ Usage
1. Configure your data
Place your CSVs into data/:

```
orders.csv

customers.csv

products.csv
```

Example schema for customers.csv:

csv
```
customer_id,customer_name,email
1,Jane Doe,jane.doe@example.com
2,John Smith,john.smith@example.com
2. Run the ELT Pipeline
```

python main.py
This will:

Extract with PySpark (reads data/*.csv)

Load into DuckDB (elt_project.duckdb)

Transform via SQL JOINs

Export data/processed_orders.csv

3. Inspect Results

head data/processed_orders.csv
Sample output:
```
order_id,customer_id,customer_name,email,product_id,product_name,category
1001,1,Jane Doe,jane.doe@example.com,200,Widget A,Gadgets
1002,2,John Smith,john.smith@example.com,201,Widget B,Gadgets
```
🧩 Code Snippet
```
import duckdb
from pyspark.sql import SparkSession

# Initialize Spark
spark = SparkSession.builder.appName("ELT with PySpark and DuckDB").getOrCreate()

# Extract
orders = spark.read.csv("data/orders.csv", header=True, inferSchema=True)
customers = spark.read.csv("data/customers.csv", header=True, inferSchema=True)
products = spark.read.csv("data/products.csv", header=True, inferSchema=True)

# Convert to Pandas
orders_df   = orders.toPandas()
customers_df= customers.toPandas()
products_df = products.toPandas()

# Load & Transform in DuckDB
con = duckdb.connect("elt_project.duckdb")
con.register("orders_df", orders_df)
con.register("customers_df", customers_df)
con.register("products_df", products_df)

# Recreate tables
con.execute("DROP TABLE IF EXISTS orders, customers, products")
con.execute("CREATE TABLE orders    AS SELECT * FROM orders_df")
con.execute("CREATE TABLE customers AS SELECT * FROM customers_df")
con.execute("CREATE TABLE products  AS SELECT * FROM products_df")

# Transform
sql = '''
SELECT
  o.order_id,
  c.customer_id,
  c.customer_name,
  o.email,
  p.product_id,
  p.product_name,
  p.category
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products  p ON o.product_id  = p.product_id
'''
result = con.execute(sql).df()

# Export
result.to_csv("data/processed_orders.csv", index=False)

# Cleanup
con.close()
spark.stop()
```
🔮 Future Roadmap
Streaming Ingestion

Integrate Kafka for real-time order streaming.

Delta Lake Support

Incremental loads, time travel, and ACID compliance.

Containerization

Dockerize Spark + DuckDB for reproducible deployments.

Orchestration

Add Airflow or Prefect to schedule and monitor jobs.

Data Quality Checks

Integrate Great Expectations for schema & anomaly detection.

🤝 Contributing
Fork the repository

Create a feature branch

Submit a PR with tests and documentation

Let’s build a future-proof ELT together!

