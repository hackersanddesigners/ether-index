import os
from dotenv import load_dotenv
load_dotenv()
import requests
from blacksheep import Application, Request, json, redirect
from blacksheep.server.templating import use_templates
from jinja2 import PackageLoader
from jinja2 import Environment, FileSystemLoader

app = Application()

@app.route("/", methods=["GET", "POST"])
async def main(req: Request):
    """
    if GET request return paginated list of pads;
    if POST request use value sent by form to redirect to
    that URL and create a new pad
    """
# create view function to read template from root folder
template_path = os.path.join(os.path.dirname(__file__), './')
view = use_templates(app, loader=FileSystemLoader(template_path))
def datetime_format(timestamp):
    # <https://stackoverflow.com/a/31548402>
    # divide by /1000 to convert from milliseconds to seconds
    ts = timestamp / 1000
    
    # <https://stackoverflow.com/a/37188257>
    ts = datetime.datetime.utcfromtimestamp(ts)
    
    # <https://stackoverflow.com/a/46339491>
    ts = ts.replace(tzinfo=datetime.timezone.utc)
    ts = ts.astimezone().strftime('%Y-%m-%d %H:%M:%S')
    
    return ts
    
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

        return view('index', {"pads": pads,
                              "pagination": pagination,
                              "ep_url": ep_url})
        return "will redirect to <url> from form etc."
