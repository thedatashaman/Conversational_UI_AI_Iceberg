CREATE OR REPLACE PROCEDURE SANDBOX_DB.ICEBERG_DEMO.GENERATE_SQL(prompt STRING)
RETURNS STRING
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE result STRING;

BEGIN
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large',
        'Generate valid Snowflake SQL using only table SANDBOX_DB.ICEBERG_DEMO.ORDERS_ICEBERG. '
        || 'Use fully qualified names. User request: ' || :prompt
    )
    INTO :result;

    RETURN result;
END;
$$;

CALL SANDBOX_DB.ICEBERG_DEMO.GENERATE_SQL('show total order_total by customer_name');
