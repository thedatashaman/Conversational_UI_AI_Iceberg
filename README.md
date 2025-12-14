# 💬 Conversational Data Engineering
**Powered by Streamlit + Snowflake Cortex AI + Iceberg Tables**

![Architecture Screenshot](./assets/architecture.png)

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-Native_in_Snowflake-FF4B4B?logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Snowflake-Iceberg_Enabled-29B5E8?logo=snowflake&logoColor=white" />
  <img src="https://img.shields.io/badge/Cortex_AI-NLP_to_SQL-2BBEA8?logo=snowflake&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" />
</p>

---

This project demonstrates how to build a natural-language conversational analytics system inside Snowflake. 
Users type questions like “show revenue by customer”, and Cortex AI automatically converts the request into SQL, 
a governance layer validates the SQL, and Snowflake executes the query against an Iceberg-backed table. 
The Streamlit interface runs natively inside Snowflake, requiring no external servers.

---

## 🚀 Key Capabilities

| Capability | Benefit |
|-----------|---------|
| Natural language → SQL | Business users query data without SQL |
| SQL governance layer | Prevents DROP/DELETE/UPDATE and enforces table scoping |
| Iceberg-backed table | Open, scalable data lakehouse storage |
| AI-generated column documentation | Automatic business-friendly data dictionary |
| Streamlit inside Snowflake | Secure, serverless UI |
| Synthetic dataset generator | Reproducible dataset with 10k rows |

---

## 🧱 High-Level Architecture

```text
     ┌─────────────────────┐       ┌─────────────────────────────┐
     │    User Query       │──────▶│ Streamlit Conversational UI │
     └─────────────────────┘       └──────────┬──────────────────┘
                                              │ Natural Language
                                              ▼
                                   ┌─────────────────────────────┐
                                   │   Cortex AI SQL Generator   │
                                   └──────────┬──────────────────┘
                                              │ Validated SQL
                                              ▼
                                   ┌─────────────────────────────┐
                                   │     SQL Governance Layer    │
                                   │  (safety + table scoping)   │
                                   └──────────┬──────────────────┘
                                              │ Approved SQL
                                              ▼
                                   ┌─────────────────────────────┐
                                   │      Iceberg Data Table     │
                                   └──────────┬──────────────────┘
                                              │ Query Results
                                              ▼
                                   ┌─────────────────────────────┐
                                   │ Streamlit Results + Charts  │
                                   └─────────────────────────────┘
```

---

## 📂 Repository Structure

```text
sql/
  01_environment_setup.sql
  02_create_orders_raw.sql
  03_create_iceberg_table.sql
  04_create_catalog_docs_table.sql
  05_create_catalog_docs_view.sql
  06_generate_sql_procedure.sql
  07_safe_execute_procedure.sql

streamlit/
  app.py

assets/
  architecture.png
  screenshot_query.png
  screenshot_results.png

README.md
```

---

## ⚙️ Setup Instructions

1. Run environment setup:
   sql/01_environment_setup.sql

2. Generate synthetic dataset:
   sql/02_create_orders_raw.sql

3. Create the Iceberg table:
   sql/03_create_iceberg_table.sql

4. Generate AI-based documentation:
   sql/04_create_catalog_docs_table.sql
   sql/05_create_catalog_docs_view.sql

5. Create NLP → SQL generator:
   sql/06_generate_sql_procedure.sql

6. Create governed SQL executor:
   sql/07_safe_execute_procedure.sql

---

## 🖥️ Streamlit Conversational UI

The main conversational UI is located at:
streamlit/app.py

It handles:
- User natural language input
- AI-generated SQL via Cortex
- SQL governance filtering
- Query execution
- Auto-rendered tables and charts

---

## 🧪 Example User Prompts

- show total order_total by customer_name
- show daily revenue
- rank customers by spend
- show trend of orders over time
- customers with more than 5 orders

---

## 🛠️ Extensibility

- Multi-table NLP query support
- AI explanations of results
- Automated dashboards
- Row-level governance
- Query rewriting optimizations

---

## 👤 Author

Dhaman Sehdev  
https://www.linkedin.com/in/thedatashaman/


---

## 👤 Medium Article Link
https://medium.com/@DhamanS/conversational-data-engineering-build-a-chat-interface-to-manipulate-iceberg-tables-using-82640a0860bc

---