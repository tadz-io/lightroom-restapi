import os
import flask
from flask import jsonify, Response
import requests
from six.moves import urllib
import json
from restapi import load_from_session, LightRoomRestApi, AssetCollectionRenderer

# Start flask app
app = flask.Flask(__name__)

# Load config object from config.py
app.config.from_object("config.APIConfig")

# Loading FLAST_SECRET from config.py
app.secret_key = app.config["FLASK_SECRET"]


@app.route("/")
def home():
    print(flask.url_for("callback", _external=True))
    return flask.render_template("index.html")


@app.route("/authorize")
def authorize():
    # Adobe OAuth2.0 authorization url
    authorization_url = (
        "https://ims-na1.adobelogin.com/ims/authorize/v2?"
    )

    # Store required parameters in a dictionary
    params = {
        "client_id": app.config["ADOBE_API_KEY"],
        "scope": "openid lr_partner_apis",
        "response_type": "code",
        "redirect_uri": flask.url_for("callback", _external=True),
    }

    # This will prompt users with the approval page if consent has not been given
    # Once permission is provided, users will be redirected to the specified page
    return flask.redirect(
        authorization_url + urllib.parse.urlencode(params)
    )


@app.route("/callback")
def callback():
    # Retrive the authorization code from callback
    authorization_code = flask.request.args.get("code")

    # Adobe OAuth2.0 token url
    token_url = "https://ims-na1.adobelogin.com/ims/token/v3?"

    # Store required parameters in a dictionary
    # And include the authorization code in it
    params = {
        "grant_type": "authorization_code",
        "client_id": app.config["ADOBE_API_KEY"],
        "client_secret": app.config["ADOBE_API_SECRET"],
        "code": authorization_code,
    }

    # Use requests library to send the POST request
    response = requests.post(
        token_url,
        params=params,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    # After receiving a 'OK' response,
    if response.status_code == 200:
        # save credentials to session
        flask.session["credentials"] = response.json()
        return flask.render_template(
            "index.html", response="login success"
        )
    else:
        return flask.render_template(
            "index.html", response="login failed"
        )


@app.route("/account")
def account():


    #     # Adobe OAuth2.0 profile url
    #     catalog_id = "126d1b0b00d14744891ec255f1ca046f"
    #     asset_id = "1e1aad4964a77c084db0dfe01b0c64b4"
    #     rendition_type = "thumbnail2x"
    #     profile_url = "https://lr.adobe.io/v2/account"
    #     # f"https://lr.adobe.io/v2/catalogs/{catalog_id}/assets"
    #     # profile_url = f"https://lr.adobe.io/v2/catalogs/{catalog_id}/assets/{asset_id}/renditions/{rendition_type}"

    light_room = LightRoomRestApi(api_config=app.config)
    account = light_room.get_account_data()

    return jsonify(account)

@app.route("/catalog")
def catalog():
    light_room = LightRoomRestApi(api_config=app.config)
    catalog = light_room.get_catalog()

    return jsonify(catalog)

@app.route("/assets")
def assets():
    light_room = LightRoomRestApi(api_config=app.config)
    catalog = light_room.get_catalog()
    assets = light_room.get_assets(
        catalog_id=catalog.id
    )
    renderer = AssetCollectionRenderer(api_config=app.config, collection=assets)
    renditions = renderer.get_renditions()
    content_types = [rendition.headers.get('Content-Type') for rendition in renditions]
    # return jsonify(renderer.get_renditions())
    return flask.render_template(
            "index.html",
            response=f"assets: {content_types}",
        )

@app.route("/health")
def health():
    light_room = LightRoomRestApi(api_config=app.config)

    return flask.render_template(
                "index.html",
                response=f"health status: {light_room._check_health_status()}",
            )


if __name__ == "__main__":
    # Make sure the hostname and port you provide match the valid redirect URI
    # specified in your project in the Adobe developer Console.
    # Also, make sure to have `cert.pem` and `key.pem` in your directory
    app.run(
        "localhost",
        8000,
        debug=True,
        ssl_context=("cert.pem", "key.pem"),
    )
