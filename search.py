from instagram import client, subscriptions
import bottle
import beaker.middleware
from bottle import route, redirect, post, run, request, hook
from pprint import pprint
import datetime
import time
import pickle
import os

api = None

bottle.debug(True)

session_opts = {
    'session.type': 'file',
    'session.data_dir': './session/',
    'session.auto': True,
}

CONFIG = {
    'client_id': 'b3725ceeea2c4b1bb5d46d6f436403d9',
    'client_secret': '1684fcc75ec8407ea9f0ca9aa17830d1',
    'redirect_uri': 'http://localhost:8515/oauth_callback'
}

locations = {
            'San Francisco':(37.7808851, -122.3948632),
            'New York City': (40.7127, -74.0059),
            'Los Angeles': (34.0500, -118.2500),
            'Tokyo':(35.6833, 139.6833),
            'London':(51.5027, -0.1275),
            'Paris':(48.8567, 2.3508),
            'Chicago':(41.8369, -87.6847),
            'Moscow':(55.7500, 37.6167),
            'Toronto':(43.7000, -79.4000),
            'Sydney':(-33.8650, 151.2094)
}

all_media = {}

app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)

unauthenticated_api = client.InstagramAPI(**CONFIG)

@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']

def process_tag_update(update):
    print(update)

reactor = subscriptions.SubscriptionsReactor()
reactor.register_callback(subscriptions.SubscriptionType.GEOGRAPHY, process_tag_update)

@route('/')
def home():
    try:
        url = unauthenticated_api.get_authorize_url(scope=["likes","comments"])
        return '<a href="%s">Connect with Instagram</a>' % url
    except Exception as e:
        print(e)


@route('/oauth_callback')
def on_callback():
    code = request.GET.get("code")
    if not code:
        return 'Missing code'
    try:
        access_token, user_info = unauthenticated_api.exchange_code_for_access_token(code)
        if not access_token:
            return 'Could not get access token'
        print("Retrieved an access token...")
        api = client.InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'], client_id=CONFIG['client_id'])
        request.session['access_token'] = access_token
    except Exception as e:
        print(e)
    return get_nav()

def get_nav():
    nav_menu = ("<h1>Connected</h1>"
                "<ul>"
                    "<li><a href='/media_search'>Media Search</a> Begin Collecting</li>"
                "</ul>")
    return nav_menu

@route('/media_search')
def media_search():
    global all_media
    access_token = request.session['access_token']
    content = "<h2>Media Search</h2>"
    if not access_token:
        return 'Missing Access Token'
    try:
        if os.path.exists('all_media.txt'):
            f = open('all_media.txt', 'r')
            all_media = pickle.load(f)
            print("Previous media dictionary size: " + str(len(all_media)))

        currFileName = 'all_media.txt'
        f = open(currFileName, 'w')

        newFile = False
        fileCounter = 0
        while True:

            if newFile is True:
                #sleep for 3 minutes so we don't get duplicates switching files
                print("Sleeping for three minutes...")
                time.sleep(180)
                currFileName = 'all_media_'+str(fileCounter)+'.txt'
                f = open(currFileName, 'w')
                newFile = False


            for key in locations:
                maxTime = int(time.time() - 86400)
                minTime = maxTime - 120
                api = client.InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'])

                #this guarantees we don't overstep the api limits
                while api.x_ratelimit_remaining == 0:
                    print("Sleeping to prevent duplicates...")
                    time.sleep(60)
                    print("Sleep finished.")

                media_search = api.media_search(lat=locations[key][0], lng=locations[key][1], count=200, distance=5000,
                                        min_timestamp=minTime, max_timestamp=maxTime)

                print(key + " photo count: " + str(len(media_search)))

                for media in media_search:
                    #map from mediaid, location -> media properties
                    if (media.id, key) not in all_media:
                        all_media[(media.id, key)] = media
                print("Remaining calls: " + str(api.x_ratelimit_remaining) +" of " + str(api.x_ratelimit))
            print("Media count: " + str(len(all_media)))

            if os.path.exists(currFileName):
                f.close()
                f = open(currFileName, 'w')
                pickle.dump(all_media, f)
                size = os.path.getsize(currFileName)
                print("Current size(mb): " + str(size/1000000))
                if size > 1000000000:
                    f.close()
                    newFile = True
                    fileCounter += 1
                    all_media = {}


    except Exception as e:
        print(e)
    return "%s %s <br/>Remaining API Calls = %s/%s" % (get_nav(),content,api.x_ratelimit_remaining,api.x_ratelimit)

bottle.run(app=app, host='localhost', port=8515, reloader=True)
