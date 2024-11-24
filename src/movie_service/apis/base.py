import json
import time
import urllib.error as u_error
import urllib.parse as u_parse
import urllib.request as u_request


class Communication:
    def __init__(self, url):
        self.url = url

    def get_response(self, retries: int = 3, timeout: int = 5):
        attempt = 0
        while attempt < retries:
            try:
                with u_request.urlopen(self.url, timeout=timeout) as response:
                    data = response.read()
                    print(data.decode())
                    return json.loads(data.decode())
            except u_error.HTTPError as e:
                if e.code == 524:
                    attempt += 1
                    time.sleep(5)
                    print("Caught 524 error..")
                else:
                    raise

            except u_error.URLError:
                raise

    def get_response_with_params(self, retries: int = 3, **kwargs):
        self.url = f"{self.url}?{u_parse.urlencode(kwargs)}"
        return self.get_response(retries)
