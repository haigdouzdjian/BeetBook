const { app, BrowserWindow, Menu, dialog, ipcMain } = require('electron')
const { spawn, execFile } = require('child_process')
const path = require('path')
const isDev = !app.isPackaged
const logger = console
const isMac = process.platform === 'darwin'
const fetch = require('node-fetch')
if (require('electron-squirrel-startup')) {
  app.quit()
}
/**********************************************/
/*                  Utils                     */
/**********************************************/

// Get file path for file in _this_ directory
const getFilePath = (filename) => {
  const url = require('url').format({
    protocol: 'file',
    slashes: true,
    pathname: path.join(__dirname, filename)
  })
  return url
}

/**********************************************/
/*              Backend Process               */
/**********************************************/
const BACK_FOLDER = 'backend'
const BACK_ENTRY = 'api'
const BACK_DIST = 'pythondist'
let backProc = null

// Find the python file
const getScriptPath = () => {
  // In development, no executable
  if (isDev) {
    return path.join(__dirname, '..', BACK_FOLDER, BACK_ENTRY + '.py')
  }
  // On window executable ends in .exe
  if (process.platform === 'win32') {
    return path.join(__dirname, '..', BACK_DIST, BACK_ENTRY + '.exe')
  }
  return path.join(__dirname, '..', BACK_DIST, BACK_ENTRY)
}

// Start the backend server
const createBackendProc = () => {
  const script = getScriptPath()

  // Call the python process
  try {
    if (isDev) {
      backProc = spawn('python', [script]) // In dev, so use python
    } else {
      backProc = execFile(script) // In prod, so run executable
    }
    backProc.on('error', (err) => {
      logger.error('Failed to start server. ' + err)
      app.quit()
    })
  } catch (err) {
    logger.error('Spawn exception: ' + err)
    app.quit()
  }

  // Python process logs
  if (isDev) {
    backProc.on('exit', (code, signal) => {
      if (code) {
        logger.error(`backProc exited with ${code}`)
      } else if (signal) {
        logger.error(`backProc was killed with ${signal}`)
      } else {
        logger.log('Child exited okay')
      }
    })

    backProc.stdout.on('data', (data) => {
      logger.log(`child stdout:\n${data}`)
    })

    backProc.stderr.on('data', (data) => {
      logger.error(`child stderr:\n${data}`)
    })

    if (backProc != null) {
      logger.log('Backend server successfully started on port 3600')
    }
  }
}

// Kill the backend server
const exitBackendProc = () => {
  backProc.kill()
  backProc = null
}

/**********************************************/
/*              Window Processes              */
/**********************************************/
let mainWindow = null
let bookWindowCounter = 0 // Keep track of how many book windows we have open
let nameModal = null
let customFieldModal = null

/* Main Window */
var createMainWindow = function () {
  mainWindow = new BrowserWindow({
    width: 1024,
    minWidth: 1024,
    height: 768,
    minHeight: 768,
    center: true,
    title: app.getName(),
    webPreferences: {
      nodeIntegration: true
    },
    titleBarStyle: 'hidden',
    show: false
  })
  // and load the index.html of the app.
  mainWindow.loadURL(getFilePath('loading_screen.html')) // load the web page

  mainWindow.once('ready-to-show', () => {
    mainWindow.maximize()
    mainWindow.show()
  })

  // Emitted when the window is closed.
  mainWindow.on('closed', function () {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null
  })
}

/* Address Book Window */
const createBookWindow = (bookName, parentWindow) => {
  const bookWindow = new BrowserWindow({
    width: 1024,
    minWidth: 1024,
    height: 768,
    minHeight: 768,
    title: `BeetBook - ${bookName}`,
    center: true,
    webPreferences: {
      nodeIntegration: true
    },
    titleBarStyle: 'hidden',
    show: false
  })
  bookWindowCounter = ++bookWindowCounter
  // Once we create an address book
  // enable the menu options
  if (bookWindowCounter >= 1) {
    const menu = Menu.getApplicationMenu()
    let menuItem = menu.getMenuItemById('open')
    menuItem.enabled = true
    menuItem = menu.getMenuItemById('save')
    menuItem.enabled = true
    menuItem = menu.getMenuItemById('save_as')
    menuItem.enabled = true
    menuItem = menu.getMenuItemById('close')
    menuItem.enabled = true
    menuItem = menu.getMenuItemById('import')
    menuItem.enabled = true
    menuItem = menu.getMenuItemById('export')
    menuItem.enabled = true
  }
  return bookWindow
}

const setBookWindowOptions = (parentWindow, bookWindow, bookContents) => {
  bookWindow.loadURL(getFilePath('book.html'))

  bookWindow.once('ready-to-show', () => {
    // Fill in page contents
    bookWindow.webContents.send('address_book:init', bookContents)
    parentWindow.blur()
    bookWindow.maximize()
    bookWindow.show()
  })

  bookWindow.on('closed', function () {
    bookWindowCounter = --bookWindowCounter
    // When all the address books are closed
    // disable their menu options
    if (bookWindowCounter === 0) {
      const menu = Menu.getApplicationMenu()
      let menuItem = menu.getMenuItemById('open')
      menuItem.enabled = true
      menuItem = menu.getMenuItemById('save')
      menuItem.enabled = false
      menuItem = menu.getMenuItemById('save_as')
      menuItem.enabled = false
      menuItem = menu.getMenuItemById('close')
      menuItem.enabled = false
      menuItem = menu.getMenuItemById('import')
      menuItem.enabled = false
      menuItem = menu.getMenuItemById('export')
      menuItem.enabled = false
    }
    bookWindow = null
  })
}

/* New Book Name Modal */
const createNameModal = () => {
  if (nameModal) {
    nameModal.focus() // only one modal at a time
    return
  }
  nameModal = new BrowserWindow({
    width: 300,
    height: 200,
    title: 'Name your new address book',
    webPreferences: {
      nodeIntegration: true
    },
    resizable: false,
    frame: false,
    parent: mainWindow,
    alwaysOnTop: true,
    center: true
  })
  nameModal.loadURL(getFilePath('new_name.html'))

  nameModal.on('closed', function () {
    nameModal = null
  })
}

/* Custom Field Modal */
const createCustomFieldModal = () => {
  if (customFieldModal) {
    customFieldModal.focus() // only one modal at a time
    return
  }
  // This modal should appear on top of the
  // book window that you are editing
  let parent = BrowserWindow.getFocusedWindow()
  if (parent === null) { parent = mainWindow }
  customFieldModal = new BrowserWindow({
    width: 300,
    height: 200,
    title: 'Create custom field',
    webPreferences: {
      nodeIntegration: true
    },
    resizable: false,
    frame: false,
    parent: parent,
    alwaysOnTop: true,
    center: true
  })
  customFieldModal.loadURL(getFilePath('add_custom_field.html'))

  customFieldModal.on('closed', function () {
    customFieldModal = null
  })
}

/**********************************************/
/*                  Startup                   */
/**********************************************/
// This method will be called when Electron has finished
// initialization and is ready to create browser windows.

app.on('ready', function () {
  createBackendProc() // Start backend process
  createMenu()
  createMainWindow()
})

app.on('activate', function () {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) createMainWindow()
})

/**********************************************/
/*                   Exit                     */
/**********************************************/
// Quit when all windows are closed.
app.on('window-all-closed', function () {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (isMac) app.quit()
})

// Kill the server when the app quits
app.on('will-quit', exitBackendProc)

/**********************************************/
/*                IPC Comms                   */
/**********************************************/

/* Messages from nameModal */
ipcMain.on('address_book:create', (e, bookContents) => {
  nameModal.close()
  bookContents = JSON.parse(bookContents) // This is Very IMPORTANT
  logger.log(`New book is: ${bookContents.meta.name}`)
  logger.log(`New book id is: ${bookContents.meta.address_book_id}`)
  logger.log(`New book has ${bookContents.meta.numEntries} entries`)
  logger.log(`New book entries: ${bookContents.entries}`)

  // Create the new bookWindow
  const parent = mainWindow
  const child = createBookWindow(bookContents.meta.name, parent)
  setBookWindowOptions(parent, child, bookContents)
})

/* Catching input from customFieldModal */
ipcMain.on('field:create', (e, modalID) => {
  customFieldModal.send('field:modal', modalID)
})

ipcMain.on('field:add', (e, value, name, parent, global) => {
  const key = 'new_attribute' // TODO: change key to be lower case with underscores
  let customField = `{
    ${key}: {
      label: '${name}',
      value: '${value}',
      global: '${global}',
      applied_globally: false
    }
  }`

  customField = JSON.stringify(customField)
  console.log(customField)

  const callingWindow = BrowserWindow.getFocusedWindow()
  // parent to find calling modal
  callingWindow.webContents.send('custom_field:add', parent, customField)
  customFieldModal.close()
})

// called by menu to export to .tsv
const exportFile = () => {
  dialog.showSaveDialog({
    filters: [
      { name: 'BeetBook (tsv)', extensions: 'tsv' }
    ]
  }).then((res) => {
    if (res) {
      console.log(res.filePath)
      const filePath = res.filePath.replace(/(\r\n|\n|\r)/gm, '')
      const newFilePath = `${filePath}.tsv`
      console.log(newFilePath)

      BrowserWindow.getFocusedWindow().webContents.send('exportBook', newFilePath)
    } else {
      console.log('CANCELED')
    }
  })
}

// called by menu to import from .json
const importFile = () => {
  dialog.showOpenDialog(
    {
      properties: ['openFile'],
      filters: [
        { name: 'BeetBook (tsv)', extensions: 'tsv' }
      ]
    }).then((res) => {
    if (res) {
      console.log(res.filePaths)
      BrowserWindow.getFocusedWindow().webContents.send('importBook', res.filePaths[0])
    } else {
      console.log('CANCELED')
    }
  })
}

// called by menu and buttons to open a .json
const openFile = () => {
  dialog.showOpenDialog(
    {
      properties: ['openFile'],
      filters: [
        { name: 'BeetBook (json)', extensions: 'json' }
      ]
    }).then((res) => {
    if (res) {
      console.log(res.filePaths)

      openBook(res.filePaths[0]).then((res) => {
        // Get the new book from the API
        console.log('Back from open book openBook')
        console.log(res)
        getBook(JSON.parse(res).id).then((res) => {
          console.log('Got into getBook function')
          console.log(res)

          const bookContents = JSON.parse(res.result)
          console.log(bookContents)
          const parent = mainWindow
          const child = createBookWindow(bookContents.meta.name, parent)
          setBookWindowOptions(parent, child, bookContents)
        })
      })
    } else {
      console.log('CANCELED')
    }
  })
}

// Refocus the mainWindow, when book icon clicked
ipcMain.on('reFocus', () => {
  mainWindow.focus()
})
// Called by menu and buttons to open file dialog
ipcMain.on('openFile', (event, path) => {
  event.preventDefault()
  dialog.showOpenDialog(
    {
      properties: ['openFile'],
      filters: [
        { name: 'BeetBook (json)', extensions: 'json' }
      ]
    }).then((res) => {
    if (res) {
      console.log(res.filePaths)

      openBook(res.filePaths[0]).then((res) => {
        // Get the new book from the API
        console.log('Back from open book openBook')
        console.log(res)
        getBook(JSON.parse(res).id).then((res) => {
          console.log('Got into getBook function')
          console.log(res)

          const bookContents = JSON.parse(res.result)
          console.log(bookContents)
          const parent = mainWindow
          const child = createBookWindow(bookContents.meta.name, parent)
          setBookWindowOptions(parent, child, bookContents)
        })
      })
    } else {
      console.log('CANCELED')
    }
  })
})

// /open route to backend
// + Loads an existing address book from file.
// Returns the id of the opened address book
async function openBook (filename) {
  console.log('in openBook filename[0] is:')
  console.log(filename)
  // try{
  const response = await fetch('http://localhost:3600/open', {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ filename: filename })
  })
  return response.json()
}

async function getBook (id) {
  console.log('Into the getBook function')
  try {
    const response = await fetch('http://localhost:3600/book', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ id: id })
    })
    return await response.json()
  } catch (err) {
    console.log(err)
  }
}

ipcMain.on('newBook', () => {
  createNameModal()
})

/**********************************************/
/*                   Menus                    */
/**********************************************/
const mainMenuTemplate = [
  // Show app name for mac menu bar
  ...(isMac ? [{
    label: app.getName()
  }] : []),
  {
    label: 'File',
    submenu: [
      {
        label: 'New',
        accelerator: isMac ? 'Command+N' : 'Ctrl + N',
        click () {
          createNameModal()
        }
      },
      {
        label: 'Open',
        id: 'open',
        enabled: true,
        accelerator: isMac ? 'Command+O' : 'Ctrl + O',
        click () {
          openFile()
        }
      },
      {
        label: 'Save',
        id: 'save',
        enabled: false,
        accelerator: isMac ? 'Command+S' : 'Ctrl + S',
        click: () => {
          // Call Save As function
          BrowserWindow.getFocusedWindow().webContents.send('address_book:save')
        }
      },
      {
        label: 'Save As',
        id: 'save_as',
        enabled: false,
        accelerator: isMac ? 'Command+A' : 'Ctrl + A',
        click: () => {
          // Call Save As function
          BrowserWindow.getFocusedWindow().webContents.send('address_book:save_as')
        }
      },
      {
        label: 'Close',
        id: 'close',
        enabled: false,
        accelerator: isMac ? 'Command+W' : 'Ctrl + W',
        click: () => {
          BrowserWindow.getFocusedWindow().webContents.send('address_book:close')
        }
      },
      {
        label: 'Import',
        id: 'import',
        enabled: false,
        accelerator: isMac ? 'Command+I' : 'Ctrl + I',
        click () {
          importFile()
        }
      },
      {
        label: 'Export',
        id: 'export',
        enabled: false,
        accelerator: isMac ? 'Command+E' : 'Ctrl + E',
        click () {
          exportFile()
        }
      },
      {
        type: 'separator'
      },
      {
        label: 'Quit',
        accelerator: isMac ? 'Command+Q' : 'Ctrl + Q',
        click () {
          app.quit()
        }
      }
    ]
  },
  {
    label: 'View',
    submenu: [
      {
        role: 'resetzoom'
      },
      {
        role: 'zoomin'
      },
      {
        role: 'zoomout'
      },
      {
        type: 'separator'
      },
      {
        role: 'togglefullscreen'
      }
    ]
  }
]

// Add developer menu when in development
if (isDev) {
  mainMenuTemplate.push({
    label: 'Dev Tools',
    submenu: [
      {
        label: 'Test Window',
        click () {
          createCustomFieldModal()
        }
      },
      {
        role: 'reload'
      },
      {
        role: 'forcereload'
      },
      {
        role: 'toggledevtools'
      }
    ]
  })
}
// Create menu based on template
const createMenu = () => {
  const menu = Menu.buildFromTemplate(mainMenuTemplate)
  Menu.setApplicationMenu(menu)
}
