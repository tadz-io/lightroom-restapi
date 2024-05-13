from restapi import LightRoomRestApi

client_id = ""
access_token = ""
client = LightRoomRestApi(client_id)

print(f"health status: {client._check_health_status()}")
print("\n")
print(f"account meta: {client._get_account_meta_data(access_token=access_token)}")
