import requests
from typing import Dict
from datetime import date

from api.portal_http_interface import PortalHttpInterface
from api.portal import Portal
from api.xpath_utils import bind_custom_html_element


class HTTPPortal(Portal):

    def __init__(self, username, password,  **kwargs):
        super().__init__()
        self.username = username
        self.password = password
        self.login_url = kwargs.get("login_url")
        self.headers.update({
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.63 Safari/537.36'
        })

    def cookies_as_dict(self):
        cookies = {}
        for cookie in self.cookies:
            cookies[cookie.name] = {
                "value": cookie.value,
                "domain": cookie.domain,
            }
        return cookies

    def get(self, url, **kwargs):
        response = super().get(url, **kwargs)
        return bind_custom_html_element(response)

    def _get(self, url, **kwargs):
        """
        Get request that doesn't use object's cookies
        """
        response = requests.get(url, **kwargs)
        return bind_custom_html_element(response)

    def post(self, url, **kwargs):
        response = super().post(url, **kwargs)
        return bind_custom_html_element(response)

    def submit(self, form, data: Dict = {}, **kwargs):
        url = form.action
        if not data:
            data = form.data()
        return self.post(url, data=data, **kwargs)
