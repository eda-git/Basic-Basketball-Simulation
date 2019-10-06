import random 
import numpy as np
import math
import sqlite3
from sqlite3 import Error
def dbGet(value):
    conn = None
    database = r"./data.db"
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)
    cur = conn.cursor()
    cur.execute(f"SELECT team, pf, pa, abb FROM Stats where abb like '%{value}%'")
    rows = cur.fetchall()
    for teamInfo in rows:
        retValue = {
        "Team Name": teamInfo[0],
        'Abb': teamInfo[3],
        "Points For": teamInfo[1],
        "Points Against": teamInfo[2],
        }
    return retValue
def tipOff(teamOne, teamTwo, Games):
        counter = 0
        oneWins = 0
        twoWins = 0
        totalSims = 0
        #gameNotes is a list of dictionaries of each game and its details. This will be used in the for loop in the template (gameplay.html)
        gameNotes = []
        while(counter < Games):
            # Each team is represented by a Normal Distribution where the mean is (team PF * opp PA). 
            # Mean of standard deviations of scores across the NBA in the 2018-19 season was 4.46  (https://shrstats.com/pace-control/).
            # Even though that might not be entirely accurate, I made this for fun :^)
            std_dev = 4.46
            num_reps = 1
            x = random.randint(0, num_reps)
            #Normal Distribution based on the square root of PF^PA, standard deviation = std_dev
            pointsFor_a = np.random.normal(math.sqrt(teamOne["Points For"] * teamTwo["Points Against"]), std_dev, num_reps).round(2)
            pointsFor_b = np.random.normal(math.sqrt(teamTwo["Points For"] * teamOne["Points Against"]), std_dev, num_reps).round(2)
            Score_A = math.floor(np.mean(pointsFor_a))
            Score_B = math.floor(np.mean(pointsFor_b))
            if(Score_A > Score_B):
                oneWins = oneWins + 1
            elif(Score_A == Score_B):
                choice = random.randint(1, 2)
                if(choice == 1):
                    Score_A = Score_A + 1
                    oneWins = oneWins + 1
                else:
                    Score_A = Score_A - 1
                    twoWins = twoWins + 1
            else:
                twoWins = twoWins + 1
            totalSims = totalSims + 1
            gameData = {
                'gameID': totalSims,
                'awayData': teamOne,
                'away': teamOne["Team Name"],
                'awayScore': Score_A,
                'homeData': teamOne,
                'home': teamTwo["Team Name"],
                'homeScore': Score_B,
            }
            gameNotes.append(gameData)
            counter = counter + 1
        if(oneWins == twoWins):
            pointsFor_a = np.random.normal(math.sqrt(teamOne["Points For"] * teamTwo["Points Against"]), std_dev, 1).round(2)
            pointsFor_b = np.random.normal(math.sqrt(teamTwo["Points For"] * teamOne["Points Against"]), std_dev, 1).round(2)
            Score_A = math.floor(np.mean(pointsFor_a))
            Score_B = math.floor(np.mean(pointsFor_b))
            if(Score_A > Score_B):
                #If Team A wins, then add a win 
                oneWins = oneWins + 1
            elif(Score_A == Score_B):
                #If a game is tied, flip a coin to determine the winner
                choice = random.randint(1, 2)
                if(choice == 1):

                    Score_A = Score_A + 1
                    oneWins = oneWins + 1
                else:
                    Score_A = Score_A - 1
                    twoWins = twoWins + 1
            else:
                twoWins = twoWins + 1
            totalSims = totalSims + 1
            gameData = {
                'gameID': totalSims,
                'awayData': teamOne,
                'away': teamOne["Team Name"],
                'awayScore': Score_A,
                'homeData': teamOne,
                'home': teamTwo["Team Name"],
                'homeScore': Score_B,
            }
            gameNotes.append(gameData)
        context = {
            "notes": gameNotes,
            "gameTotal": Games,
            "away": {
                "Name": teamOne["Team Name"],
                "Wins": oneWins,
                "Abb": teamOne["Abb"]
            },
            "home": {
                "Name": teamTwo["Team Name"],
                "Wins": twoWins,
                "Abb": teamTwo["Abb"]
            }
        }
        return context