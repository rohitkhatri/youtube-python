import requests


class YouTube:
    api_key = None
    access_token = None
    api_base_url = 'https://www.googleapis.com/youtube/v3/'
    part = 'id,snippet'

    def __init__(self, api_key, access_token=None, api_url=None):
        self.api_key = api_key
        self.access_token = access_token

        if api_url:
            self.api_url = api_url

    def get(self, endpoint, **kwargs):
        if self.access_token:
            kwargs['access_token'] = self.access_token
        else:
            kwargs['api_key'] = self.api_key

        if 'part' not in kwargs:
            kwargs['part'] = self.part

        return self.response(requests.get(self.api_base_url+endpoint, params=kwargs))

    @staticmethod
    def response(response):
        return response.json()
