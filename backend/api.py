from utils import *
import sys
import addressBook
from entry import Entry
from app import App
from flask import Flask, redirect, request, jsonify
import json
server = Flask(__name__)
app = App()

def create_json(**kwargs):
    obj = {
        'code': 0,
        'message': ''
    }
    for key,value in kwargs.items():
        obj[key] = value
    return obj

@server.route('/', methods = ['POST'])
def root_route():
    response = create_json(result = app.get_default_fields())
    log('response: {}'.format(str(response)))
    return jsonify(response)

@server.route('/new', methods = ['POST'])
def create_address_book():
    name = request.get_json().get('name')
    if name is not None:
        if name != '':
            book_id = app.create_address_book(name)
            log('book id: ' + str(book_id))
            if book_id >= 0:
                response = create_json(message = 'success', id = book_id)
            else:
                response = create_json(code = -1, message = 'could not create new address book', id = -1)
        else:
            response = create_json(code = -2, message = 'name cannot be empty', id = -1)
    else:
        response = create_json(code = -3, message = 'name must be provided', id = -1)
    log('response: {}'.format(str(response)))
    return jsonify(response)

@server.route('/open', methods = ['POST'])
def open_address_book():
    log(request)
    filename = str(request.get_json().get('filename'))
    if filename is not None:
        if filename != '':
            book_id = app.open_address_book(filename)
            if book_id < 0:
                response = create_json(code = -1, message = 'error opening file: {}'.format(filename), id = book_id)
            else:
                response = create_json(message= 'success', id = book_id)
        else:
            response = create_json(code = -2, message = 'filename cannot be empty', id = -1)
    else:
        response = create_json(code = -3, message = 'filename must be provided', id = -1)
    log('response: {}'.format(str(response)))
    log(json.dumps(response))
    return jsonify(json.dumps(response))

@server.route('/import', methods = ['POST'])
def import_address_book():
    data = request.get_json()
    filename = data.get('filename')
    try:
        book_id = int(data.get('id'))
    except:
        response = create_json(code = -1, message = 'id is not an int')
        log('response: {}'.format(str(response)))
        return jsonify(response)
    valid = app.check_address_book_id(book_id)
    if valid == False:
        response = create_json(code = -2, message = 'id does not correspond to an open address book')
    else:
        if filename is not None:
            if filename != '':
                result = app.import_tsv(book_id, filename)
                if result < 0:
                    response = create_json(code = result, message = 'error importing file: {}'.format(filename), id = book_id)
                else:
                    response = create_json(message = 'success', id = book_id)
            else:
                response = create_json(code = -3, message = 'filename cannot be empty', id = book_id)
        else:
            response = create_json(code = -4, message = 'filename must be provided', id = book_id)
    log('response: {}'.format(str(response)))
    return jsonify(response)

@server.route('/book', methods = ['POST'])
def get_address_book():
    try:
        book_id = int(request.get_json().get('id'))
    except:
        response = create_json(code = -1, message = 'id is not an int')
        log('response: {}'.format(str(response)))
        return jsonify(response)
    valid = app.check_address_book_id(book_id)
    if valid == True:
        response = create_json(message = 'success', result = app.get_address_book(book_id))
    else:
        response = create_json(code = -2, message = 'id does not correspond to an open address book')
    log('response: {}'.format(str(response)))
    return jsonify(response)

@server.route('/new_entry', methods = ['POST'])
def create_entry():
    data = request.get_json()
    log('data: ' +  str(data))
    book_id = int(data.get('book_id'))
    # try:
    #     book_id = int(data.get('book_id'))
    # except:
    #     response = create_json(code = -1, message = 'id is not an int', id = -1)
    #     log('response: {}'.format(str(response)))
    # valid = app.check_address_book_id(book_id)
    # if valid == False:
    #     response = create_json(code = -2, message = 'id does not correspond to an open address book', id = book_id)
    #     log('response: {}'.format(str(response)))
    #     return jsonify(response)
    # try:
    #     log('data: {}'.format(str(data.get('entry_data'))))
    #     entry_data = data.get('entry_data')
    #     # if entry_data['address_line_one'] == '' or entry_data['city'] == '' or entry_data['state'] == '' or entry_data['zip'] == '':
    #     #     response = create_json(code = -5, message = 'address not in compliance with USPS standards')
    #     #     log('response: {}'.format(str(response)))
    #     #     return jsonify(response)
    # except:
    #     response = create_json(code = -3, message = 'error creating new entry', id = book_id)
    #     log('response: {}'.format(str(response)))
    #     return jsonify(response)
    new_entry = data.get('entry_data')
    log('response: {}'.format(str(new_entry)))
    success = app.create_entry(book_id, new_entry)
    log('response: {}'.format(str(success)))
    if success == True:
        response = create_json(message = 'success', id = book_id)
    else:
        response = create_json(code = -4, message = 'error adding new entry to address book', id = book_id)
    log('response: {}'.format(str(response)))
    return jsonify(response)

@server.route('/close', methods = ['POST'])
def close_address_book():
    data = request.get_json()
    try:
        book_id = int(data.get('id'))
    except:
        response = create_json(code = -1, message = 'id is not an int', id = -1)
        log('response: {}'.format(str(response)))
        return jsonify(response)
    try:
        force = bool(data.get('force'))
    except:
        response = create_json(code = -2, message = 'force is not a bool')
        log('response: {}'.format(str(response)))
        return jsonify(response)
    success = app.close_address_book(book_id, force)
    if success == False:
        response = create_json(code = 3, message = 'changes have been made, please save before closing', id = book_id)
    else:
        response = create_json(message = 'success')
    log('response: {}'.format(str(response)))
    return jsonify(response)

@server.route('/save', methods = ['POST'])
def save_address_book():
    log(request.get_json())
    data = request.get_json()
    try:
        book_id = int(data.get('id'))
    except:
        response = create_json(code = -1, message = 'id is not an int')
        log('response: {}'.format(str(response)))
        return jsonify(response)
    filename = data.get('filename')
    if filename is not None and filename == '':
        response = create_json(code = -2, message = 'filename cannot be empty', id = book_id)
        log('response: {}'.format(str(response)))
        return jsonify(response)
    elif filename is None:
        filename = ''

    book_name = data.get('book_name')
    app.update_book_name(book_id, book_name)
    result = app.save_address_book(book_id, filename)
    if result == 1:
        response = create_json(code = -3, message = 'no file associated with id', id = book_id)
    elif result == 2:
        response = create_json(code = -4, message = 'file io error', id = book_id)
    else:
        response = create_json(message = 'success', id = book_id)
    log('response: {}'.format(str(response)))
    return jsonify(response)

@server.route('/delete_entry', methods = ['POST'])
def delete_entry():
    data = request.get_json()
    try:
        book_id = int(data.get('book_id'))
    except:
        response = create_json(code = -1, message = 'book_id is not an int', book_id = -1, entry_id = -1)
        log('response: {}'.format(str(response)))
        return jsonify(response)
    try:
        entry_id = int(data.get('entry_id'))
    except:
        response = create_json(code = -2, message = 'entry_id is not an int', book_id = -1, entry_id = -1)
        log('response: {}'.format(str(response)))
        return jsonify(response)
    valid = app.check_address_book_id(book_id)
    if valid == False:
        response = create_json(code = -3, message = 'no open address book associated with book_id', book_id = book_id, entry_id = entry_id)
        log('response: {}'.format(str(response)))
        return jsonify(response)
    valid = app.check_entry_id(book_id, entry_id)
    if valid == False:
        response = create_json(code = -4, message = 'no entry with entry_id', book_id = book_id, entry_id = entry_id)
        log('response: {}'.format(str(response)))
        return(jsonify(response))
    success = app.delete_entry(book_id, entry_id)
    if success == False:
        response = create_json(code = -5, message = 'error deleting entry, unknown reason', book_id = book_id, entry_id = entry_id)
    else:
        response = create_json(message = 'succes', book_id = book_id)
    log('response: {}'.format(str(response)))
    return jsonify(response)

@server.route('/edit_entry', methods = ['POST'])
def edit_entry():
    log(request)
    data = request.get_json()
    entry_data = data.get('entry_data')
    if entry_data == None:
        response = create_json(code = -1, message = 'no data provided', entry_data = {})
        log('response: {}'.format(str(response)))
        return jsonify(response)
    book_id = entry_data.get('address_book_id')
    entry_id = entry_data.get('entry_id')

    valid = app.check_address_book_id(book_id)
    if valid == False:
        response = create_json(code = -2, message = 'no open address book associated with entry\'s address_book_id')
        log('response: {}'.format(str(response)))
    valid = app.check_entry_id(book_id, entry_id)
    if valid == False:
        response = create_json(code = -3, message = 'no entry associated with entry_id')
        log('response: {}'.format(str(response)))
        return jsonify(response)
    success = app.update_entry(entry_data)
    if success == False:
        response = create_json(code = -4, message = 'could not update entry, unknown reason')
    else:
        response = create_json(message = 'success')
    log('response: {}'.format(str(response)))
    return jsonify(response)

@server.route('/export', methods = ['POST'])
def export_address_book():
    data = request.get_json()
    try:
        book_id = int(data.get('book_id'))
    except:
        response = create_json(code = -1, message = 'book_id is not an int', book_id = -1, filename = '', entry_ids = [])
        log('response: {}'.format(str(response)))
        return jsonify(response)
    filename = data.get('filename')
    if filename is None:
        response = create_json(code = -2, message = 'filename must be provided', book_id = book_id, filename = '', entry_ids = [])
        log('response: {}'.format(str(response)))
        return jsonify(response)
    if filename == '':
        response = create_json(code = -3, message = 'filename cannot be empty', book_id = book_id, filename = '',  entry_ids = [])
        log('response: {}'.format(str(response)))
        return jsonify(response)
    entry_ids = []
    if data.get('entry_ids') is not None:
        entry_ids = data.get('entry_ids').copy()
    success = app.export_tsv(book_id, filename, entry_ids)
    if success == False:
        response = create_json(code = -4, message = 'file io error', book_id = book_id)
    else:
        response = create_json(message = 'success', book_id = book_id)
    log('response: {}'.format(str(response)))
    return jsonify(response)

@server.route('/sort', methods = ['POST'])
def sort_address_book():
    log(request.get_json())
    data = request.get_json()
    try:
        book_id = int(data.get('id'))
    except:
        response = create_json(code = -1, message = 'id is not an int', book_id = -1, key = '', order_by = '')
        log('response: {}'.format(str(response)))
        return jsonify(response)
    key = data.get('sort_key')
    if key is not None:
        valid = True if key in ['last_name', 'zip'] else False
        if valid == False:
            response = create_json(code = -2, message = 'key is not valid', book_id = book_id, key = key, order_by = '')
            log('response: {}'.format(str(response)))
            return jsonify(response)
    else: key = 'Lname'
    order_by = data.get('order_by')
    if order_by is not None and order_by not in ['asc', 'des']:
        response = create_json(code = -3, message = 'order_by is not valid', book_id = book_id, key = key, order_by = order_by)
        log('response: {}'.format(str(response)))
        return jsonify(response)
    success = app.sort_address_book(book_id, key, order_by)
    if success == False:
        response = create_json(code = -4, message = 'could not sort address book, unknown reason', book_id = book_id)
    else:
        response = create_json(message = 'success', book_id = book_id)
    log('response: {}'.format(str(response)))
    return jsonify(response)


@server.route('/test/<string:msg>')
def test_route(msg):
    '''TEST ROUTE'''
    tmp = 'Python received ' + msg
    log(tmp, logging.INFO)
    res = 'Python says ' + msg
    return res


def main():
    '''
    Everything starts from here.
    '''

    setup_log()  # Logging
    log('Server running on port 3600', logging.INFO)
    server.run(host='localhost', port=3600, debug=True)


if __name__ == "__main__":
    main()
