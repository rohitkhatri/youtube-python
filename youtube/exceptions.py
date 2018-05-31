class YouTubeException(Exception):
    def __init__(self, code, message, response):
        self.status_code = code
        self.error_type = message
        self.message = message
        self.response = response
        self.get_error_type()

    def get_error_type(self):
        json_response = self.response.json()

        if 'error' in json_response and 'errors' in json_response['error']:
            self.error_type = json_response['error']['errors'][0]['reason']
