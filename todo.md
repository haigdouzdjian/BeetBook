# Critical
+ Open Book makes api calls
  + Flow
    + Open Dialog
    + /open request to api with filename
    + receive id from api
    + /book request to api with id provided by previous response
+ File -> Open
  + See above open file flow
+ File -> Save
  + Flow
    + make /save request to api with current ID
    + API will indicate if a filename needs to be provided
    + If filename needed
      + Save As dialog
      + Send /save request again with filename
    + else
      + handle other errors
+ File -> Save As
  + Save As Dialog
  + send /save request to api with current ID and new filename

+ File -> Close
  + Send close request to API
  + if changes made, api will indicate
    + If yes
      + Prompt user to save
      + If use wants to save
        + send /save request, see above flow
      + else
        + send /close with force flag set (see routes-overview.md)
    + else
      + wait for response from api indicating successful closure, close window

+ Close All / Cmd-Q, etc.
  + see above flow for close
  + do for each window


+ On edit of Entry
  + when User clicks submit, send data to api with /edit_entry request
  + reload book
  + /edit_entry -> /book

+ Reset Modals after each edit/new entry
  + Right now, if I edit an entry and click save, the modal will be static with the data unable to create a new entry with fresh data

---

# Major
+ Remove DevTools Menu for packaging
+ When user clicks Ascending/Descending/Zip-Code drop down, send /sort request to user, reload book with sort changes
+ User-Defined Fields support in new entry AND edit entry

---

# Minor
+ Import/Export of Entries