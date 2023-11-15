import ossapi
from ossapi import Ossapi
from openpyxl import load_workbook
from openpyxl import Workbook
import commons

api = commons.generate_osu_api()

def readTeams():
    wb = load_workbook(filename='sheets/participate.xlsx', read_only=True)
    ws = wb.active
    m_row = ws.max_row
    teams = []
    for i in range(2, m_row + 1):
        team = {}
        team['name'] = ws.cell(row=i, column=1).value
        team['players'] = ws.cell(row=i, column=2).value
        team['qualifier'] = ws.cell(row=i, column=3).value
        teams.append(team)
    return teams


def cleanTags(playerName:str):
    tags = ['[GB]','[Crz]','[Paw]','[LS]','[Mom]','ERA ','[RS]','[KN]','[RUE]',
            '[MR]','[GS]','[HD]','[SPNG]','[Mom]','[TMEO]']
    for tag in tags:
        #assume clan tags always at the beginning of the id.
        if playerName.startswith(tag):
            playerName = playerName[len(tag):]
    return playerName

def cleanString(stringToClean):
    targets = [' ']
    for target in targets:
        stringToClean = stringToClean.replace(target,"")
    return stringToClean

def generateTeamCardInfo(team):
    result = '{{TeamCard\n' + \
             '|team=' + team['name'] + '\n'
    players = cleanString(team['players']).split(',')
    for i in range(0,len(players)):
        player = str(players[i])
        print('generate ' + player + '\'s info...')
        try:
            player_Country = api.user(player).country_code
        except Exception as e:
            print('error finding player country:' + player)
            print(e)
            player_Country = ''
        player_name_clean = cleanTags(player)
        result +=f'|p{i+1}={player_name_clean} |p{i+1}flag={player_Country}'
        if '[' in player_name_clean and ']' in player_name_clean:
            parsed_player_name = player_name_clean.replace("[","(").replace("]",")")
            result +=f' |p{i+1}link={parsed_player_name}'
        if i == 0:
            result += ' |captain=true\n'
        else:
            result += '\n'
    if not team['qualifier'] is None:
        result += '|qualifier=' + team['qualifier'] + '\n'
    result += '}}\n'
    return result

if __name__ == '__main__':
    teams = readTeams()
    result = ''
    for i in range(0,len(teams)):
        # print('generate ' + teams[i]['name'] + 's info...')
        result += generateTeamCardInfo(teams[i])
        if i < len(teams):
            result += '\n'

    f = open("teamcardresult_seprate.txt", "w", encoding='utf-8')
    f.write(result)
    f.close()
