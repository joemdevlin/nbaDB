import csv
import time
import os.path
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import leaguegamelog

# https://stackoverflow.com/questions/3086973/how-do-i-convert-this-list-of-dictionaries-to-a-csv-file
def listOfDicToFile(tables, path):
    keys = tables[0].keys()
    with open(path, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(tables)

def csvToArrayDic(path):
    myDict = []
    fp = csv.DictReader(open(path))
    for row in fp:
        myDict.append(row)
    return myDict

def headersAndRowsToCSV(headers, rows, path):
    with open(path, 'w') as outFile:
        outFile.write(",".join(headers) + "\n")
        for row in rows:
            rowStr = [str(r) for r in row]
            outFile.write(",".join(rowStr) + "\n")

# Simple Team info such as location and name
teamDataPath = './data/teams.csv'
if not os.path.exists(teamDataPath):
    listOfDicToFile(teams.get_teams(), teamDataPath)
teamsInfo = csvToArrayDic(teamDataPath)

for team in teamsInfo:
    rosterPath = './data/' + team['abbreviation'] + '_roster.csv'
    print(rosterPath)
    if not os.path.exists(rosterPath):
        time.sleep(1)
        resp = commonteamroster.CommonTeamRoster(team['id'], proxy=False)
        rosterDict = resp.common_team_roster.get_dict()
        headers = rosterDict['headers']
        data = rosterDict['data']
        headersAndRowsToCSV(headers, data, rosterPath)
    rosterInfo = csvToArrayDic(rosterPath)

gameLogPath = './data/gameLogs.csv'
gameLog = leaguegamelog.LeagueGameLog(proxy=False)
gameLogDict = gameLog.league_game_log.get_dict()
headers = gameLogDict['headers']
data = gameLogDict['data']
headersAndRowsToCSV(headers, data, gameLogPath)
