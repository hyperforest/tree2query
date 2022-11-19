import sys

DEBUG = False

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

    if not DEBUG:
        print('SELECT', end='')

    for i, row in enumerate(rule):
        row = row.strip()

        depth = row.count('|')
        indent = depth * spacing        
        else_flag = False
        
        if depth > stack[-1]:
            stack.append(depth)
        else:
            else_flag = True
            if depth < stack[-1]:
                stack.pop()
                while stack[-1] != depth:
                    if not DEBUG:
                        text = '\n' + ' ' * tab * stack[-1] + 'END'
                        print(text, end='')
                    stack.pop()
        
        if DEBUG:
            print(row, stack)

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
                    after = '\n' + ' ' * spacing * (depth - 1) + 'END'
            
            text = f" {text}{after}"
            
            if not DEBUG:
                print(text, end='')
        else:
            end, text = '', ''
            if else_flag:
                text = '\n' + ' ' * indent + 'ELSE'
                if not DEBUG:
                    print(text, end='')
            else:
                start_idx = (spacing + 1) * depth + 1
                text = row[start_idx:]
                text = f"\n{' ' * indent}{end}CASE WHEN {text} THEN"
                if not DEBUG:
                    print(text, end='')

    if DEBUG:
        print(stack)
    else:
        if stack[-1] > 1:
            text = '\n' + ' ' * spacing * stack[-1] + 'END'
            print(text, end='')
        
        print(f"\n{' ' * spacing}END AS {column_name}")
        print(f"FROM {src_table}")
    sys.stdout = OUT
