SELECT
    CASE WHEN feature_0 <= 16 THEN
        CASE WHEN feature_4 <= 54 THEN
            CASE WHEN feature_3 <= 60 THEN
                CASE WHEN feature_1 <= 89 THEN
                    CASE WHEN feature_3 <= 48 THEN
                        CASE WHEN feature_3 <= 32 THEN 42
                        ELSE 36
                        END
                    ELSE 76
                    END
                ELSE
                    CASE WHEN feature_2 <= 15 THEN 10
                    ELSE
                        CASE WHEN feature_2 <= 57 THEN 52
                        ELSE 45
                        END
                    END
                END
            ELSE 22
            END
        ELSE 10
        END
    ELSE 92
    END AS value
FROM my_table
