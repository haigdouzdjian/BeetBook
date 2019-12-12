import unittest

import addressBook as AddressBookClass

class TestAddressBook(unittest.TestCase):
    address_book_one = AddressBookClass.AddressBook()
    address_book_two = AddressBookClass.AddressBook('test_data/sample_book_saved.json')

    '''
    Order of Tests
        + import_json - DONE
        + import_tsv - FIX
        + add_entry -> Andy Bernard - DONE
        + update_entry - DONE
        + delete_entry -> Andy Bernard - DONE
        + export_tsv -> all - DONE
        + export_tsv -> partial (Jim and Pam) - DONE
        + save
        + sort
    '''

    def test_0_import_json(self):
        filename = './test_data/sample_input.json'
        self.assertFalse(self.address_book_two.import_json())
        self.assertTrue(self.address_book_two.import_json(filename, 0))
        print(self.address_book_two)

    def test_1_import_tsv(self):
        filename = 'test_data/sample_input.tsv'
        self.assertFalse(self.address_book_two.import_tsv())
        self.assertFalse(self.address_book_two.import_tsv(''))
        self.assertTrue(self.address_book_two.import_tsv(filename,0))

    def test_2_add_entry(self):
        new_entry = AddressBookClass.Entry({'first_name': 'Andy'})
        self.assertFalse(self.address_book_two.add_entry())
        self.assertTrue(self.address_book_two.add_entry(new_entry))

    def test_3_update_entry(self):
        update = {'entry_id': 2, 'address_book_id': 0, 'first_name': 'Andy', 'last_name': 'Bernard',
            'address_line_one': '1234 Slough Ave', 'address_line_two': 'Suite 300', 'city': 'Scranton', 'state': 'PA', 'zip': '18505', 'phone': '(570) 123-4569', 'email': 'abernard@dundermifflin.com', 'custom_fields': {
                'notes': {'label': 'Notes', 'value': 'sings too much', 'global': False, 'applied_globally': False}}}
        self.assertFalse(self.address_book_two.update_entry())
        self.assertTrue(self.address_book_two.update_entry(update))

    def test_4_delete_entry(self):
        self.assertFalse(self.address_book_two.delete_entry())
        self.assertTrue(self.address_book_two.delete_entry(2))

    def test_5_export_tsv(self):
        filename_all = 'test_data/export_all.tsv'
        filename_partial = 'test_data/export_partial.tsv'
        id_list = [1, 2]
        self.assertTrue(self.address_book_two.export_tsv(filename_all))
        self.assertFalse(self.address_book_two.export_tsv())
        self.assertTrue(self.address_book_two.export_tsv(filename_partial, id_list))

    def test_6_save(self):
        self.assertTrue(self.address_book_two.save())
        self.assertFalse(self.address_book_one.save())
        self.assertTrue(self.address_book_one.save('test_data/empty_book.json'))

if __name__ == "__main__":
    unittest.main()