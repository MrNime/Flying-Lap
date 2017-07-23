"""
Flask f1 app
"""
from flask import Flask, render_template, request, redirect, url_for
import pickle
import os
from make_tables import make_qualy_htmltable, make_race_htmltable, make_schedule_htmltable

app = Flask(__name__)

MYDIR = os.path.dirname(__file__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/qualifying/<season>/<ronde>')
def qualy_results(season, ronde):
    season = str(season)
    ronde = str(ronde)
    pickle_path = os.path.join(MYDIR + '/' + 'pickles/qualifying_results/{season}/QualifyingResult_f1_{season}_round{ronde}.pickle'.format(season = season, ronde = ronde))
    with open(pickle_path, 'rb') as f:
        main_dict = pickle.load(f)
    table = make_qualy_htmltable(pickle_path)
    return render_template('qualifyingresult.html', dict = main_dict, table = table)

@app.route('/schedule/<int:year>', methods=['GET', 'POST'])
def schedule_page(year):
    year = str(year)
    pickle_path = os.path.join(MYDIR + '/' + 'pickles/schedules/ScheduleTable_f1_{}.pickle'.format(year))
    choices = [(str(x), str(x)) for x in range(2000, 2018)]
    selected = request.form.get('year', year)
    state = {'choice': selected}
    if request.method == 'POST':
        return redirect(url_for('schedule_page', year=state['choice']))
    with open(pickle_path, 'rb') as f:
        main_dict = pickle.load(f)
    table = make_schedule_htmltable(pickle_path)
    return render_template('schedule.html', dict = main_dict, table = table, choices = choices, state = state)

@app.route('/race/<season>/<ronde>')
def race_results(season, ronde):
    season = str(season)
    ronde = str(ronde)
    pickle_path = os.path.join(MYDIR + '/' + 'pickles/race_results/{season}/RaceResult_f1_{season}_round{ronde}.pickle'.format(season = season, ronde = ronde))
    with open(pickle_path, 'rb') as f:
        main_dict = pickle.load(f)
    table = make_race_htmltable(pickle_path)
    return render_template('raceresult.html', dict = main_dict, table = table)

if __name__ == '__main__':
    app.run(debug = True)

#testen of een route werkt
def test_route(route_path):
    with app.test_client() as c:
        response = c.get(route_path)
        return response.status_code
