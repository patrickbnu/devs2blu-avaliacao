import unittest
"""import vcr"""

from portals import AvaliacaoPortal


class AvaliacaoPortalTestCase(unittest.TestCase):

    """@vcr.use_cassette("fixtures/vcr_cassettes/avaliacao_portal/login.yaml",)"""
    def test__login(self):
        portal = AvaliacaoPortal(
            username="some_username",
            password="some_password",
            login_url="https://www.clickpay.com/custom/clickpay/login.html",
        )
        assert portal.token is not None

   
    """@vcr.use_cassette("fixtures/vcr_cassettes/avaliacao_portal/test_validate_credentials.yaml",)"""
    def test_validate_credentials(self):
        portal = AvaliacaoPortal(
            username="some_username",
            password="some_password",
            login_url="https://www.clickpay.com/custom/clickpay/login.html",
        )
        self.assertEqual(
            portal.validate_credentials(), "",
        )

  
  
