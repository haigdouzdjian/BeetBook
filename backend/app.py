from entry import Entry
from addressBook import AddressBook
from utils import *


class App:
    def __init__(self):
        self.open_address_books = {}
        self.address_book_count = 0
        self.default_fields = []
        self.filename = ''

    def check_address_book_id(self,book_id):
        if book_id in self.open_address_books.keys():
            return True
        else:
            return False

    def check_entry_id(self, book_id, entry_id):
        return self.open_address_books.get(book_id).get('object').check_entry_id(entry_id)

    def get_default_fields(self):
        entry = Entry()
        entry = entry.get_values()
        temp = []
        for key in entry:
            temp.append(key)
        return temp

    #creates a new blank addressbook
    #returns that address book's ID
    def create_address_book(self, address_book_name):
        #create addressbook and get hash
        new_ad = AddressBook(address_book_name)
        original_hash = hash(new_ad)

        #create a temporary dictionary and add values {hash, AddressBook}
        temp_dict = {}
        temp_dict['initialHash'] = original_hash
        temp_dict['object'] = new_ad

        # add temp_dict to list of open addressbooks and increment book_count
        self.open_address_books[self.address_book_count] = temp_dict
        temp_dict['object'].set_meta('address_book_id', self.address_book_count)
        self.address_book_count += 1

        log(self.open_address_books)

        #return id of new_ad
        return self.address_book_count - 1

    #opens an addressbook from an existing
    def open_address_book(self, filename = ''):
        #create addressbook, import from json
        new_ad = AddressBook()
        valid = new_ad.import_json(filename, self.address_book_count)

        #check to see if import was sucessful
        if valid:
            original_hash = hash(new_ad)

            #create a temporary dictionary and add values {hash, AddressBook}
            temp_dict = {}
            temp_dict['initialHash'] = original_hash
            temp_dict['object'] = new_ad
            new_ad.set_meta('address_book_id', self.address_book_count)

            # add temp_dict to list of open addressbooks and increment book_count
            self.open_address_books[self.address_book_count] = temp_dict
            new_ad.set_meta('address_book_id', self.address_book_count)
            self.address_book_count += 1

            #return id of new_ad
            return self.address_book_count - 1
        else:
            return -1

    def close_address_book(self, address_book_id = -1, force = False):
        if self.check_address_book_id(address_book_id) == False:
            #addressBook already closed
            return True
        if force == False:
            initial_hash = self.open_address_books.get(address_book_id).get('initialHash')
            new_hash = hash(self.open_address_books.get(address_book_id).get('object'))
            if initial_hash != new_hash:
                return False
            else:
                del self.open_address_books[address_book_id]
        else:
            del self.open_address_books[address_book_id]

    def save_address_book(self, address_book_id = -1, filename = ''):
        if filename != '':
            self.open_address_books.get(address_book_id).get('object').set_file_name(filename)
        elif self.open_address_books.get(address_book_id).get('object').get_file_name() == '':
            return 1
        if self.open_address_books.get(address_book_id).get('object').save():
            self.open_address_books.get(address_book_id)['initialHash'] = hash(self.open_address_books.get(address_book_id).get('object'))
            return 0
        else:
            return 2

    def create_entry(self, address_book_id = -1, entry_data = None):
        if self.check_address_book_id(address_book_id) and entry_data != None:
            new_entry = Entry(entry_data)
            new_entry.set_value('address_book_id',address_book_id)
            result = self.open_address_books.get(address_book_id).get('object').add_entry(new_entry)
            return result
        else:
            return False

    def delete_entry(self, address_book_id = -1, entry_id = -1):
        if self.check_address_book_id(address_book_id):
            result = self.open_address_books.get(address_book_id).get('object').delete_entry(entry_id)
            return result
        else:
            return False

    def update_entry(self, entry_data = {}):
        address_book_id = entry_data.get('address_book_id')
        if len(entry_data) > 0:
            return self.open_address_books.get(address_book_id).get('object').update_entry(entry_data)
        else:
            return False

    def get_address_book(self, address_book_id = -1):
        if self.check_address_book_id(address_book_id):
            return str(self.open_address_books.get(address_book_id).get('object'))
        else:
            return False

    def import_tsv(self, address_book_id = -1, filename = ''):
        if '.tsv' in filename and self.check_address_book_id(address_book_id):
            result = self.open_address_books.get(address_book_id).get('object').import_tsv(filename,address_book_id)
            return result
        else:
            return -1

    def export_tsv(self, address_book_id = -1, filename = '', entry_ids = []):
        if '.tsv' in filename and self.check_address_book_id(address_book_id):
            result = self.open_address_books.get(address_book_id).get('object').export_tsv(filename,entry_ids)
            return result
        else:
            return -1

    def sort_address_book(self, address_book_id = -1, key = 'last_name', orderBy = 'asc'):
        result = self.open_address_books.get(address_book_id).get('object').sort(key,orderBy)
        return result

    def update_book_name(self,address_book_id = -1, new_book_name = ''):
        if address_book_id == -1 or new_book_name == '':
            return False
        else:
            return self.open_address_books.get(address_book_id).get('object').set_meta('name',new_book_name)

    def get_open_address_books(self):
        return self.open_address_books
