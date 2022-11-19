import argparse
from tree_parser import parse_tree

def main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="path of exported text for sklearn tree")
    parser.add_argument(
        "-s",
        "--save_to", 
        default="query.sql",
        type=str,
        help="file name to save query")
    parser.add_argument(
        "-c",
        "--column_name", 
        default="value",
        help="column name of the parsed tree")
    parser.add_argument(
        "-t",
        "--src_table",
        default="my_table",
        help="source table name, i.e. X in `SELECT * FROM X`"
    )
    parser.add_argument(
        "-b",
        "--tab",
        default=4,
        type=int,
        help="indentation of the query"
    )

    args = parser.parse_args()
    path = args.path
    save_to = args.save_to
    column_name = args.column_name
    src_table = args.src_table
    tab = args.tab

    parse_tree(
        path=path,
        save_to=save_to,
        column_name=column_name,
        src_table=src_table,
        tab=tab
    )

if __name__ == "__main__":
    main()
