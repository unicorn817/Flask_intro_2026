from flask import Flask, render_template, request
from linked_list import LinkedList

app = Flask(__name__)

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

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
