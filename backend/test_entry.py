import unittest

import entry as EntryClass

class TestEntry(unittest.TestCase):

    entry = EntryClass.Entry()

    # str()
    def test_0_str(self):
        print('Testing __str__()')
        string = str(self.entry)
        self.assertEqual(string, '{"entry_id": "", "address_book_id": "", "first_name": "", "last_name": "", "address_line_one": "", "address_line_two": "", "city": "", "state": "", "zip": "", "phone": "", "email": "", "custom_fields": {}}')

    # set_value()
    def test_1_set_value(self):
        print('\n\nTesting set_value()')
        self.assertTrue(self.entry.set_value('first_name', 'Kevin'))
        self.assertTrue(self.entry.set_value('custom_fields', { 'notes': { 'label': 'Notes', 'value': 'These are some notes.', 'global': True, 'applied_globally': True } }))
        print(self.entry)

    # set_values()
    def test_2_set_values(self):
        print('\n\nTesting set_values()')
        self.assertTrue(self.entry.set_values({'first_name': 'Kevin', 'last_name': 'Conte'}))
        print(self.entry)

    # get_value()
    def test_3_get_value(self):
        print('\n\nTesting get_value()')
        self.assertEqual('Kevin', self.entry.get_value('first_name'))

    # get_values()
    def test_4_get_values(self):
        print('\n\nTesting get_values()')
        reference = {'entry_id': '', 'address_book_id': '', 'first_name': 'Kevin', 'last_name': 'Conte', 'address_line_one': '', 'address_line_two': '', 'city': '', 'state': '', 'zip': '', 'phone': '', 'email': '', 'custom_fields': {'notes': {'label': 'Notes', 'value': 'These are some notes.', 'global': True, 'applied_globally': True}}}
        self.assertEqual(reference, self.entry.get_values())
        print(self.entry)

    # hash()
    def test_5_hash(self):
        print('\n\nTesting __hash__()')
        initial_hash = hash(self.entry)
        self.entry.set_value('first_name', 'John')
        self.entry.set_value('last_name', 'Doe')
        post_hash = hash(self.entry)
        print(initial_hash)
        print(post_hash)
        self.assertNotEqual(initial_hash, post_hash)

if __name__ == "__main__":
    unittest.main()
