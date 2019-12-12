import requests

url_base = 'http://localhost:3600'


data = {'name': 'Dunder Mifflin'}
response = requests.post(url_base + '/new', json = data)

index = int(response.json().get('id'))

data = {
    'book_id': index,
    'entry_data': {
        'first_name': 'Kevin',
        'last_name': 'Conte',
        'custom_fields': {
            'notes': {
                'label': 'Notes',
                'value': 'drinks too many energy drinks',
                'global': False,
                'applied_globally': False
            }
        }
    }
}
response = requests.post(url_base + '/new_entry', json = data)

data = {
    'book_id': index,
    'entry_data': {
        'first_name': 'Kevin',
        'last_name': 'Alpha',
        'custom_fields': {
            'notes': {
                'label': 'Notes',
                'value': 'drinks too many energy drinks',
                'global': False,
                'applied_globally': False
            }
        }
    }
}
response = requests.post(url_base + '/new_entry', json = data)
response = requests.post(url_base + '/book', json = {'id': index})
print(response.json())



# failed_tests = []

# def get_result(response, expected):
#     response = sorted(response)
#     expected = sorted(expected)
#     if response == expected:
#         return 'PASSED'
#     else:
#         return 'FAILED'

# # /
# print('/:')
# print('==')

# url = url_base + '/'

# print('URL:', url, end = '\n\n')

# data = {}
# response = requests.post(url, json = data)

# test_result = get_result(response.json(),
#     { 'code': 0, 'message': 'success', 'result': ['entry_id', 'address_book_id', 'first_name', 'last_name', 'address_line_one', 'address_line_two', 'city', 'state', 'zip', 'phone', 'email'] })
# if test_result == 'FAILED':
#     failed_tests.append('/, test 1')

# print('---  1  ---\n')
# print('  request: ', str(data))
# print('  response:', str(response.json()), end = '\n\n')
# print('--- ', test_result, ' ---')
# print('\n\n\n================================================================================\n\n\n')

# # /new
# # ----
# print('/new:')
# print('=====')

# url = url_base + '/new'
# print('URL:', url, end = '\n\n')
# data = {'name': 'Dunder Mifflin'}
# response = requests.post(url, json = data)
# test_result = get_result(response.json(),
#     {'code': 0, 'message': 'success', 'id': 0})
# if test_result == 'FAILED':
#     failed_tests.append('/new, test 1')
# print('---  1  ---\n')
# print('  request: ', str(data))
# print('  response:', str(response.json()), end = '\n\n')
# print('--- ', test_result, ' ---')
# print('\n\n\n')

# data = {}
# response = requests.post(url, json = data)
# test_result = get_result(response.json(),
#     {'code': -3, 'message': 'name must be provided', 'id': -1})
# if test_result == 'FAILED':
#     failed_tests.append('/new, test 2')
# print('---  2  ---\n')
# print('  request: ', str(data))
# print('  response:', str(response.json()), end = '\n\n')
# print('--- ', test_result, ' ---')
# print('\n\n\n')

# data = {'name': ''}
# response = requests.post(url, json = data)
# test_result = get_result(response.json(),
#     {'code': -2, 'message': 'name cannot be empty', 'id': -1})
# if test_result == 'FAILED':
#     failed_tests.append('/new, test 3')
# print('---  3  ---\n')
# print('  request: ', str(data))
# print('  response:', str(response.json()), end = '\n\n')
# print('--- ', test_result, ' ---')
# print('\n\n\n================================================================================\n\n\n')


# # =============================================================================

# url = url_base + '/open'
# data = {'filename': './test_data/sample_input.json'}
# response = requests.post(url, json = data)
# print(response.json())

# url = url_base + '/book'
# data = {'book_id': response.json().get('id')}
# response = requests.post(url, json = data)
# print(response.json())

# if len(failed_tests) > 0:
#     print('Failed Tests:')
#     for test in failed_tests:
#         print('   ', test)
# else:
#     print('All tests passed\n\n\n')