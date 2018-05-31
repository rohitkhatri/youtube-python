import requests
from urllib.parse import urlencode


class YouTube:
    _client_id = None
    _client_secret = None
    _api_key = None
    _access_token = None
    _api_base_url = 'https://www.googleapis.com/youtube/v3/'
    _auth_url = 'https://accounts.google.com/o/oauth2/auth'
    _exchange_code_url = 'https://accounts.google.com/o/oauth2/token'
    _scope = [
        'https://www.googleapis.com/auth/youtube',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]
    _part = 'id,snippet'

    def __init__(self, client_id, client_secret, api_key, access_token=None, api_url=None):
        self._client_id = client_id
        self._client_secret = client_secret
        self._api_key = api_key
        self._access_token = access_token

        if api_url:
            self.api_url = api_url

    def get(self, endpoint, **kwargs):
        if self._access_token:
            kwargs['access_token'] = self._access_token
        else:
            kwargs['api_key'] = self._api_key

        if 'part' not in kwargs:
            kwargs['part'] = self._part

        return self.response(self._get(self._api_base_url+endpoint, params=kwargs))

    def post(self, endpoint, **kwargs):
        if self._access_token:
            kwargs['access_token'] = self._access_token
        else:
            kwargs['api_key'] = self._api_key

        return self.response(self._post(self._api_base_url + endpoint, params=kwargs))

    def get_auth_url(self, redirect_uri, **kwargs):
        kwargs = {**{
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'client_id': self._client_id,
            'access_type': 'offline',
            'approval_prompt': 'force'
        }, **kwargs}

        if 'scope' not in kwargs:
            kwargs['scope'] = self._scope

        kwargs['scope'] = ' '.join(kwargs['scope'])

        return self._auth_url+'?'+urlencode(kwargs)

    def exchange_code(self, code, redirect_uri):
        params = {
            'code': code, 'client_id': self._client_id, 'client_secret': self._client_secret,
            'redirect_uri': redirect_uri, 'grant_type': 'authorization_code'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = self.response(self._post(self._exchange_code_url, params=params, headers=headers))

        if response and 'access_token' in response:
            self._access_token = response['access_token']

        return response

    def refresh_token(self, refresh_token):
        params = {
            'client_id': self._client_id, 'client_secret': self._client_secret, 'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return self.response(requests.post(self._exchange_code_url, data=params, headers=headers))

    def get_profile(self):
        return self.response(self._get(
            'https://www.googleapis.com/oauth2/v1/userinfo',
            {'access_token': self._access_token}
        ))

    @staticmethod
    def _get(url, params=None, **kwargs):
        return requests.get(url, params=params, **kwargs)

    @staticmethod
    def _post(url, params=None, **kwargs):
        return requests.post(url, data=params, **kwargs)

    @staticmethod
    def response(response):
        return response.json()
