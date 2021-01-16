from library.datetime_helper import is_expired, utcnow
import urllib.request as request
import urllib.parse as parse
import json
from . import HOST, CLIENT_PORT, CLIENT_ID, CLIENT_SECRET, APP_TOKEN

SESSIONS = {

}


def generate_redirect_uri():
    return 'http://{host}:{port}/redirect'.format(host=HOST, port=CLIENT_PORT)


def login(client_id, state):
    redirect_uri = generate_redirect_uri()
    PERMISSIONS = (
        'public_profile',
        'email',
        'user_location',
        'user_gender',
        'user_friends',
        'user_birthday',
        'user_hometown',
        'user_likes',
        'user_photos',
        'user_posts'
    )
    scope = ','.join(PERMISSIONS)
    return '{host}?{query}'.format(host='https://www.facebook.com/v4.0/dialog/oauth', query=parse.urlencode(locals()))


def get_access_token(auth_code=None, refresh_token=None):
    assert auth_code is not None or refresh_token is not None, 'Require either auth or refresh token'
    url = '{host}?{query}'.format(host='https://graph.facebook.com/v4.0/oauth/access_token', query=parse.urlencode({
        'code': auth_code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': generate_redirect_uri()
    }))

    req = request.urlopen(url)
    return json.loads(req.read().decode('ascii'))


def inspect(token):
    url = '{host}?{query}'.format(host='https://graph.facebook.com/debug_token', query=parse.urlencode({
        'input_token': token,
        'access_token': APP_TOKEN
    }))
    req = request.urlopen(url)
    return json.loads(req.read().decode('ascii'))


class Credentials:
    def __init__(self, creds):
        creds.update({
            'start_time': utcnow()
        })
        self.creds = creds
        creds['inspect'] = self._inspect().get('data')

    def __getattr__(self, item):
        if item == 'access_token':
            if self.expired:
                self.refresh()
        return self.creds.get(item, None)

    @property
    def expired(self):
        return is_expired(self.creds['start_time'], self.creds['expires_in'])

    def refresh(self):
        new_token = get_access_token(refresh_token=self.creds['refresh_token'])
        self.creds = new_token

    @staticmethod
    def fromAuthCode(authcode):
        return Credentials(get_access_token(authcode))

    def _inspect(self):
        r = inspect(self.access_token)
        print('Inspect', r)  # Debug
        return r
