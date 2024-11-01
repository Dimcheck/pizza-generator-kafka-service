import json
import urllib.error as u_error
import urllib.parse as u_parse
import urllib.request as u_request

from fastapi.exceptions import HTTPException


class Communication:
    def __init__(self, url):
        self.url = url

    def get_response(self):
        try:
            with u_request.urlopen(self.url) as response:
                data = response.read()
                return json.loads(data.decode())
        except u_error.HTTPError as e:
            raise HTTPException(e.code, e.reason)
        except u_error.URLError as e:
            raise HTTPException(e.code, e.reason)

    def get_response_with_params(self, **kwargs):
        self.url = f"{self.url}?{u_parse.urlencode(kwargs)}"
        return self.get_response()
