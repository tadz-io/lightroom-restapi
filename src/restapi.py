import requests
import os


class LightRoomRestApi:
    _base_url = "https://lr.adobe.io/v2/"
    _api_key_header = "X-API-Key"
    _authorization_token_header = "Authorization"

    def __init__(self, api_key):
        self._api_key = api_key

    def _check_health_status(self):
        url = os.path.join(self._base_url, "health")
        return requests.get(
            url, headers={self._api_key_header: self._api_key}
        ).status_code

    def _get_account_meta_data(self, access_token):
        url = os.path.join(self._base_url, "account")
        headers = {
            self._api_key_header: self._api_key,
            self._authorization_token_header: access_token
        }

        return requests.get(url, headers=headers)