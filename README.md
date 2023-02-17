# ether-index

## setup

- python > 3.6 (currently 3.9)
- make virtual environment: `python3 -m venv env`
- activate virtual environment: `source env/bin/activate`
- do `pip freeze > requirements.txt` after installing a new package to update list of packages
- to install all packages do: 
  - make sure to upgrade pip: `python3 -m pip install --upgrade pip`
  - then try: `python3 -m pip install -r requirements.txt`
- copy `env.sample` and rename it to `.env`: `cp env.sample .env`
  - `ENV`: choose between `development` or `production`, `development` sets more debug options for the app
  - `DB_HOST`: SQL db host
  - `DB_USER`: SQL db user
  - `DB_PASSWORD`: SQL db pw
  - `DB_NAME`: SQL db name
  - `EP_URL`: check etherpad-lite's `settings.json`, under the `port` key
  - `EP_API_KEY`: check etherpad-lite's `APIKEY` file, this file is generated after running etherpad-lite for the first time
  - `FILTER`: set a special keyword to use at the beginning of a pad to mark it as non-indexable, eg it will not show up in the ether-index list
  - `PAGINATION`: *currently not in used*: set how many pads should be shown at once, it would enable pagination
  
`PAGINATION`: there is a problem to make this work and sort pads by latest modified at the same time. for now loading all pads at once (~1200) takes 2 seconds (eg to load the front page), so it's OK.

## run

to run server, do:

```
./server.sh
```
