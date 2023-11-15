from ossapi import Ossapi

client_id = None
client_secret = None
def generate_osu_api():
    return Ossapi(client_id, client_secret)