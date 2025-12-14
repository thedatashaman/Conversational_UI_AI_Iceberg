CREATE OR REPLACE PROCEDURE SANDBOX_DB.ICEBERG_DEMO.SAFE_EXECUTE(prompt STRING)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = 3.10
PACKAGES = ('snowflake-snowpark-python')
EXECUTE AS CALLER
AS
$$
from snowflake.snowpark import Session

def main(session: Session, prompt: str):

    df = session.sql(f"""
        SELECT SNOWFLAKE.CORTEX.COMPLETE(
            'mistral-large',
            'Generate valid SQL using only SANDBOX_DB.ICEBERG_DEMO.ORDERS_ICEBERG. '
            'Use fully qualified names. User request: {prompt}'
        ) AS SQL_TEXT
    """).collect()

    generated_sql = df[0]["SQL_TEXT"]

    if not generated_sql:
        return {"status": "error", "reason": "Cortex returned no SQL"}

    lower_sql = generated_sql.lower()

    forbidden = ["drop ", "alter ", "truncate ", "delete ", "update ", "insert "]
    for f in forbidden:
        if f in lower_sql:
            return {
                "status": "blocked",
                "reason": f"Forbidden operation detected: {f.strip()}",
                "generated_sql": generated_sql
            }

    required_table = "sandbox_db.iceberg_demo.orders_iceberg"
    if required_table not in lower_sql:
        return {
            "status": "blocked",
            "reason": f"Generated SQL must reference only {required_table}",
            "generated_sql": generated_sql
        }

    try:
        rows = session.sql(generated_sql).collect()
        return {
            "status": "ok",
            "generated_sql": generated_sql,
            "rows": [r.as_dict() for r in rows]
        }
    except Exception as e:
        return {
            "status": "error",
            "generated_sql": generated_sql,
            "error": str(e)
        }
$$;
