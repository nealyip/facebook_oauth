from .credentials import Credentials
import urllib.request as request
from urllib.parse import urlencode
import json
from . import FEED_LIMIT


def get_user(credential: Credentials):
    url = '{host}{user}?{query}'.format(host='https://graph.facebook.com/v3.1/', query=urlencode({
        'access_token': credential.access_token,
        'fields': 'email,id,gender,name,friends,birthday,hometown,games,feed,photos,albums'
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
