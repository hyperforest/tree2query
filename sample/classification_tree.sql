SELECT
CASE WHEN petal width (cm) <= 0.80 THEN 0
ELSE
   CASE WHEN petal width (cm) <= 1.75 THEN 1
   ELSE 2 END AS my_column
FROM dev_table
