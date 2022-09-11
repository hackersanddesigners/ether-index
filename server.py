import os
from dotenv import load_dotenv
load_dotenv()
import requests
from blacksheep import Application, Request, json, redirect
from blacksheep.server.templating import use_templates
from jinja2 import PackageLoader
from jinja2 import Environment, FileSystemLoader
import pymysql.cursors
import get_from_db
from operator import itemgetter


# app init
app = Application(show_error_details=True, debug=True)

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


def chunks(lst, n):
    "Yield successive n-sized chunks from lst."

    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def t(req):
    """
    if GET request return paginated list of pads;
    if POST request use value sent by form to redirect to
    that URL and create a new pad
    """

    
    if req.method == 'GET':

        """
        return list of all pads (padID)
        paginate through the list and fetch x-amount of pads each time
        start with PAGINATION_SIZE
        """

        ep_url = os.getenv('EP_URL')
        ep_api_key = os.getenv('EP_API_KEY')
        
        URL_all_pads = "%s/api/1.2.1/listAllPads?apikey=%s" % (ep_url, ep_api_key)
        
        # use requests sessions to first fetch list of pads
        # then go through the list and check if padText contains `__NOINDEX__`
        
        try:
            s = requests.Session()
            r = s.get(URL_all_pads)
            
            r.raise_for_status()
            
            res = r.json()
            
        except requests.exceptions.HTTPError as e:
            print('cannot fetch resource', r.status_code, '\n', e)
            
            padlist_res = None
            pads_count = 0
            
            
        padlist_res = res['data']['padIDs']
        pads_count = len(padlist_res)

        pagination_size = int(os.getenv('PAGINATION'))
        padlist_data = chunks(padlist_res, pagination_size)

        # we have a list of chunk ranges [0-99], [100-99], ...
        # the URL has a route to set the pagination
        # we read from it and select the correct range size

        padlist = list(padlist_data)

        # get eventual page/<id> from route
        if req.route_values is not None:
            paginate = int(req.route_values["id"])
        else:
            paginate = 0

        # set correct paginate value
        if paginate == 0:
            paginate_UI = paginate +1
        else:
            paginate_UI = paginate


        # build pagination object with all necessary data
        paginate_total = len(padlist)

        pagination = {'display': False,
                      'status': "%s / %s" % (paginate_UI, paginate_total),
                      'page_prev': {'display': False,
                                    'value': None },
                      'page_next': {'display': False,
                                    'value': None }}

        # set correct page-prev/next values
        # page-prev
        if paginate_UI > 1:
            pagination['page_prev'] = {'display': True,
                                       'value': paginate_UI -1}

        # page-next
        if paginate_UI < paginate_total:
            pagination['page_next'] = {'display': True,
                                       'value': paginate_UI +1}
            
        # we add -1 to sync with the list index counter
        padlist_paged = padlist[paginate -1]

        # -- setup db connection
        connection = pymysql.connect(host=os.getenv('DB_HOST'),
                                     user=os.getenv('DB_USER'),
                                     password=os.getenv('DB_PASSWORD'),
                                     db=os.getenv('DB_NAME'),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        # get all pad with appropriate data
        pads_data = get_from_db.get_data(connection, os.getenv('FILTER'), padlist_res)
        pads_data = sorted(pads_data, key=itemgetter(1), reverse=True)

        pads = {"count": pads_count,
                "data": pads_data }

        return view('index', {"pads": pads,
                              "pagination": pagination,
                              "ep_url": ep_url})


    elif req.method == 'POST':
        
        return "will redirect to <url> from form etc."


@app.route("/", methods=["GET", "POST"])
async def page(req: Request):
        
    return await t(req)


@app.route("/page/<id>", methods=["GET", "POST"])
async def subpage(req: Request):

    return await t(req)
