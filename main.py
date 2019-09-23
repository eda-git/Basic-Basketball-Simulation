### This is a very basic simulation 
#math.sqrt(teamOne["Points For"] * teamTwo["Points Against"]), std_dev, num_reps
# Each team is represented by a Normal Distribution where the mean is (team PF * opp PA). 
# Mean of standard deviations of scores across the NBA in the 2018-19 season was 4.46  (https://shrstats.com/pace-control/).
# Even though that might not be entirely accurate, I made this for fun :^)
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import numpy as np
import math
import random
import sqlite3
from sqlite3 import Error
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'NBA Simulation'
        self.left = 10
        self.top = 50
        self.width = 640
        self.height = 480
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        homeValue = self.getTeam("Home: ")
        awayValue = self.getTeam("Away: ")
        teamOne = self.dbGet(homeValue)
        teamTwo = self.dbGet(awayValue)
        getGameTotal = self.getGameTotal()
        result = self.tipOff(teamOne, teamTwo, getGameTotal)
        self.final(result)
        windowLayout = QVBoxLayout()
        self.setLayout(windowLayout)


        self.show()
    
    def final(self, result):
        hbox = QHBoxLayout(self)

        splitter1 = QSplitter(Qt.Horizontal)
        self.awayGame = QLabel()
        self.awayGame.setObjectName("awayGame")
        self.awayGame.setText(f"""{result["away"]["Name"]}: {result["away"]["Wins"]}""")
        self.homeGame = QLabel()
        self.homeGame.setObjectName("homeGame")
        self.homeGame.setText(f"""{result["home"]["Name"]}: {result["home"]["Wins"]}""")
        topSplit.addWidget(self.awayGame)
        topSplit.addWidget(self.homeGame)

        bottomSplit = QSplitter(Qt.Vertical)
        self.le = QPlainTextEdit()
        self.le.setObjectName("host")
        self.le.insertPlainText(result["notes"])
        bottomSplit.addWidget(splitter1)
        bottomSplit.addWidget(self.le)

        hbox.addWidget(bottomSplit)
        self.setLayout(hbox)
        
        self.setGeometry(300, 300, 600, 400)
        
        self.setWindowTitle("NBA Simulation: " + result["home"]["Name"] + " vs. " + result["away"]["Name"])

    
    def dbGet(self, value):
        conn = None
        database = r"./data.db"
        try:
            conn = sqlite3.connect(database)
        except Error as e:
            print(e)
        cur = conn.cursor()
        cur.execute(f"SELECT team, pf, pa FROM Stats where team like '%{value}%'")
        rows = cur.fetchall()
        for teamInfo in rows:
            retValue = {
            "Team Name": teamInfo[0],
            "Points For": teamInfo[1],
            "Points Against": teamInfo[2],
            }
        print(retValue)
        return retValue
		
    def tipOff(self, teamOne, teamTwo, Games):
        counter = 0
        oneWins = 0
        twoWins = 0
        totalSims = 0
        gameNotes = ""
        while(counter < Games):
            std_dev = 4.46
            num_reps = 1
            x = random.randint(0, num_reps)
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
            gameNotes = gameNotes + (f"""
            {teamOne["Team Name"]}: {Score_A}
            {teamTwo["Team Name"]}: {Score_B}
            Total Simulations: {totalSims}
            """)
            counter = counter + 1
        if(oneWins == twoWins):
            pointsFor_a = np.random.normal(math.sqrt(teamOne["Points For"] * teamTwo["Points Against"]), std_dev, 1).round(2)
            pointsFor_b = np.random.normal(math.sqrt(teamTwo["Points For"] * teamOne["Points Against"]), std_dev, 1).round(2)
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
            gameNotes = gameNotes + (f"""
            {teamOne["Team Name"]}: {Score_A}
            {teamTwo["Team Name"]}: {Score_B}
            Total Simulations: {totalSims}
            """)

        print(f"""
        Total Wins:
        {teamOne["Team Name"]}: {oneWins}
        {teamTwo["Team Name"]}: {twoWins}
        """)
        context = {
            "notes": gameNotes,
            "home": {
                "Name": teamOne["Team Name"],
                "Wins": oneWins
            },
            "away": {
                "Name": teamTwo["Team Name"],
                "Wins": twoWins
            }
        }
        return context
        
    def getTeam(self, location):
        conn = None
        database = r"./data.db"
        try:
            conn = sqlite3.connect(database)
        except Error as e:
            print(e)
        cur = conn.cursor()
        cur.execute("SELECT team FROM Stats")
        items = [item[0] for item in cur.fetchall()]
        items, okPressed = QInputDialog.getItem(self, "Get item",location, items, 0, False)
        return items
    def getGameTotal(self):
        i, okPressed = QInputDialog.getInt(self, "How Many Games Will Be Played?","How Many Games:", 100, 0, 10000, 1)
        if okPressed:
            print(i)
        return i

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())