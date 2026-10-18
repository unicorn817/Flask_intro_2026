from flask import Flask, abort, render_template, request
from linked_list import LinkedList
from stack import (
    Stack,
    decimal_to_base,
    evaluate_postfix,
    infix_to_postfix,
    reverse_string,
)

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/works', methods=['GET', 'POST'])
def works():
    return render_template('works.html')

@app.route('/works/area/circle', methods=['GET', 'POST'])
def acircle():
    result = None
    if request.method == 'POST':
        radius = request.form.get('radius', '')

        if radius:
            result = float(radius) * 3.14 * float(radius)
    return render_template('circle.html', result=result)

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

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
