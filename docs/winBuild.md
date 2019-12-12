# From PowerShell
## Prereqs
* choco install python --version=3.7.0
* choco install yarn

## Build
* yarn install
* python -m venv env
* .\env\Scripts\activate
* pip install -r .\backend\requirements.txt
* pyinstaller -F .\backend\api.py --distpath .\pythondist
* yarn electron-forge make
