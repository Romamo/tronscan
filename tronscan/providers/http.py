import os
import random
import sys
import time
from typing import Any, List, Union
from urllib.parse import urljoin

import requests
from requests_ratelimiter import LimiterSession

DEFAULT_TIMEOUT = 10.0


class HTTPProvider:
    """An HTTP Provider for API request.

    :param endpoint_uri: HTTP API URL base. Default value is ``"https://apilist.tronscanapi.com/"``. Can also be configured via
        the ``TRONPY_HTTP_PROVIDER_URI`` environment variable.
    :param timeout: HTTP timeout in seconds.
    :param api_key: Tronscan API Key in str, or list of str.
    """

    def __init__(
        self,
        endpoint_uri: str = None,
        api_key: Union[str, List[str]] = None,
        timeout: float = DEFAULT_TIMEOUT,
        rate_limit: int = 4
    ):
        super().__init__()

        if endpoint_uri is None:
            self.endpoint_uri = os.environ.get("TRONSCAN_HTTP_PROVIDER_URI", "https://apilist.tronscanapi.com/")
        elif isinstance(endpoint_uri, (str,)):
            self.endpoint_uri = endpoint_uri
        else:
            raise TypeError(f"unknown endpoint uri {endpoint_uri}")

        if "tronscanapi" in self.endpoint_uri:
            self.use_api_key = True
            if api_key is None:
                self._api_keys = [os.environ.get("TRONSCAN_API_KEY", "")]
            elif isinstance(api_key, (str,)):
                self._api_keys = [api_key]
            elif isinstance(api_key, (list,)) and api_key:
                self._api_keys = api_key

            self._default_api_keys = self._api_keys.copy()
        else:
            self.use_api_key = False

        self.timeout = timeout

        self.rate_limit = rate_limit
        self.sess = self._get_session()
        self.sess.headers["User-Agent"] = f"Tronscanpy/1.0"

    def _headers(self):
        headers = {
        }
        if self.use_api_key:
            headers["TRON-PRO-API-KEY"] = self.random_api_key
        return headers

    def _get_session(self) -> requests.Session:
        if self.rate_limit:
            return LimiterSession(per_second=self.rate_limit)
        else:
            return requests.Session()

    def make_request(self, endpoint: str, get=None, post=None, json=None) -> dict:
        if post or json:
            method = 'POST'
        else:
            method = 'GET'
            if not get:
                get = {}

        headers = self._headers()

        if json:
            headers['Content-Type'] = 'application/json'

        if self.use_api_key:
            headers["TRON-PRO-API-KEY"] = self.random_api_key

        url = urljoin(self.endpoint_uri, endpoint)

        resp = self.sess.request(method, url, params=get, data=post, json=json, headers=headers, timeout=self.timeout)

        if self.use_api_key:
            if resp.status_code == 403 and b"Exceed the user daily usage" in resp.content:
                print("W:", resp.json().get("Error", "rate limit!"), file=sys.stderr)
                self._handle_rate_limit()
                return self.make_request(endpoint, get, post, json)

        resp.raise_for_status()
        return resp.json()

    @property
    def random_api_key(self):
        return random.choice(self._api_keys)

    def _handle_rate_limit(self):
        if len(self._api_keys) > 1:
            self._api_keys.remove(self.sess.headers["TRON-PRO-API-KEY"])
        else:
            print("W: Please add as-many API-Keys in HTTPProvider", file=sys.stderr)
            time.sleep(0.9)
