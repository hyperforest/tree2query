import sys

def parse_tree(path, save_to='query.sql', column_name='value', src_table='my_table', tab=4):
    OUT = sys.stdout
    sys.stdout = open(save_to, 'w')

    with open(path, 'r') as f:
        rule = f.readlines()

    spacing = rule[0].index(' ') - 1
    task_type = ''
    node_type = 'split'
    stack = [0]

    print('SELECT', end='')

    for i, row in enumerate(rule):
        row = row.strip()

        depth = row.count('|')
        indent = depth * spacing
        
        end_flag = False
        else_flag = False
        if (depth < stack[-1]):
            end_flag = True
            stack.pop()
            while stack[-1] != depth:
                print('\n' + ' ' * tab * (stack[-1] - 1) + 'END', end='')
                stack.pop()
        elif depth > stack[-1]:
            stack.append(depth)
        else:
            else_flag = True
        # print(row, stack)
        node_type = 'leaf'
        if (row.count('<') > 0) | (row.count('>') > 0):
            node_type = 'split'

        text = ''
        if node_type == 'leaf':
            if task_type == '':
                if row.find('class') != -1:
                    task_type = 'classification'
                else:
                    task_type = 'regression'
            
            start_idx = row.index(':') + 1

            if task_type == 'regression':
                text = row[start_idx + 2:-1]
            else:
                text = row[start_idx + 1:]
            
            stack.pop()
            after = ''
            if i < len(rule) - 1:
                if rule[i + 1].count('|') <= stack[-2]:
                    after = '\n' + ' ' * spacing * (depth - 2) + 'END'
            print(f" {text}{after}", end='')
        else:
            end = ''
            if end_flag or else_flag:
                end = '\n' + ' ' * (indent - spacing) + 'ELSE'
                print(end, end='')
            else:
                start_idx = (spacing + 1) * depth + 1
                text = row[start_idx:]
                text = f"\n{' ' * (indent - spacing)}{end}CASE WHEN {text} THEN"
                print(text, end='')

    print(f" END AS {column_name}")
    print(f"FROM {src_table}")
    sys.stdout = OUT
