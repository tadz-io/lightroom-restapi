import requests
import os
from flask import session
from dataclasses import dataclass
import json
from typing import Literal


@dataclass
class UserSession:
    access_token: str = None
    expires_in: int = None
    id_token: str = None
    token_type: str = None


@dataclass
class Catalog:
    base: str = None
    created: str = None
    id: str = None
    links: dict = None
    payload: dict = None
    subtype: str = None
    type: str = None
    updated: str = None


@dataclass
class Asset:
    created: str = None
    id: str = None
    links: dict = None
    payload: dict = None
    subtype: str = None
    type: str = None
    updated: str = None


@dataclass
class AssetColletion:
    base: str = None
    last_updated: str = None
    links: dict = None
    resources: list[Asset] = None


def load_from_session() -> UserSession:
    credentials = session.get("credentials")
    return UserSession(**credentials)


class LightRoomRestApi:
    _base_url = "https://lr.adobe.io/v2/"

    def __init__(self, api_config):
        self._session = load_from_session()
        self._api_credentials = {
            "X-API-Key": api_config.get("ADOBE_API_KEY"),
            "Authorization": f"Bearer {self._session.access_token}",
        }

    def _check_health_status(self):
        url = os.path.join(self._base_url, "health")
        return requests.get(
            url, headers=self._api_credentials
        ).status_code

    def get_account_data(self):
        url = os.path.join(self._base_url, "account")
        response = requests.get(url, headers=self._api_credentials)
        return self._to_json(response.text)

    def get_catalog(self):
        url = os.path.join(self._base_url, "catalog")
        response = requests.get(url, headers=self._api_credentials)
        json_response = self._to_json(response.text)
        # return json_response
        return Catalog(**json_response)

    def get_assets(self, catalog_id):
        url = os.path.join(
            self._base_url, f"catalogs/{catalog_id}/assets"
        )
        response = requests.get(url, headers=self._api_credentials)
        json_response = self._to_json(response.text)
        return AssetColletion(**json_response)

    def _to_json(self, text):
        # return text
        return json.loads(text[len("while (1) {}\n") :])


class AssetCollectionRenderer:

    def __init__(self, api_config, collection: AssetColletion) -> None:
        self._collection = collection
        self._base_url = collection.base
        self._session = load_from_session()
        self._api_credentials = {
            "X-API-Key": api_config.get("ADOBE_API_KEY"),
            "Authorization": f"Bearer {self._session.access_token}",
        }

    def get_renditions(
        self,
        rendition_type: Literal[
            "thumbnail2x", "fullsize", "640", "1280", "2048", "2560"
        ] = "thumbnail2x",
    ):
        responses = []
        for asset in self._collection.resources:
            url = os.path.join(
                self._base_url,
                f"assets/{asset.get('id')}/renditions/{rendition_type}"
            )
            response = requests.get(url, headers=self._api_credentials)
            responses.append(response)
        return responses