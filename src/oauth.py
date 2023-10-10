# from oauthlib.oauth2 import WebApplicationClient
# import requests

# client_id = "32d76dde6f664a889931c28bc1016c45"
# client_secret = "p8e-N4bnTOI0kURJqmmg1PE_w5qDi-FAhUvZ"
# authorization_url = "https://ims-na1.adobelogin.com/ims/authorize/v2"
# token_url = "https://ims-na1.adobelogin.com/ims/token/v3"
# redirect_uri = "https://adobeioruntime.net"
# client = WebApplicationClient(client_id)
# code = "eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEta2V5LWF0LTEuY2VyIiwia2lkIjoiaW1zX25hMS1rZXktYXQtMSIsIml0dCI6ImF0In0.eyJpZCI6IjE2OTY4NzQ1NDcxNzBfYWQwYjJmYzktMjI1Ni00OThiLWFkOTItOTRlOGYyN2NmNTk0X2V3MSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJjbGllbnRfaWQiOiIzMmQ3NmRkZTZmNjY0YTg4OTkzMWMyOGJjMTAxNmM0NSIsInVzZXJfaWQiOiJBQjJCNTcwOTVGMEYwRjc0MEE0OTVDMDdAQWRvYmVJRCIsInN0YXRlIjoiIiwiYXMiOiJpbXMtbmExIiwiYWFfaWQiOiJBQjJCNTcwOTVGMEYwRjc0MEE0OTVDMDdAQWRvYmVJRCIsImN0cCI6MiwiZmciOiJYM0VFVzRBSFhQUDdNSFdLRU9RVllIQUFXSSIsInNpZCI6IjE2OTY4NzE3MTQ5MjBfN2RlYWFlMmYtYjhiNy00MzRjLWE1ZTgtZDUxYTZlYjA5YjU3X3VlMSIsIm1vaSI6ImVlMzQzYjciLCJwYmEiOiJNZWRTZWNOb0VWLExvd1NlYyIsImV4cGlyZXNfaW4iOiI4NjQwMDAwMCIsImNyZWF0ZWRfYXQiOiIxNjk2ODc0NTQ3MTcwIiwic2NvcGUiOiJvcGVuaWQsQWRvYmVJRCJ9.OwjBo2jdI10QI32a8xjTPAMpgjOOEOsqVRd0xImTyNppUk8oI-ITdRzIxYLfmvmGRPGzCLctR2YJVNP2uzcY3H-xLVZNafbJ1iD5ViDQywS9sie00c5-l2p_x2YQqcu_yQgiGVuPyjHDr22uafHxrkfKVgmcGsNGd72AA0XmihErUp-C2Odu31MA91eRF6rYLADE_VM44mel-33W4t1NYQT5rn8JJ3kQkm7zTUMYRbZY26n7dM-q7YJRUmRREaCd4EBgB2kCaPaJEGQMMLb198PxptJJd8JAXbK29jCnF8to0oyd1so3bD8fU3QfjTZA8sD4_D8GtF2hcum6Oo0QMQ"

# # url = client.prepare_request_uri(
# #     authorization_url, redirect_uri=redirect_uri, scope="openid"
# # )

# data = client.prepare_request_body(
#     # grant_type='authorization_code',
#     client_id=client_id,
#     client_secret=client_secret,
#     code=code,
#     redirect_uri=redirect_uri,
# )

# response = requests.post(token_url, data=data)
# print(response.text)

import requests, json

client_id = "32d76dde6f664a889931c28bc1016c45"
client_secret = "p8e-N4bnTOI0kURJqmmg1PE_w5qDi-FAhUvZ"
authorize_url = "https://ims-na1.adobelogin.com/ims/authorize/v2"
token_url = "https://ims-na1.adobelogin.com/ims/token/v3"
callback_uri = "https://adobeioruntime.net"

test_api_url = "https://lr.adobe.io/v2/account"


# step A - simulate a request from a browser on the authorize_url - will return an authorization code after the user is
# prompted for credentials.

authorization_redirect_url = (
    authorize_url
    + "?response_type=code&client_id="
    + client_id
    + "&redirect_uri="
    + callback_uri
    + "&scope=openid offline_access profile email"
)


print(
    "go to the following url on the browser and enter the code from"
    " the returned url: "
)
print(f"{authorization_redirect_url}")
# authorization_code = input("code: ")
authorization_code = "eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEta2V5LWF0LTEuY2VyIiwia2lkIjoiaW1zX25hMS1rZXktYXQtMSIsIml0dCI6ImF0In0.eyJpZCI6IjE2OTY5MzA5MTUxMDVfYWQwZWViZWYtYzMyNy00YWI3LWJiZjUtNTI3YWQ1YjFkYmYxX3VlMSIsInR5cGUiOiJhdXRob3JpemF0aW9uX2NvZGUiLCJjbGllbnRfaWQiOiIzMmQ3NmRkZTZmNjY0YTg4OTkzMWMyOGJjMTAxNmM0NSIsInVzZXJfaWQiOiJBQjJCNTcwOTVGMEYwRjc0MEE0OTVDMDdAQWRvYmVJRCIsInN0YXRlIjoiIiwiYXMiOiJpbXMtbmExIiwiYWFfaWQiOiJBQjJCNTcwOTVGMEYwRjc0MEE0OTVDMDdAQWRvYmVJRCIsImZnIjoiWDNFVU80QUhWUFA1TUhVS0VNUVZZSEFBQkUiLCJzaWQiOiIxNjk2ODcxNzE0OTIwXzdkZWFhZTJmLWI4YjctNDM0Yy1hNWU4LWQ1MWE2ZWIwOWI1N191ZTEiLCJvdG8iOnRydWUsImV4cGlyZXNfaW4iOiIxODAwMDAwIiwiY3JlYXRlZF9hdCI6IjE2OTY5MzA5MTUxMDUiLCJzY29wZSI6Im9wZW5pZCxBZG9iZUlEIn0.SVgbEZfSvS14KPCckE_2rml7mmFGdYX0UxuHq_IrtsIWk93J1ENXeAyxJ0cNJJuiK2YTtD2u_9zvUpIp1mrW8u761a07nCBlSb0Aq-RHbX94VXpXaSFrnvgjoap1BZUY588XemR4k1rUO4RLFzSPi2QXXxln11zO0ItDr7RzJ4F1nVlhsViVJIYx7EdukDOQImFDeIaKUOGfYcZLFGtYdIeNtnZQ8bYI58kHD9ccbyUmqNy4sqNEO5wXonsHC_UKEqA4QlTTjiT58zp-UzhOQ8JSoCO7AlY-GSmRAFI7ay9tAOY6SjZjINjmt3QW7RRN4yu8UaCcS0FUj2-rZYvH3A"

# step I, J - turn the authorization code into a access token, etc
data = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": callback_uri,
}
print("requesting access token")
access_token_response = requests.post(
    token_url,
    data=data,
    verify=False,
    allow_redirects=False,
    auth=(client_id, client_secret),
)

print("response: ")
print(f"{access_token_response.headers}\n\n\n")
print(f"body: {access_token_response.text}")

# we can now use the access_token as much as we want to access protected resources.
tokens = json.loads(access_token_response.text)
print(f"{tokens.keys()} \n\n")
access_token = tokens["access_token"]
print(f"access token: {access_token}")

api_call_headers = {
    "Authorization": f"Bearer {access_token}",
    "X-API-Key": client_id,
}
api_call_response = requests.get(
    test_api_url, headers=api_call_headers, verify=False
)

print(api_call_response.text)
