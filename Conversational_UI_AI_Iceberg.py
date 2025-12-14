import streamlit as st
from snowflake.snowpark import Session
import pandas as pd

# --------------------------------------------------
# Create Snowflake session
# --------------------------------------------------
session = Session.builder.getOrCreate()

# --------------------------------------------------
# Streamlit UI Setup
# --------------------------------------------------
st.set_page_config(page_title="AI Conversational Iceberg SQL", layout="wide")
st.title("💬 Conversational Data Engineering for Iceberg Tables")
st.caption("Ask natural language questions. Snowflake Cortex generates safe SQL for your Iceberg table.")

st.markdown("### ❓ Ask a question about the Iceberg table `ORDERS_ICEBERG`:")
prompt = st.text_input("Example: Show total order amount by customer", "")

run_query = st.button("Run Query")

# ========================================================================
# RUN WHEN USER CLICKS BUTTON
# ========================================================================
if run_query and prompt.strip():

    # --------------------------------------------------
    # 1. Generate SQL using Cortex AI
    # --------------------------------------------------
    st.markdown("## 🔍 Generating SQL using Cortex AI...")

    cortex_prompt = (
        "You are an expert Snowflake SQL generator. "
        "Return ONLY valid SQL. No markdown, no explanation. "
        "Use ONLY this table and ONLY these columns:\n"
        "SANDBOX_DB.ICEBERG_DEMO.ORDERS_ICEBERG(\n"
        "  ORDER_ID,\n"
        "  CUSTOMER_NAME,\n"
        "  CUSTOMER_EMAIL,\n"
        "  ORDER_TOTAL,\n"
        "  CREATED_AT\n"
        ").\n"
        "If the user references incorrect or unknown column names, "
        "rewrite the SQL using the closest valid column names.\n"
        f"User request: {prompt}"
    )

    df_sql = session.sql(f"""
        SELECT SNOWFLAKE.CORTEX.COMPLETE(
            'mistral-large',
            '{cortex_prompt}'
        ) AS SQL_TEXT
    """).to_pandas()

    generated_sql = df_sql["SQL_TEXT"][0]

    # Clean any accidental markdown fences
    generated_sql = (
        generated_sql.replace("```sql", "")
                     .replace("```", "")
                     .strip()
    )

    st.code(generated_sql, language="sql")

    # --------------------------------------------------
    # 2. SQL GOVERNANCE (safety layer)
    # --------------------------------------------------
    st.markdown("## 🧠 Executing SQL safely...")

    lower_sql = generated_sql.lower()

    forbidden = ["drop ", "alter ", "truncate ", "delete ", "update ", "insert "]
    if any(f in lower_sql for f in forbidden):
        st.error("❌ Dangerous SQL detected. Query blocked for safety.")
        st.stop()

    required_table = "sandbox_db.iceberg_demo.orders_iceberg"
    if required_table not in lower_sql:
        st.error(
            f"❌ SQL must reference only `{required_table}`.\n"
            "Your query was blocked for safety."
        )
        st.stop()

    # --------------------------------------------------
    # 3. Execute SQL + Display Results
    # --------------------------------------------------
    try:
        results_df = session.sql(generated_sql).to_pandas()
        st.success("Query executed successfully! 🎉")
        st.dataframe(results_df, use_container_width=True)

        # Optional Charts
        numeric_cols = results_df.select_dtypes(include=["float64", "int64"]).columns
        if len(numeric_cols) >= 1:
            st.markdown("### 📊 Auto Chart (Numeric Columns Found)")
            st.line_chart(results_df[numeric_cols])

    except Exception as e:
        st.error(f"❌ Error executing SQL:\n\n{str(e)}")
