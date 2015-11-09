import bottle
import beaker.middleware
import urllib
import datetime
import time
import json

from bottle import route, redirect, post, run, request, hook
from instagram import client, subscriptions
from os import rename as os_move_file
from instagram.client import InstagramAPI


bottle.debug(True)

session_opts = {
    'session.type': 'file',
    'session.data_dir': './session/',
    'session.auto': True,
}

app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)



CONFIG = {
    'client_id': '12685873d4bc48578693c0a497a98d0f',
    'client_secret': '879c151fd422416aa33d251f70e3924b',
    'redirect_uri': 'http://localhost:8515/oauth_callback'
}



unauthenticated_api = client.InstagramAPI(**CONFIG)
# repsonse = unauthenticated_api.create_subscription(object='geography', lat=35.657872, lng=139.70232, radius=1000, aspect='media', callback_url='http://localhost:8515/realtime_callback')
# print 'response: ', response

@hook('before_request')
def setup_request():
    request.session = request.environ['beaker.session']

def process_tag_update(update):
    print(update)

reactor = subscriptions.SubscriptionsReactor()
reactor.register_callback(subscriptions.SubscriptionType.TAG, process_tag_update)

@route('/')
def home():
    try:
        url = unauthenticated_api.get_authorize_url(scope=["likes","comments"])
        return '<a href="%s">Connect with Instagram</a>' % url
    except Exception as e:
        print(e)

def get_nav():
    nav_menu = ("<h1>Python Instagram</h1>"
                "<ul>"
                    "<li><a href='/media_popular'>Popular Media</a> Calls media_popular - Get a list of the overall most popular media items</li>"
                    "<li><a href='/media_search'>Media Search</a> Calls media_search - Get a list of media close to a given latitude and longitude</li>"
                "</ul>")
    return nav_menu

@route('/oauth_callback')
def on_callback():
    code = request.GET.get("code")
    if not code:
        return 'Missing code'
    try:
        access_token, user_info = unauthenticated_api.exchange_code_for_access_token(code)
        if not access_token:
            return 'Could not get access token'
        api = client.InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'])
        request.session['access_token'] = access_token
    except Exception as e:
        print(e)
    return get_nav()


@route('/media_popular')
def media_popular():
    access_token = request.session['access_token']
    content = "<h2>Popular Media</h2>"
    PIC_NUM = 0
    if not access_token:
        return 'Missing Access Token'
    try:
        api = client.InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'])
        media_search = api.media_popular()
        photos = []
        for media in media_search:
            # print media.tags
            print media.like_count
            photos.append('<img src="%s"/>' % media.get_standard_resolution_url())
            filename = media.id + ".jpg"
            PIC_NUM += 1
            urllib.urlretrieve(media.get_standard_resolution_url(), filename)
            os_move_file(filename, "./popular_pics/"+filename)
        content += ''.join(photos)
    except Exception as e:
        print(e)
    return "%s %s <br/>Remaining API Calls = %s/%s" % (get_nav(),content,api.x_ratelimit_remaining,api.x_ratelimit)


@route('/media_search')
def media_search():
    access_token = request.session['access_token']
    content = "<h2>Media Search</h2>"
    if not access_token:
        return 'Missing Access Token'
    try:
        start = '11/02/2014'
        startDate = datetime.datetime.strptime(start, '%d/%m/%Y')
        count = 0
        result = {}
        endDate = startDate + datetime.timedelta(days=7)
        while count < 15:
            startDate = startDate + datetime.timedelta(days=7)
            endDate = endDate + datetime.timedelta(days=7)
            api = client.InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'])
            media_search = api.media_search(lat="40.7127", lng="74.0059",distance=5000, min_timestamp=startDate, max_timestamp=endDate)
            photos = []
            for media in media_search:
                photos.append('<img src="%s"/>' % media.get_standard_resolution_url())
            content += ''.join(photos)
            count = count + 1
    except Exception as e:
        print(e)
    return "%s %s <br/>Remaining API Calls = %s/%s" % (get_nav(),content,api.x_ratelimit_remaining,api.x_ratelimit)


# location.each do |l|
#     puts
#     html << "<p><b>#{l.name}</b><br/>"
#     media = client.location_recent_media(l.id,:count=>1000)
#     media.each do |m|
#       # html << "<img src='#{m.images.standard_resolution.url}'>"
#       html << "<img src='#{m.images.thumbnail.url}'>"

#     end


@route('/realtime_callback')
@post('/realtime_callback')
def on_realtime_callback():
    mode = request.GET.get("hub.mode")
    challenge = request.GET.get("hub.challenge")
    verify_token = request.GET.get("hub.verify_token")
    if challenge:
        return challenge
    else:
        x_hub_signature = request.header.get('X-Hub-Signature')
        raw_response = request.body.read()
        try:
            reactor.process(CONFIG['client_secret'], raw_response, x_hub_signature)
        except subscriptions.SubscriptionVerifyError:
            print("Signature mismatch")

bottle.run(app=app, host='localhost', port=8515, reloader=True)