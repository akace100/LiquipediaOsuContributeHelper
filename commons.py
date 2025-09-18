import json

from oauthlib.oauth2 import InvalidClientIdError
from ossapi import Ossapi

def generate_osu_api():
    try:
        with open("secret.json") as f:
            data = json.load(f)
            client_id = data["osu_apikeys"]["client_id"]
            client_secret = data["osu_apikeys"]["client_secret"]
        api_obj = Ossapi(client_id, client_secret)
    except InvalidClientIdError as e:
        print('please fill client_id / secret in /secret.json before using\n'
            + 'You can find on osu!web settings (https://osu.ppy.sh/home/account/edit)')
        print(e)
        api_obj = None
    return api_obj

def clean_clan_tags(player_name: str):
    tags = ['[GB]', '[Crz]', '[Paw]', '[LS]', '[Mom]', 'ERA ', '[RS]', '[KN]', '[RUE]',
            '[MR]', '[GS]', '[HD]', '[SPNG]', '[Mom]', '[TMEO]', '[MY]', '[MBR]', '[MG]',
            '[TCD]', '[Sick]', '[AR]', '[DT]', '[Monkey]', '[BBC]', '[Szy]']
    for tag in tags:
        # assume clan tags always at the beginning of the id.
        if player_name.startswith(tag):
            player_name = player_name[len(tag):]
    return player_name


def clean_string(string_to_clean: str):
    targets = [' ']
    for target in targets:
        string_to_clean = string_to_clean.replace(target, "")
    return string_to_clean


def get_player_osuflag(player_id):
    api = generate_osu_api()
    player_country = ''
    try:
        player_country = api.user(player_id).country_code
    except Exception as e:
        if not isinstance(player_id, str):
            player_id = str(player_id)
            print('error finding player\'s osu flag:' + player_id)
        print(e)
    return player_country

