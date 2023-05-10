import json
import re
from urllib.parse import urlparse, urljoin

from api import HTTPPortal


class AvaliacaoPortal(HTTPPortal):
    base_url = "https://www.clickpay.com/"

    def __init__(self, username, password, login_url):
        super().__init__(
            username=username,
            password=password,
            login_url=login_url,
        )
        self.token = None
        self.login()

    def login(self):
        try:
            login_page = self.get(self.login_url)
            iframe = login_page.first(".//iframe")
            src_url = iframe.get("src").replace("../../", "")

            landing_login_page = self.get(urljoin(self.base_url, src_url))
            login_form = landing_login_page.first(".//form")
            login_data = login_form.data()
            remove_keys = {
                "h_uc_UCLoginForm$h_P_HomePage_Login$h_hp_btn_Login",
                "h_uc_UCLoginForm$h_P_HomePage_Login$h_lnk_Register",
            }
            login_data = {k: v for k, v in login_data.items() if k not in remove_keys}
            login_data.update(
                {
                    "__EVENTTARGET": "LOGIN",
                    "__EVENTARGUMENT": "undefined",
                }
            )
            landing_page = self.post(
                urljoin(self.base_url, login_form.action.lstrip(".")),
                data=login_data,
                headers={
                    "referer": landing_login_page.url,
                },
            )
            app = self.get(
                "https://www.clickpay.com/app",
                headers={
                    "referer": landing_login_page.url,
                },
            )
            token_element = app.elements(".//input[@id='antiForgeryToken']")
            if not token_element:
                raise Exception("Login failed", landing_page.text_content())
            self.token = token_element[0].value
        except Exception as e:
            raise Exception("Could not log in", e)

    def validate_credentials(self) -> str:
        try:
            profile = self.get_profile(request_type="get_user_paynow_desktop")

            if not profile.get("Result") or profile.get("Error"):
                return "xxx"
            return "yyy"
        except Exception as e:
            raise Exception("Could not validate credentials", e)

  