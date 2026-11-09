import json

# Flask tools used to create the application and handle web requests.
from flask import Flask, abort, render_template, request

# Data structures and algorithms implemented in separate Python files.
from binary_tree import BinaryTree, Node
from linked_list import LinkedList
from queue_deque import Deque, Queue
from sorting import SORT_ALGORITHMS, sort_values
from stack import (
    Stack,
    decimal_to_base,
    evaluate_postfix,
    infix_to_postfix,
    reverse_string,
)


# Application setup
app = Flask(__name__)


# General website pages
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/works', methods=['GET', 'POST'])
def works():
    return render_template('works.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


# Area calculators
@app.route('/works/area/circle', methods=['GET', 'POST'])
def acircle():
    result = None
    if request.method == 'POST':
        radius = request.form.get('radius', '')

        if radius:
            result = float(radius) * 3.14 * float(radius)
    return render_template('circle.html', result=result)


# Older circle-area example kept from the original project.
# @app.route('/areaOfcirle', methods=['GET', 'POST'])
# def areaOfcirle():
#     result = None
#     name=request.get('name','')
#     print(name)
#     if request.method == 'POST':
#         input_string = request.form.get('inputradius', '')
#         result = int(input_string) * int(input_string) * 3.14
#     return render_template('areaCircle.html', result=result)


@app.route('/works/area/triangle', methods=['GET', 'POST'])
def atriangle():
    result = None

    if request.method == 'POST':
        base = request.form.get('base', '')
        height = request.form.get('height', '')

        if base and height:
            result = 0.5 * float(base) * float(height)

    return render_template('triangle.html', result=result)


# Linked-list operations page
@app.route('/works/linked-list', methods=['GET', 'POST'])
def linked_list_page():
    values = request.form.getlist('items') if request.method == 'POST' else []
    linked_list = LinkedList()

    for item in values:
        linked_list.insert_at_end(item)

    message = None
    message_type = 'success'
    selected_action = 'insert_at_end'
    match_value = None

    if request.method == 'POST':
        selected_action = request.form.get('action', '')
        value = request.form.get('value', '').strip()
        target = request.form.get('target', '').strip()

        if selected_action == 'insert_at_end':
            if value:
                linked_list.insert_at_end(value)
                message = f'Added {value} to the end.'
            else:
                message = 'Enter a value to add.'
                message_type = 'error'
        elif selected_action == 'insert_at_beginning':
            if value:
                linked_list.insert_at_beginning(value)
                message = f'Added {value} to the beginning.'
            else:
                message = 'Enter a value to add.'
                message_type = 'error'
        elif selected_action == 'insert_after':
            if not value or not target:
                message = 'Enter both values to insert a node.'
                message_type = 'error'
            elif linked_list.insert_after(target, value) is None:
                message = f'No node contains {target}.'
                message_type = 'error'
            else:
                message = f'Added {value} after {target}.'
        elif selected_action == 'remove_beginning':
            removed = linked_list.remove_beginning()
            if removed is None:
                message = 'The list is already empty.'
                message_type = 'error'
            else:
                message = f'Removed {removed} from the beginning.'
        elif selected_action == 'remove_at_end':
            removed = linked_list.remove_at_end()
            if removed is None:
                message = 'The list is already empty.'
                message_type = 'error'
            else:
                message = f'Removed {removed} from the end.'
        elif selected_action == 'remove_value':
            removed = linked_list.remove_at(value) if value else None
            if removed is None:
                message = f'No node contains {value}.' if value else 'Enter a value to remove.'
                message_type = 'error'
            else:
                message = f'Removed the first node containing {removed}.'
        elif selected_action == 'search':
            found = bool(value) and linked_list.search(value)
            if found:
                message = f'Found {value} in the list.'
                match_value = value
            else:
                message = f'{value} is not in the list.' if value else 'Enter a value to search for.'
                message_type = 'error'
        else:
            message = 'Choose a valid list operation.'
            message_type = 'error'

    values = []
    current_node = linked_list.head
    while current_node:
        values.append(current_node.data)
        current_node = current_node.next

    return render_template(
        'linked_list.html',
        values=values,
        message=message,
        message_type=message_type,
        selected_action=selected_action,
        match_value=match_value,
    )


@app.route('/works/queue-deque', methods=['GET', 'POST'])
def queue_deque_page():
    structure = request.form.get('structure', 'queue')
    if structure not in {'queue', 'deque'}:
        structure = 'queue'

    values = request.form.getlist('items') if request.method == 'POST' else []
    data_structure = Queue() if structure == 'queue' else Deque()
    for item in values:
        if structure == 'queue':
            data_structure.enqueue(item)
        else:
            data_structure.add_rear(item)

    action = request.form.get('action', '')
    value = request.form.get('value', '').strip()
    message = None
    message_type = 'success'
    peek_result = None

    if request.method == 'POST':
        if action == 'clear':
            data_structure = Queue() if structure == 'queue' else Deque()
            message = f'Cleared the {structure}.'
        elif structure == 'queue':
            if action == 'enqueue':
                if value:
                    data_structure.enqueue(value)
                    message = f'Added {value} to the rear of the queue.'
                else:
                    message = 'Enter a value to enqueue.'
                    message_type = 'error'
            elif action == 'dequeue':
                removed = data_structure.dequeue()
                if removed is None:
                    message = 'The queue is empty; there is nothing to dequeue.'
                    message_type = 'error'
                else:
                    message = f'Removed {removed} from the front of the queue.'
            elif action == 'peek':
                front = data_structure.front()
                if front is None:
                    message = 'The queue is empty.'
                    message_type = 'error'
                else:
                    peek_result = ('Front of the queue', front)
            else:
                message = 'Choose a valid queue operation.'
                message_type = 'error'
        else:
            if action in {'add_front', 'add_rear'}:
                if value:
                    if action == 'add_front':
                        data_structure.add_front(value)
                        message = f'Added {value} to the front of the deque.'
                    else:
                        data_structure.add_rear(value)
                        message = f'Added {value} to the rear of the deque.'
                else:
                    message = 'Enter a value to add.'
                    message_type = 'error'
            elif action in {'remove_front', 'remove_rear'}:
                removed = (
                    data_structure.remove_front()
                    if action == 'remove_front'
                    else data_structure.remove_rear()
                )
                if removed is None:
                    message = 'The deque is empty; there is nothing to remove.'
                    message_type = 'error'
                else:
                    end = 'front' if action == 'remove_front' else 'rear'
                    message = f'Removed {removed} from the {end} of the deque.'
            elif action in {'peek_front', 'peek_rear'}:
                end = 'front' if action == 'peek_front' else 'rear'
                item = (
                    data_structure.peek_front()
                    if action == 'peek_front'
                    else data_structure.peek_rear()
                )
                if item is None:
                    message = 'The deque is empty.'
                    message_type = 'error'
                else:
                    peek_result = (f'{end.title()} of the deque', item)
            else:
                message = 'Choose a valid deque operation.'
                message_type = 'error'

    return render_template(
        'queue_deque.html',
        structure=structure,
        values=data_structure.to_list(),
        action=action,
        message=message,
        message_type=message_type,
        peek_result=peek_result,
    )


# Sorting algorithms page
@app.route('/works/sorting', methods=['GET', 'POST'])
def sorting_page():
    raw_values = request.form.get('values', '')
    requested_algorithm = request.form.get('algorithm', 'bubble')
    requested_order = request.form.get('order', 'ascending')
    algorithm = (
        requested_algorithm
        if requested_algorithm in SORT_ALGORITHMS
        else 'bubble'
    )
    order = (
        requested_order
        if requested_order in {'ascending', 'descending'}
        else 'ascending'
    )
    result = None
    message = None
    message_type = 'success'

    if request.method == 'POST':
        if request.form.get('action') == 'clear':
            raw_values = ''
            message = 'Cleared the sorting input.'
        elif requested_algorithm not in SORT_ALGORITHMS:
            message = 'Choose a valid sorting algorithm.'
            message_type = 'error'
        elif requested_order not in {'ascending', 'descending'}:
            message = 'Choose ascending or descending order.'
            message_type = 'error'
        else:
            try:
                tokens = raw_values.replace(',', ' ').split()
                if not tokens:
                    raise ValueError('Enter at least one whole number to sort.')
                try:
                    values = [int(value) for value in tokens]
                except ValueError as error:
                    raise ValueError(
                        'Enter whole numbers separated by commas or spaces.'
                    ) from error
                if len(values) > 100:
                    raise ValueError('Enter no more than 100 numbers at a time.')

                sorted_values, comparisons, moves = sort_values(
                    values,
                    algorithm,
                    descending=order == 'descending',
                )
                result = {
                    'values': sorted_values,
                    'comparisons': comparisons,
                    'moves': moves,
                    'algorithm': SORT_ALGORITHMS[algorithm]['title'],
                    'order': order,
                }
            except ValueError as error:
                message = str(error)
                message_type = 'error'

    return render_template(
        'sorting.html',
        algorithms=SORT_ALGORITHMS,
        algorithm=algorithm,
        order=order,
        raw_values=raw_values,
        result=result,
        message=message,
        message_type=message_type,
    )


# Binary tree operations page
@app.route('/works/binary-tree', methods=['GET', 'POST'])
def binary_tree_page():
    tree = BinaryTree()
    message = None
    message_type = 'success'
    traversal_result = None
    matched_value = None
    records = []
    selected_action = request.form.get('action', '') if request.method == 'POST' else ''
    try:
        zoom_percent = int(request.form.get('zoom_percent', '100'))
    except ValueError:
        zoom_percent = 100
    zoom_percent = max(10, min(100, zoom_percent))

    if request.method == 'POST':
        try:
            records = json.loads(request.form.get('tree_data', '[]'))
            if not isinstance(records, list) or len(records) > 50:
                raise ValueError('The tree data is invalid or exceeds 50 nodes.')

            nodes = []
            for index, record in enumerate(records):
                if not isinstance(record, dict) or not isinstance(record.get('value'), str):
                    raise ValueError('The saved tree data is invalid.')
                node = Node(record['value'])
                if index == 0:
                    if record.get('parent') is not None or record.get('side') is not None:
                        raise ValueError('The saved root node is invalid.')
                    tree.root = node
                else:
                    parent_index = record.get('parent')
                    side = record.get('side')
                    if (
                        not isinstance(parent_index, int)
                        or parent_index < 0
                        or parent_index >= index
                        or side not in {'left', 'right'}
                    ):
                        raise ValueError('The saved tree links are invalid.')
                    parent = nodes[parent_index]
                    if getattr(parent, side) is not None:
                        raise ValueError('The saved tree contains duplicate child links.')
                    setattr(parent, side, node)
                nodes.append(node)

            action = selected_action
            value = request.form.get('value', '').strip()
            parent_value = request.form.get('parent_value', '').strip()

            if action == 'set_root':
                if tree.root is not None:
                    raise ValueError('The tree already has a root. Clear it to start over.')
                if not value:
                    raise ValueError('Enter a value for the root node.')
                tree.root = Node(value)
                message = f'Set {value} as the root node.'
            elif action in {'insert_left', 'insert_right'}:
                if tree.root is None:
                    raise ValueError('Set a root node before adding children.')
                if len(nodes) >= 50:
                    raise ValueError('The tree can contain up to 50 nodes.')
                if not parent_value or not value:
                    raise ValueError('Enter both a parent value and a new node value.')
                parent = tree.search(tree.root, parent_value)
                if parent is None:
                    raise ValueError(f'No node contains {parent_value}.')
                side = 'left' if action == 'insert_left' else 'right'
                getattr(tree, action)(parent, value)
                message = f'Added {value} as the {side} child of {parent_value}.'
            elif action in {'preorder', 'inorder', 'postorder'}:
                if tree.root is None:
                    raise ValueError('The tree is empty.')
                traversal_methods = {
                    'preorder': tree.preorder_traversal,
                    'inorder': tree.inorder_traversal,
                    'postorder': tree.post_traversal,
                }
                traversal_result = traversal_methods[action](tree.root, '').split()
                message = f'{action.title()} traversal completed.'
            elif action == 'search':
                if tree.root is None:
                    raise ValueError('The tree is empty.')
                if not value:
                    raise ValueError('Enter a value to search for.')
                matched_node = tree.search(tree.root, value)
                if matched_node is None:
                    message = f'There is no such value in the existing tree: {value}.'
                    message_type = 'error'
                else:
                    matched_value = matched_node.value
                    message = f'Found {value} in the existing tree. Activate the highlighted node to stop it blinking.'
            elif action == 'delete':
                if tree.root is None:
                    raise ValueError('The tree is empty.')
                if not value:
                    raise ValueError('Enter a value to delete.')
                if tree.search(tree.root, value) is None:
                    message = f'{value} was not found in the tree.'
                    message_type = 'error'
                else:
                    tree.root = tree.delete_node(tree.root, value)
                    message = f'Deleted {value}. The deepest rightmost node replaced it.'
            elif action == 'clear':
                tree = BinaryTree()
                message = 'Cleared the binary tree.'
            else:
                raise ValueError('Choose a valid binary tree operation.')
        except json.JSONDecodeError:
            message = 'Saved tree data is invalid. Clear the tree and try again.'
            message_type = 'error'
        except ValueError as error:
            message = str(error)
            message_type = 'error'

    records = []
    if tree.root is not None:
        pending: list[tuple[Node, int | None, str | None]] = [
            (tree.root, None, None)
        ]
        while pending:
            node, parent_index, side = pending.pop(0)
            index = len(records)
            records.append({
                'value': node.value,
                'parent': parent_index,
                'side': side,
            })
            if node.left is not None:
                pending.append((node.left, index, 'left'))
            if node.right is not None:
                pending.append((node.right, index, 'right'))

    return render_template(
        'binary_tree.html',
        tree=tree,
        tree_data=json.dumps(records),
        node_count=len(records),
        message=message,
        message_type=message_type,
        selected_action=selected_action,
        traversal_result=traversal_result,
        matched_value=matched_value,
        zoom_percent=zoom_percent,
    )


# Descriptions for the stack tools, displayed on the stack pages.
STACK_TOOLS = {
    'stack': {
        'title': 'Stack Operations',
        'description': 'Practice the last-in, first-out rule by pushing, popping, and peeking at values.',
    },
    'decimal': {
        'title': 'Decimal Conversion',
        'description': 'Convert a decimal integer to binary, octal, hexadecimal, or any base from 2 to 36.',
    },
    'infix': {
        'title': 'Infix to Postfix',
        'description': 'Convert an arithmetic expression to postfix notation and evaluate the result.',
    },
    'reverse': {
        'title': 'Reverse a String',
        'description': 'Use a stack to read characters in last-in, first-out order and reverse the text.',
    },
}


# Stack overview and stack-based tool pages
@app.route('/works/stack')
def stack_page():
    return render_template('stack.html', tools=STACK_TOOLS)


@app.route('/works/stack/<tool>', methods=['GET', 'POST'])
def stack_tool_page(tool):
    tool_info = STACK_TOOLS.get(tool)
    if tool_info is None:
        abort(404)

    stack = Stack[str]()
    for item in request.form.getlist('stack_items'):
        stack.push(item)

    message = None
    message_type = 'success'
    result_lines = []
    result_title = 'Your result'
    postfix_result = None
    evaluation_result = None
    evaluation_note = None
    evaluate_requested = request.form.get('evaluate') == 'on'

    if request.method == 'POST':
        try:
            if tool == 'stack':
                action = request.form.get('action', '')
                if action == 'push':
                    value = request.form.get('stack_value', '').strip()
                    if not value:
                        raise ValueError('Enter a value to push onto the stack.')
                    stack.push(value)
                    message = f'Pushed {value} onto the stack.'
                elif action == 'pop':
                    value = stack.pop()
                    if value is None:
                        raise ValueError('The stack is empty; there is nothing to pop.')
                    message = f'Popped {value} from the stack.'
                elif action == 'peek':
                    value = stack.peek()
                    if value is None:
                        raise ValueError('The stack is empty; there is no top value.')
                    message = f'Top value: {value}.'
                elif action == 'clear':
                    stack = Stack()
                    message = 'The stack has been cleared.'
                else:
                    raise ValueError('Choose a valid stack operation.')
                result_title = 'Current stack'
            elif tool == 'decimal':
                raw_number = request.form.get('number', '').strip()
                if not raw_number:
                    raise ValueError('Enter a decimal integer to convert.')
                number = int(raw_number)
                base = int(request.form.get('base', ''))
                result_title = 'Converted number'
                result_lines.append(
                    f'{number} in base {base}: {decimal_to_base(number, base)}'
                )
            elif tool == 'infix':
                expression = request.form.get('expression', '')
                postfix_result = infix_to_postfix(expression)
                result_title = 'Converted postfix'
                if evaluate_requested:
                    try:
                        evaluation_result = evaluate_postfix(postfix_result)
                    except ValueError:
                        evaluation_note = 'Evaluation is available for numeric expressions only.'
            elif tool == 'reverse':
                text = request.form.get('reverse_text', '')
                result_title = 'Reversed string'
                result_lines.append(reverse_string(text))
        except (ValueError, ZeroDivisionError, OverflowError) as error:
            message = str(error)
            message_type = 'error'

    stack_values = list(stack)
    stack_items = list(reversed(stack_values))
    return render_template(
        'stack_tool.html',
        tool=tool,
        tool_info=tool_info,
        stack_values=stack_values,
        stack_items=stack_items,
        result_lines=result_lines,
        result_title=result_title,
        postfix_result=postfix_result,
        evaluation_result=evaluation_result,
        evaluation_note=evaluation_note,
        evaluate_requested=evaluate_requested,
        message=message,
        message_type=message_type,
        number=request.form.get('number', ''),
        base=request.form.get('base', '2'),
        expression=request.form.get('expression', ''),
        reverse_text=request.form.get('reverse_text', ''),
    )


# Start the Flask development server when this file is run directly.
if __name__ == "__main__":
    app.run(debug=True)
