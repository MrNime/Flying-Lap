"""
Flask f1 app
"""
from flask import Flask, render_template, request
import pickle
from make_tables import make_qualy_htmltable, make_race_htmltable, make_schedule_htmltable

app = Flask(__name__)

@app.route('/')
def home():
    return 'test'

app.run()
