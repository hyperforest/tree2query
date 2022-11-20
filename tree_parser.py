import sys

DEBUG = False

def _debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def _print(*args, end='', **kwargs):
    if not DEBUG:
        print(*args, end=end, **kwargs)


def parse_tree(path, save_to='query.sql', column_name='value', src_table='my_table', tab=4):
    OUT = sys.stdout
    if not DEBUG:
        sys.stdout = open(save_to, 'w')

    with open(path, 'r') as f:
        rule = f.readlines()

    spacing = rule[0].index(' ') - 1
    task_type = ''
    node_type = 'split'
    stack = [0]

    _print('SELECT')

    for i, row in enumerate(rule):
        row = row.strip()

        depth = row.count('|')
        indent = depth * tab
        
        else_flag = _handle_else_flag(tab, stack, depth)
        _debug(row, stack)
        
        node_type = _get_node_type(row)
        if node_type == 'leaf':
            _process_leaf_node(tab, rule, task_type, stack, i, row, indent)
        else:
            _process_split_node(spacing, row, depth, indent, else_flag)

    _debug(stack)
    _post_process(column_name, src_table, tab, stack)
    sys.stdout = OUT


def _post_process(column_name, src_table, tab, stack):
    while stack[-1] > 0:
        prev_depth = stack[-1]
        text = f"\n{' ' * prev_depth * tab}END"
        if stack[-1] == 1:
             text += f" AS {column_name}\nFROM {src_table};\n"

        _print(text)
        stack.pop()


def _process_split_node(spacing, row, depth, indent, else_flag):
    text = ''
    if else_flag:
        text = f"\n{' ' * indent}ELSE"
        _print(text)
    else:
        start_idx = depth * spacing + depth + 1
        text = row[start_idx:]
        text = f"\n{' ' * indent}CASE WHEN {text} THEN"
        _print(text)


def _process_leaf_node(tab, rule, task_type, stack, i, row, indent):
    stack.pop()

    if task_type == '': # infer task
        task_type = _get_task_type(row)
            
            # infer value
    start_idx = row.index(':') + 1
    if task_type == 'regression':
        text = row[start_idx + 2:-1]
    else:
        text = row[start_idx + 1:]
            
    after = '' # handle cases to put an END
    if i < len(rule) - 1:
        if rule[i + 1].count('|') <= stack[-2]:
            after = f"\n{' ' * (indent - tab)}END"
            
    text = f" {text}{after}"
    _print(text)


def _get_task_type(row):
    if row.find('class') != -1:
        task_type = 'classification'
    else:
        task_type = 'regression'
    return task_type


def _get_node_type(row):
    node_type = 'leaf'
    if (row.count('<') > 0) | (row.count('>') > 0):
        node_type = 'split'
    return node_type


def _handle_else_flag(tab, stack, depth):
    else_flag = False
    if depth > stack[-1]:
        stack.append(depth)
    else:
        else_flag = True
        if depth < stack[-1]:
            stack.pop()
            while stack[-1] != depth:
                prev_depth = stack[-1]
                text = f"\n{' ' * prev_depth * tab}END"
                _print(text)
                stack.pop()
    return else_flag
