import os
from dotenv import load_dotenv
load_dotenv()
import requests
from blacksheep import Application, Request, json, redirect

app = Application()

@app.route("/", methods=["GET", "POST"])
async def main(req: Request):
    """
    if GET request return paginated list of pads;
    if POST request use value sent by form to redirect to
    that URL and create a new pad
    """
    
    if req.method == 'GET':

        """
        return list of all pads (padID)
        paginate through the list and fetch x-amount of pads each time
        start with 100 (?)
        """

        URL_all_pads = "%s/api/1.2.1/listAllPads?apikey=%s" % (os.getenv('EP_URL'), os.getenv('EP_API_KEY'))
        r = requests.get(URL_all_pads)

        return json(r.json())

    elif req.method == 'POST':

        return "will redirect to <url> from form etc."
