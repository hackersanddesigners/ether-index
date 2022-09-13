# ether-index

## setup

- python > 3.6 (currently 3.9)
- make virtual environment: `python3 -m venv env`
- activate virtual environment: `source env/bin/activate`
- `pip install backsheep uvicorn[standard]`
  - if `zsh` gives an error, do `pip install backsheep uvicorn\[standard\]`
- do `pip freeze > requirements.txt` after installing a new package to update list of packages
- to install all packages do: `pip install -r requirements`
  - if a problem happens:
    - make sure to upgrade pip: `python3 -m pip install --upgrade pip`
    - then try: `python3 -m pip install -r requirements.txt`

## run

to run server, do:

```
uvicorn server:app --port 44777 --reload
```
