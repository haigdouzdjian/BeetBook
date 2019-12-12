import json

from utils import *

'''
class Entry

Represents an entry in an Address Book.
'''
class Entry:
    def __init__(self, key_values = {}, default_custom_fields = {}):
        # ensure that the default properties exist in the entry.
        self.values = {
            'entry_id': '',
            'address_book_id': '',
            'first_name': '',
            'last_name': '',
            'address_line_one': '',
            'address_line_two': '',
            'city': '',
            'state': '',
            'zip': '',
            'phone': '',
            'email': '',
            'custom_fields' : default_custom_fields
        }

        for key, value in key_values.items():
            self.set_value(key, value)

        #log(''.join(('Created Entry: ', str(self))))

    def __hash__(self):
        list_of_items = []
        for key, value in self.values.items():
            if key != 'custom_fields':
                list_of_items.append(value)
        for key, value in self.values.get('custom_fields').items():
            for item in value.values():
                list_of_items.append(item)
        return hash(tuple(list_of_items))

    def __str__(self):
        return json.dumps(self.values, sort_keys = False)

    def get_value(self, key):
        return self.values.get(key)

    def set_values(self, entry_data = {}):
        try:
            self.values.update(entry_data)
            return True
        except:
            return False

    def set_value(self, key, value):
        try:
            self.values.update({key: value})
            return True
        except:
            return False

    def get_values(self):
        return self.values
