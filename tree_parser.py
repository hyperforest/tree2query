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
        else_flag = False
        
        if depth > stack[-1]:
            stack.append(depth)
        else:
            else_flag = True
            if depth < stack[-1]:
                stack.pop()
                while stack[-1] != depth:
                    text = f"\n{' ' * tab * stack[-1]}END"
                    _print(text)
                    stack.pop()
        
        _debug(row, stack)

        # infer node type
        node_type = 'leaf'
        if (row.count('<') > 0) | (row.count('>') > 0):
            node_type = 'split'

        text = ''
        if node_type == 'leaf':
            stack.pop()

            # infer task
            if task_type == '':
                if row.find('class') != -1:
                    task_type = 'classification'
                else:
                    task_type = 'regression'
            
            # infer value
            start_idx = row.index(':') + 1
            if task_type == 'regression':
                text = row[start_idx + 2:-1]
            else:
                text = row[start_idx + 1:]
            
            after = '' # handle cases to put END
            if i < len(rule) - 1:
                if rule[i + 1].count('|') <= stack[-2]:
                    after = f"\n{' ' * tab * (depth - 1)}END"
            
            text = f" {text}{after}"
            _print(text)
        else: # split/internal node
            text = ''
            if else_flag:
                text = f"\n{' ' * indent}ELSE"
                _print(text)
            else:
                start_idx = depth * spacing + depth + 1
                text = row[start_idx:]
                text = f"\n{' ' * indent}CASE WHEN {text} THEN"
                _print(text)

    _debug(stack)
    
    while stack[-1] > 0:
        text = f"\n{' ' * tab * stack[-1]}END"
        if stack[-1] == 1:
             text += f" AS {column_name}\nFROM {src_table};\n"

        _print(text)
        stack.pop()
    
    sys.stdout = OUT
