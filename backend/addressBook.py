from entry import Entry
from fileIO import *
import json
from utils import *

'''
class AddressBook

Represents an Address Book
'''
class AddressBook:
    def __init__(self, name = ''):
        self.meta = {
            'address_book_id': 0,
            'name': name,
            'num_entries': 0,
            'sort_key': 'last_name',
            'sort_order': 'asc'
        }
        self.entries = {}
        self.default_custom_fields = {}
        self.entryCount = 0
        self.filename = ''

    def __str__(self):
        rep = {}
        rep['meta'] = self.meta
        rep['entries'] = {}
        for id, entry in self.entries.items():
            rep['entries'][str(id)] = entry.get_values()
        return json.dumps(rep)

    def check_entry_id(self, entry_id):
        return entry_id in self.entries.keys()

    def __hash__(self):
        items = []
        for key, value in self.entries.items():
            items.append(key)
            items.append(value)
        items.append(value for key, value in self.meta.values())
        items.append(self.filename)
        log(items)
        return hash(tuple(items))

    def get_file_name(self):
        return self.filename

    def set_file_name(self, filename = ''):
        if filename == '':
            return False
        else:
            self.filename = filename
            return True

    def add_entry(self, entry_object = None):
        if entry_object != None:
            entry_object.set_value('entry_id',self.entryCount)
            entry_object.set_value('address_book_id', self.meta.get('address_book_id'))
            self.entries[self.entryCount] = entry_object
            self.entryCount += 1
            self.update_num_entries()
            self.sort(self.meta.get('sort_key'),self.meta.get('sort_order'))
            return True
        else:
            return False

    def delete_entry(self, entry_id = -1):
        if entry_id in self.entries.keys():
            del self.entries[entry_id]
            self.update_num_entries()
            return True
        else:
            return False

    def update_entry(self, entry_data = {}):
        if entry_data != {}:
            entry_id = entry_data.get('entry_id')
            result = self.entries.get(entry_id).set_values(entry_data)
            for key,value in entry_data.get('custom_fields').items():
                if value.get('global') == True and value.get('applied_globally') == False:
                    for entry in self.entries.values():
                        if entry.get_value('custom_fields').get(key) == None:
                            entry_customFields = entry.get_value('custom_fields')
                            entry_customFields[key] = {'label' : value.get('label') , 'value': '', 'global': True, 'applied_globally' : True}
                            entry.set_value('custom_fields',entry_customFields)
                        else:
                            entry_customFields = entry.get_value('custom_fields')
                            entry_customFields[key].update({'label':value.get('label'),'global':True,'applied_globally':True})
                            entry.set_value('custom_fields',entry_customFields)
            self.sort(self.meta.get('sort_key'),self.meta.get('sort_order'))
            return result
        return False

    def import_tsv(self, filename = '', address_book_id = -1):
        if filename != '' and address_book_id != -1:
            #TODO Gold plating, set metadata from tsv file
            #self.meta = getMetaTSV(filename)
            entries = getEntriesTSV(filename)
            for entry in entries:
                new_entry = Entry(entry)
                new_entry.set_value('address_book_id', address_book_id)
                new_entry.set_value('custom_fields', {})
                new_entry.set_value('entry_id',self.entryCount)
                self.entries[self.entryCount] = new_entry
                self.entryCount += 1
            self.update_num_entries()
            self.sort(self.meta.get('sort_key'),self.meta.get('sort_order'))
            return True
        return False

    def update_num_entries(self):
        self.meta['num_entries'] = len(self.entries)


    #TODO IOError Checking
    def export_tsv(self, filename = '', entry_ids = []):
        if filename is '':
            return False
        elif len(entry_ids) is 0:
            entries_list = []
            for value in self.entries.values():
                    export_entry = value.get_values()
                    export_entry = self.sanatize_for_export(export_entry)
                    entries_list.append(export_entry)
            saveTSV(filename,entries_list)
            return True

        else:
            entries_list = []
            for key,value in self.entries.items():
                if key in entry_ids:
                    export_entry = value.get_values()
                    export_entry = self.sanatize_for_export(export_entry)
                    entries_list.append(export_entry)
            saveTSV(filename,entries_list)
            return True

        #TODO IOError
    def import_json(self, filename = '',address_book_count = -1):
        if filename is '' or address_book_count == -1:
            return False
        else:
            meta_from_file = getMetaJSON(filename)
            for key, value in meta_from_file.items():
                self.set_meta(key,value)
            entries = getEntriesJSON(filename)
            for entry in entries:
                new_entry = Entry(entry)
                new_entry.set_value('entry_id',self.entryCount)
                new_entry.set_value('address_book_id',address_book_count)
                self.entries[self.entryCount] = new_entry
                self.entryCount += 1
            self.update_num_entries()
            self.filename = filename
            self.sort(self.meta.get('sort_key'),self.meta.get('sort_order'))
            return True

    #TODO IOError
    def save(self, filename = ''):
        if filename != '':
            self.filename = filename
        if self.filename is '':
            return False
        else:
            entry = []
            self.meta.pop('address_book_id')
            for value in self.entries.values():
                entry.append(self.sanatize_for_save(value.get_values()))
            saveJSON(self.filename,self.meta,entry)
            return True

    def sanatize_for_export(self,data_dict):
        if data_dict.get('entry_id') != None:
            data_dict.pop('entry_id')
        if data_dict.get('address_book_id') != None:
            data_dict.pop('address_book_id')
        if data_dict.get('custom_fields') != None:
            data_dict.pop('custom_fields')
        return data_dict

    def sanatize_for_save(self,data_dict):
        if data_dict.get('entry_id') != None:
            data_dict.pop('entry_id')
        if data_dict.get('address_book_id') != None:
            data_dict.pop('address_book_id')
        return data_dict

    def sort(self, key = 'last_name', orderBy = 'asc'):
        self.meta['sort_key'] = key
        self.meta['sort_order'] = orderBy
        log(key)
        log(orderBy)

        reverse_order = False
        if self.meta.get('sort_order') == 'des':
            reverse_order = True

        sorted_list = sorted(self.entries.values(), key=lambda x: self.sort_helper(x,self.meta.get('sort_key')),reverse=reverse_order)

        position = 0

        for key in self.entries.keys():
            sorted_list[position].set_value('entry_id',key)
            self.entries[key] = sorted_list[position]
            position += 1

        return True

    def sort_helper(self, entry,key):
        if key == 'last_name':
            return str(entry.get_value('last_name')).lower() + str(entry.get_value("first_name")).lower()
        else:
            return entry.get_value('zip')

    def get_entry(self,entry_id):
        return self.entries.get(entry_id)

    def get_meta(self, key):
        return self.meta.get(key)

    def set_meta(self, key, value):
        self.meta[key] = value
        return True

    def get_entries(self):
        return self.entries
