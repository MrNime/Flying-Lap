"""
Flask f1 app
"""
from flask import Flask, render_template, request
import pickle
import os
from make_tables import make_qualy_htmltable, make_race_htmltable, make_schedule_htmltable

app = Flask(__name__)

MYDIR = os.path.dirname(__file__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/qualifying/<season>/<ronde>')
def qualy_results(season, ronde):
    season = str(season)
    ronde = str(ronde)
    pickle_path = "pickles\\qualifying_results\\QualifyingResults_f1_{}_round{}.pickle".format(season, ronde)
    with open(pickle_path, 'rb') as f:
        main_dict = pickle.load(f)
    table = make_qualy_htmltable(pickle_path)
    return render_template('qualifyingresult.html', dict = main_dict, table = table)

@app.route('/schedule')
def schedule_page():
    pickle_path = os.path.join(MYDIR + '\\' + 'pickles\\schedules\\ScheduleTable_f1_2017.pickle')
    with open(pickle_path, 'rb') as f:
        main_dict = pickle.load(f)
    table = make_schedule_htmltable(pickle_path)
    return render_template('schedule.html', dict = main_dict, table = table)

@app.route('/race/<season>/<ronde>')
def race_results(season, ronde):
    season = str(season)
    ronde = str(ronde)
    pickle_path = "pickles\\race_results\\RaceResult_f1_{}_round{}.pickle".format(season, ronde)
    with open(pickle_path, 'rb') as f:
        main_dict = pickle.load(f)
    table = make_race_htmltable(pickle_path)
    return render_template('raceresult.html', dict = main_dict, table = table)

#testen of een route werkt
def test_route(route_path):
    with app.test_client() as c:
        response = c.get(route_path)
        return response.status_code
