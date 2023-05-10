import json
import re
import time
from pathlib import Path

from . import Session
from . import logger


class Portal(Session):
    MAX_TIMEOUT = 30

    def __init__(self, is_spm_proxy_enabled=False):
        super().__init__()
      

    def get(self, url, **kwargs):
        retry_count = kwargs.pop("retry_count", 0)
        no_raise = kwargs.pop("no_raise", False)
        if retry_count and retry_count >= 3:
            exception = kwargs.get("exception")
            logger.error(f"\nFailed to GET url {url}")
            raise exception
        try:
            kwargs.pop("exception", None)
            response = super().get(url, timeout=self.MAX_TIMEOUT, **kwargs)
            logger.info(f"Response from {url}: {response.status_code}")
            Portal.check_status_code(response, no_raise=no_raise)
            return response
        except Exception as e:
            retry_count += 1
            kwargs["retry_count"] = retry_count
            kwargs["exception"] = e
            time.sleep(2 * retry_count + 2)
            return self.get(url, **kwargs)

    def post(self, url, **kwargs):
        retry_count = kwargs.pop("retry_count", 0)
        no_raise = kwargs.pop("no_raise", False)
        if retry_count and retry_count >= 3:
            exception = kwargs.get("exception")
            logger.error(f"\nFailed to POST to url {url}")
            raise exception
        try:
            kwargs.pop("exception", None)
            response = super().post(url, timeout=self.MAX_TIMEOUT, **kwargs)
            logger.info(f"Response from {url}: {response.status_code}")
            Portal.check_status_code(response, no_raise=no_raise)
            return response
        except Exception as e:
            retry_count += 1
            kwargs["retry_count"] = retry_count
            kwargs["exception"] = e
            return self.post(url, **kwargs)

    def convert_balance_to_cents(self, balance: str):
        balance = balance.replace("$", "")
        balance = balance.replace(",", "")
        return self.to_cents(balance)

    def normalize_negative_amount(self, amount_str: str) -> int:
        """
        Handle negative amount strings - ex:
        (123.45) => -123.45
        :param amount_str: string to perform regex on
        :return: amount in cents
        """
        negative_amount = re.findall("\((.*?)\)", amount_str)
        if negative_amount:
            return -self.convert_balance_to_cents(negative_amount[0].strip())
        return self.convert_balance_to_cents(amount_str.strip())

    @staticmethod
    def check_status_code(response, no_raise=False):
        if no_raise:
            return
        if response.status_code >= 400:
            if response.status_code == 422:
                raise Exception
            if response.status_code == 401:
                raise Exception
            raise Exception


   
