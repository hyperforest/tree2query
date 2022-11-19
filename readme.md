# tree2query

Simple app to convert an text-exported Scikit-Learn decision tree into a SQL query.

<img src="example.png" alt="example" width="800"/>

# Usage

```bash
usage: main.py [-h] [-p PATH] [-s SAVE_TO] [-c COLUMN_NAME] [-t SRC_TABLE] [-b TAB]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  path of exported text for sklearn tree
  -s SAVE_TO, --save_to SAVE_TO
                        file name to save query
  -c COLUMN_NAME, --column_name COLUMN_NAME
                        column name of the parsed tree
  -t SRC_TABLE, --src_table SRC_TABLE
                        source table name, i.e. X in `SELECT * FROM X`
  -b TAB, --tab TAB     indentation of the query
```

# Example

```bash
python main.py -p ./sample/classification_tree.txt -s ./sample/classification_tree.sql -c my_column -t dev_table -b 4
```

Output:

```sql
SELECT
CASE WHEN petal width (cm) <= 0.80 THEN 0
ELSE
   CASE WHEN petal width (cm) <= 1.75 THEN 1
   ELSE 2 END AS my_column
FROM dev_table
```

# Current Limitations
- Only supports numerical features
- Only supports decision tree
- Features should only contains letters, numbers, and underscores

# TODO
- Support categorical features
- Support multiple trees (random forest, gradient boosting, etc.)
