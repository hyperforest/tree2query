SELECT
   CASE WHEN petal width (cm) <= 0.80 THEN 0
   ELSE
      CASE WHEN petal width (cm) <= 1.75 THEN 1
      ELSE 2
      END
   END AS value
FROM my_table;
