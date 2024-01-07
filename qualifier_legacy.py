from ossapi import Ossapi
from openpyxl import load_workbook
import commons

api = commons.generate_osu_api()
# must equal with template name
tournamentname = 'osumania 7k world cup 2023'
#maxinum = 2, must equal with template parm name in col 3, col 4
seedingconditions = ['avgrank','avgscore']
mappoolIDs = ['rc1','rc2','hb1','ln1','rc3','rc4','ln2','hb2']

qualifier_slots = [(1,16)]

def readQualifierResults():
    wb = load_workbook(filename='sheets/qualifier.xlsx', read_only=True)
    ws = wb.active
    m_row = ws.max_row
    if m_row == None:
        # we will defined an default max mappools size if we couldn't
        # get max_row when reading , usually by xlsx files saved by 3rd
        # software like "google sheet"
        m_row = 400
    results = []
    for i in range(2, m_row + 1):
        result = {
            'name':ws.cell(row=i, column=1).value,
            'place':ws.cell(row=i, column=2).value,
            'mplink': ws.cell(row=i, column=5).value,
            'bg':ws.cell(row=i, column=6).value,
            'seedingScores':[],
            'maps':[]
        }
        if result['name'] is None or result['place'] is None:
            break
        for j in range(0,len(seedingconditions)):
            seedingScore = ws.cell(row=i, column=3+j).value
            if not (seedingScore is None):
                result['seedingScores'].append(seedingScore)
        for j in range(0,len(mappoolIDs)):
            mapScore = ws.cell(row=i, column=7+ j*2 + 1).value
            mapPlace = ws.cell(row=i, column=7+ j*2 ).value
            if mapScore is None or mapPlace is None:
                break
            else:
                map = {
                    'score':f'{mapScore:,}',
                    'place':mapPlace
                }
                result['maps'].append(map)
        results.append(result)
    return results

def createQualifierResultRow(qualifierResult):
    name = qualifierResult['name']
    place = qualifierResult['place']
    mplink = qualifierResult['mplink']
    bg = qualifierResult['bg']
    seedingScores = qualifierResult['seedingScores']
    maps = qualifierResult['maps']
    result = '{{TableRow/Qualifier/'
    result += tournamentname + '|' + name + '|place=' + str(place)
    for i in range(0,len(seedingconditions)):
        try:
            seedingCondition = seedingconditions[i]
            seedingScore = seedingScores[i]
            result += '|' + seedingCondition + '=' + str(seedingScore)
        except Exception as e:
            print(f'Team {name} haven\'t enough seeding scores.')
            print(e)
    result += '\n'
    if not (mplink is None):
        result += '|mplink=' + mplink
    result += '|bg=' + bg + '\n'
    for i in range(0,len(mappoolIDs)):
        placeMark = mappoolIDs[i] + 'p'
        scoreMark = mappoolIDs[i] + 's'
        try:
            place = maps[i]['place']
            score = maps[i]['score']
            result += '|' + placeMark + '=' + str(place) + '|' + scoreMark + '=' + str(score)
        except Exception as e:
            print(f'Team {name} haven\'t enough map scores.')
            print(e)
        if i % 3 == 2:
            result += '\n'
    result+='}}'
    return result

def createPrizeRow(qualifierResult,qualifieds_range = []):
    name = qualifierResult['name']
    place = qualifierResult['place']
    result = '|{{Slot'
    for i in range(0,len(qualifieds_range)):
        if place in range(qualifieds_range[i][0],qualifieds_range[i][1]+1):
            result += f'|qualified{i+1}=true'
    result += '|{{Opponent|'+name+'}}}}'
    return result

if __name__ == '__main__':
    qualifierResults = readQualifierResults()
    with open('reuslt_qualifier_table.txt','w') as resultFile:
        for qualifierResult in qualifierResults:
            resultRow = createQualifierResultRow(qualifierResult)
            resultFile.writelines(resultRow + '\n')
    with open('reuslt_qualifier_prizepool.txt','w') as resultFile:
        for qualifierResult in qualifierResults:
            resultRow = createPrizeRow(qualifierResult,qualifier_slots)
            resultFile.writelines(resultRow + '\n')