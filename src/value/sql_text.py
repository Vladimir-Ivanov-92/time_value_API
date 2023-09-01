minute_aggregated_sql = """
                SELECT 
                    date_trunc('minute', "time") as minute,
                    ROUND(AVG("value")::NUMERIC, 2) as average_value,
                    MAX("value") as max_value,
                    MIN("value") as min_value
                FROM "value"
                GROUP BY date_trunc('minute', "time")
                ORDER BY date_trunc('minute', "time");
            """
