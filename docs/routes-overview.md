# API Routes Overview
This document outlines all of the various routes that the backend api accepts as well as expected inputs and provided outputs.
All routes accept only POST requests. Every request will send a JSON object as the body.
Every response includes the following:
+ `code`: integer representing status of the request, 0 => success, !0 => error
+ `message`: error message on error, 'success' on success

## Custom Data Structures
+ \<address_book\>
  + Schema
    ```JSON
    {
        "meta": {
            "name": "<string>",
            "book_id": <integer>,
            "num_entries": <integer>
        },
        "entries": [
            <entry>,
            <entry>,
            ...
            <entry>
        ]
    }
    ```

+ \<entry\>
    ```JSON
    {
        "entry_id": <integer>,
        "address_book_id": <integer>,
        "first_name": "<string>",
        "last_name": "<string>",
        "address_line_one": "<string>",
        "address_line_two": "<string>",
        "city": "<string>",
        "state": "<string>",
        "zip": "<string>",
        "phone": "<string>",
        "email": "<string>",
        "custom_fields": {
            "<key>": {
                "label": "<string>",
                "value": "<string>",
                "global": <boolean>,
                "applied_globally": <boolean>
            }
        }
    }
    ```

---

## `/`
+ input
    ```JSON
    {}
    ```
+ output
    ```JSON
    {
        "code": 0,              // status code
        "message": "success",   // message associated with status code
        "result": [             // list of default fields
            "first_name",
            "last_name",
            ...
        ]
    }
    ```
+ Returns the list of default, static fields to the address book entries.
  + i.e. fields that will always be there (non-custom)

---

## `/new`
+ input
    ```JSON
    {
        "name": "<string>"  // name of new address book
    }
    ```
+ output
    ```JSON
    {
        "code": <integer>,      // status code
        "message": "<string>",  // message associated with status code
        "book_id": <integer>    // id of the new address book
    }
    ```
+ Creates a new address book and returns the book id of the new address book.

---

## `/open`
+ input
    ```JSON
    {
        "filename": "<string>"  // path to file to open
    }
    ```
+ output
    ```JSON
    {
        "code": <integer>,      // status code
        "message": "<string>",  // message associated with status code
        "id": <integer>
    }
    ```
+ Loads an existing address book from file. Returns the id of the opened address book

---

## `/import`
+ input
    ```JSON
    {
        "filename": "<string>",     // path to file to open
        "id": <integer>             // id of address book to append to
    }
    ```
+ output
    ```JSON
    {
        "code": <integer>,          // status code
        "message": "<string>",      // message associated with status code
        "id": <integer>             // id of book appended to
    }
    ```
+ Imports a TSV list of addresses into an open address book. Returns the id of the address book imported into

---

## `/book`
+ input
    ```JSON
    {
        "id": <integer>         // id of address book to get
    }
    ```
+ output
    ```JSON
    {
        "code": <integer>,          // status code
        "message": "<string>",      // message associated with status code
        "result": <address_book>    // address book object
    }
    ```
+ Returns an address book with the given id, if it exists

---

## `/new_entry`
+ input
    ```JSON
    {
        "book_id": <integer>,       // id of book to add to
        "entry_data": <entry>       // entry object
    }
    ```
+ output
    ```JSON
    {
        "code": <integer>,          // status code
        "message": "<string>",      // message associated with status code
        "book_id": <integer>        // id of book added to
    }
    ```
+ Creates a new entry and adds it to the address book specified by `book_id`. Returns the `book_id`.

---

## `/close`
+ input
    ```JSON
    {
        "book_id": <integer>,       // id of book to close
        "force": <boolean>          // indicates whether to force close the book
    }
    ```
+ output
    ```JSON
    {
        "code": <integer>,          // status code
        "message": "<string>"       // message associated with status code
    }
    ```
+ Attempts to close an open address book, forcing if necessary. Returns status code

---

## `/save`
+ input
    ```JSON
    {
        "book_id": <integer>,       // book to save
        "filename": "<string>"      // optional, path to save to
    }
    ```
+ output
    ```JSON
    {
        "code": <integer>,          // status code
        "message": "<string>"       // message associated with status code
    }
    ```
+ Attempts to save an open address book identified by `book_id`. If a file name is specified, the existing filename in `book_id`'s address book is overwritten and the provided filename is used instead

---

## `/delete_entry`
+ input
    ```JSON
    {
        "book_id": <integer>,       // book to delete from
        "entry_id": <integer>       // entry to delete
    }
    ```
+ output
    ```JSON
    {
        "code": <integer>,          // status code
        "message": "<string>"       // message associated with status code
    }
    ```
+ Attempts to delete an entry from an address book.

---

## `/edit_entry`
+ input
    ```JSON
    {
        "entry_data": <entry>       // entry to update
    }
    ```
+ output
    ```JSON
    {
        "code": <integer>,          // status code
        "message": "<string>"       // message associated with status code
    }
    ```
+ Updates an entry in an address book

---

## `/export`
+ input
    ```JSON
    {
        "book_id": <integer>,       // book to export from
        "filename": "<string>",     // file to export to
        "entry_ids": [              // list of entries to export
            <integer>,
            <integer>,
            ...
            <integer>
        ]
    }
    ```
+ output
    ``` JSON
    {
        "code": <integer>,          // status code
        "message": "<string>"       // message associated with status code
    }
    ```
+ Attempts to export a list of entries from an open address book to a file

---

## `/sort`
+ input
    ```JSON
    {
        "book_id": <integer>,           // book to sort
        "sort_key": "<string>",         // last_name / zip
        "order_by": "<string>"          // asc / des
    }
    ```
+ output
    ```JSON
    {
        "code": <integer>,              // status code
        "message": "<string>"           // message associated with status code
    }
    ```
+ Sorts an address book on sort_key, orderd by order_by

---

## /update_book
+ input
    ```JSON
    {
        "book_id": <integer>,           // address book to update
        "new_book_name": "<string>"     // new name of the address book
    }
    ```
+ output
    ```JSON
    {
        "code": <integer>,
        "message": "<string>"
    }
    ```
+ Updates a given book with a new name.