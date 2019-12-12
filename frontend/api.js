/* This file holds all of our calls to the API */

// /new TODO Ask if they want the name or the ID???
// + Creates a new address book and returns the book id of the new address book.
async function createBook (bookName) {
  const response = await fetch('http://localhost:3600/new', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ name: bookName })
  })
  return await response.json()
}

// /open
// + Loads an existing address book from file.
// Returns the id of the opened address book
async function openBook (filename) {
  const response = await fetch('http://localhost:3600/open', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ filename: filename })
  })
  return await response.json()
}

// /import TODO: Ask if ID is int or string
// + Imports a TSV list of addresses into an open address book.
// Returns the id of the address book imported into
async function importBook (filename, id) {
  const response = await fetch('http://localhost:3600/import', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ filename: filename, id: id })
  })
  return await response.json()
}

// /book
// Request the address book based on id
// Returns an address book with the given id, if it exists
async function getBook (id) {
  const response = await fetch('http://localhost:3600/book', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ id: id })
  })
  return await response.json()
}

// /new_entry TODO: 2 inputs to stringify
// + Creates a new entry and adds it to the address book specified by `book_id`. Returns the `book_id`.
async function newEntry (id, entry) {
  const response = await fetch('http://localhost:3600/new_entry', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ book_id: id, entry_data: entry })
  })
  return await response.json()
}

// /close
// + Attempts to close an open address book, forcing if necessary. Returns status code
async function closeBook (id, force) {
  const response = await fetch('http://localhost:3600/close', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ book_id: id, force: force })
  })
  return await response.json()
}

// /save
// + Attempts to save an open address book identified by `book_id`.
// If a file name is specified, the existing filename in `book_id`'s address book is overwritten
// and the provided filename is used instead
async function saveBook (id, filename) {
  const response = await fetch('http://localhost:3600/save', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ book_id: id, filename: filename })
  })
  return await response.json()
}

// /delete_entry
// + Attempts to delete an entry from an address book.
async function deleteEntry (book_id, entry_id) {
  const response = await fetch('http://localhost:3600/delete_entry', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ book_id: book_id, entry_id: entry_id })
  })
  return await response.json()
}

// /edit_entry
// + Updates an entry in an address book
async function editEntry (entry) {
  const response = await fetch('http://localhost:3600/edit_entry', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ entry_data: entry })
  })
  return await response.json()
}

// /export
// + Attempts to export a list of entries from an open address book to a file
async function exportBook (book_id, filename, entry_ids) {
  const response = await fetch('http://localhost:3600/export', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ book_id: book_id, filename: filename, entry_ids: entry_ids })
  })
  return await response.json()
}

// /sort
// + Sorts an address book on sort_key, orderd by order_by
async function sortBook (book_id, sort_key, order_by) {
  const response = await fetch('http://localhost:3600/sort', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ book_id: book_id, sort_key: sort_key, order_by: order_by })
  })
  return await response.json()
}
