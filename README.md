# DRPG Wiki Filler

A tool written in python 3 to update the wikia automatically.
## Installation

git clone this repo 

```bash
git clone git@github.com:Arctia/DRPGWiki_filler.git
```

fill a user_data.py with the following variables
```python
username = '' # wiki (bot or user) name
password = "" # wiki (bot or user) password
deeplauth = "" # Deepl translator auth api
excell_url = "" # spreadsheet url
```

create an ".env" file and add the following fields
```bash
# if set to true, %AppData%\LocalLow folder is used
DRPG_DEFAULT_PATH=true

# path to drpg master files, used if default path is set to false
DRPGMasters_path=""
```

now you need to install python requirements (inside an venv or as you please)

```bash
pip install -r requirements.txt
```

## Usage/Examples

First of all we need to update the characters data, to do so call and follow the istructions on screen

```bash
bash refresh_xlsx.sh
```

Once the new translations are ready to be pushed call

```bash
bash update_characters.sh
```

At last when the command is over check in the wiki if it is all ok else manually fix the formatting
