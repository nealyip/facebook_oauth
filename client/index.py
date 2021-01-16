import hashlib
import random
import re
import urllib.parse as parse
from urllib.error import HTTPError
import json

import library.local_server as local_server
from . import CLIENT_PORT, HOST, CLIENT_ID
from .credentials import Credentials, SESSIONS, login
from .api import get_user


def generateCode():
    m = hashlib.sha256()
    m.update(bytes(str(random.random()), encoding='ascii'))
    return m.hexdigest()


class ClientHandler(local_server.Handler):

    def do_GET(self):
        try:
            parsed = parse.urlparse(self.path)
            query = dict(parse.parse_qsl(parsed.query))
            cookies = self.headers.get('Cookie') or ''
            search_session = re.search(r'SESSIONID=\b(\w+)\b', cookies)
            if parsed.path == '/':
                if search_session is not None and SESSIONS.get(search_session.group(1)) is not None:
                    self.redirect('http://%s:%d/user' % (HOST, CLIENT_PORT))
                else:
                    authorization_code = '<a href="{}">Login</a>'.format(login(CLIENT_ID, '1'))
                    body = '<!DOCTYPE html><html><body><h1>Welcome to client</h1><p>{}</p></body></html>'.format(
                        authorization_code)
                    self.ok(body)
            elif parsed.path == '/redirect':
                code = query.get('code')
                assert code is not None, 'Auth code not found'
                session_id = generateCode()
                SESSIONS.setdefault(session_id, {'oauth2': Credentials.fromAuthCode(code)})
                self.redirect('http://%s:%d/user' % (HOST, CLIENT_PORT), headers={
                    "Set-Cookie": 'SESSIONID=%s; httponly' % session_id
                }.items())
            elif parsed.path == '/user':
                assert search_session and SESSIONS.get(search_session.group(1)), 'Session not found'
                credential = SESSIONS.get(search_session.group(1)).get('oauth2')
                user = get_user(credential)
                body = '<!DOCTYPE html><html><body><h1>Hello {}</h1><div><pre>{}</pre></div></body></html>'.format(user.get('name'), json.dumps(user, ensure_ascii=False, indent=2))
                self.ok(body)
        except HTTPError as e:
            print(e.fp.read())
            self.error(e)
        except BaseException as e:
            self.error(e)


def run():
    local_server.serve(CLIENT_PORT, ClientHandler)
