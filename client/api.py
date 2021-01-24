from .credentials import Credentials
import urllib.request as request
from urllib.parse import urlencode
import json
from . import FEED_LIMIT


def get_friends(credential: Credentials):
    url = '{host}{user}?{query}'.format(host='https://graph.facebook.com/v9.0/me/friends/', query=urlencode({
        'access_token': credential.access_token,
    }), user=credential.inspect.get('user_id'))

    req = request.urlopen(url)
    return json.loads(req.read().decode('utf-8'))


def get_user(credential: Credentials):
    url = '{host}{user}?{query}'.format(host='https://graph.facebook.com/v4.0/', query=urlencode({
        'access_token': credential.access_token,
        'fields': 'email,id,gender,name,name_format,first_name,middle_name,last_name,languages,friends,'
                  'permissions,picture,quotes,likes,birthday,age_range,hometown,meeting_for,link,games,'
                  'feed,photos,albums,videos'
    }), user=credential.inspect.get('user_id'))

    req = request.urlopen(url)
    results = json.loads(req.read().decode('utf-8'))

    feed = results.get('feed', {})
    while True:
        url = feed.get('paging', {}).get('next')
        if url is None:
            break

        req = request.urlopen(url)
        feed = json.loads(req.read().decode('utf-8'))

        results['feed']['data'].extend(feed.get('data'))

        if len(results['feed']['data']) >= FEED_LIMIT:
            break

    return results
