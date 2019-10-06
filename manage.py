from flask import Flask
from gui import init_gui

app = Flask(__name__)
# Reduces Cache Time for Static Files
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
from routes import *



if __name__ == '__main__':
    init_gui(app)