# ether-index

## setup

- python > 3.6 (currently 3.9)
- make virtual environment: `python -m venv venv`
- activate virtual environment: `source venv/bin/activate`
- `pip install backsheep uvicorn[standard]`
  - if `zsh` gives an error, do `pip install backsheep uvicorn\[standard\]`
- do `pip freeze > requirements.txt` after installing a new package to update list of packages

## run

to run server, do:

```
uvicorn server:app --port 44777 --reload
```
