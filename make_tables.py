import glob
import os
import datetime
import pickle
from pathlib import Path
import pandas as pd
from nationality import nationality_to_code
from teamcolors import constructor_id_to_hex

MYDIR = os.path.dirname(__file__)

def get_filepaths(folderpath):
    """
    returns list of filepath in a certain folderpath
    """
    list_of_files = glob.glob(folderpath + '*') # * means all if need specific format then *.csv
    return list_of_files

def make_qualy_htmltable(qualy_pickle_path):
    with open(qualy_pickle_path, 'rb') as f:
        main_dict = pickle.load(f)
    RACETABLE = main_dict['MRData']['RaceTable'] #is een dict
    RACEINFO = RACETABLE['Races'][0] #item 0 (dict) uit list, is alles
    QUALIFYINGRESULTS = RACEINFO['QualifyingResults'] #is een lijst met dicts
    #make an html table and save it
    qualytablelist = []
    for result in QUALIFYINGRESULTS:
        qualytableline = []
        pos = result['position']
        driver = result['Driver']['givenName'] + ' ' + result['Driver']['familyName']
        constructor_id = result['Constructor']['constructorId']
        try:
            hex_code = constructor_id_to_hex(constructor_id)
            teamcircle = """<i class="fa fa-circle" aria-hidden="true" style="color:{}"></i>""".format('#' + str(hex_code))
        except:
            teamcircle = ' '
        if 'Q1' in result.keys():
            q1 = result['Q1']
        else:
            q1 = None
        if 'Q2' in result.keys():
            q2 = result['Q2']
        else:
            q2 = None
        if 'Q3' in result.keys():
            q3 = result['Q3']
        else:
            q3 = None
        curr_fastest_time = '0:00.000'
        time_format = '%M:%S.%f'
        if 'Q3' in result.keys():
            pole_time = datetime.datetime.strptime(QUALIFYINGRESULTS[0]['Q3'], time_format)
        else:
            pole_time = None
        if q3:
            curr_fastest_time = q3
        elif q2:
            curr_fastest_time = q2
        elif q1:
            curr_fastest_time = q1
        curr_fastest_time = datetime.datetime.strptime(curr_fastest_time, time_format)
        gap = ''
        if pole_time:
            time_delta = curr_fastest_time - pole_time
            if time_delta.seconds == 0 and time_delta.microseconds == 0:
                gap = None
            else:
                gap = '+' + str(time_delta.seconds) + '.' + str(time_delta.microseconds)[:3]
        qualytableline.append(pos)
        qualytableline.append(teamcircle)
        qualytableline.append(driver)
        qualytableline.append(q1)
        qualytableline.append(q2)
        qualytableline.append(q3)
        qualytableline.append(gap)
        qualytablelist.append(qualytableline)

    #create pandas dataframe
    df = pd.DataFrame(qualytablelist)

    my_columns = ["POS", "", "Driver", "Q1 Time", "Q2 Time", "Q3 Time", "Gap"]
    #assign column names to the dataframe
    df.columns = my_columns
    #replace the None values with an empty string
    df = df.fillna('')
    #export the dataframe to a HTML table
    # htmltable = df.to_html(index = False, classes='table is-striped', escape=False)

    htmltable = (
        df.style
        .set_table_attributes('border="1" class="table is-striped"') #html op ganse tabel
        .set_properties(**{'text-align': 'right'}, subset=['']) #css op gekozen kolom
        .set_table_styles([{'selector': '.row_heading, .blank', 'props': [('display', 'none;')]}]) #verberg index
        .render()
    )
    season = RACETABLE['season']
    race_round = RACETABLE['round']
    return htmltable

def make_schedule_htmltable(schedule_pickle_path):
    with open(schedule_pickle_path, 'rb') as f:
        main_dict = pickle.load(f)

    RACETABLE = main_dict['MRData']['RaceTable']
    RACE_LIST = RACETABLE['Races']
    season = RACETABLE['season']

    #create pandas dataframe
    df = pd.DataFrame(make_schedule_list(RACE_LIST))

    my_columns = ["Round", "Race Name", "Circuit", "Date", "Q", "R"]
    #assign column names to the dataframe
    df.columns = my_columns

    #avoid truncating, dat em de string afkapt en 3 puntjes zet
    pd.set_option('display.max_colwidth', -1)
    htmltable = df.to_html(index = False, classes='table is-striped', escape=False)
    return htmltable

#helper function that makes schedule list to pass
def make_schedule_list(race_list):
    schedule_table_list = []
    for result in race_list:
        table_line = []
        season = result['season']
        round_nr = result['round']
        race_url = result['url']
        # race_name = result['raceName']
        race_name = '<a href=' + race_url + ' target="_blank">' + result['raceName']
        # circuit_name = result['Circuit']['circuitName']
        circuit_url = result['Circuit']['url']
        circuit_name = '<a href=' + circuit_url + ' target="_blank">' + result['Circuit']['circuitName']
        date = result['date']
        qualy_url = '/qualifying/{}/{}'.format(season, round_nr)
        qualy_file = os.path.join(MYDIR + '/pickles/qualifying_results/{season}/QualifyingResult_f1_{season}_round{round_nr}.pickle'.format(season = season, round_nr = round_nr))
        race_url = '/race/{}/{}'.format(season, round_nr)
        race_file = os.path.join(MYDIR + '/pickles/race_results/{season}/RaceResult_f1_{season}_round{round_nr}.pickle'.format(season = season, round_nr = round_nr))
        qualy_disabled = ''
        if Path(qualy_file).is_file() == False:
            qualy_disabled = 'disabled'
        race_disabled = ''
        if Path(race_file).is_file() == False:
            race_disabled = 'disabled'
        qualy_result = """<a class="button is-primary" href="{}" {}><span class="icon is-small"><i class="fa fa-list-ul" aria-hidden="true"></i></span></a>""".format(qualy_url, qualy_disabled)
        race_result = """<a class="button is-info" href="{}" {}><span class="icon is-small"><i class="fa fa-list-ul" aria-hidden="true"></i></span></a>""".format(race_url, race_disabled)
        table_line.append(round_nr)
        table_line.append(race_name)
        table_line.append(circuit_name)
        table_line.append(date)
        table_line.append(qualy_result)
        table_line.append(race_result)
        schedule_table_list.append(table_line)
    return schedule_table_list

def make_race_htmltable(race_pickle_path):
    with open(race_pickle_path, 'rb') as f:
        main_dict = pickle.load(f)
    RACETABLE = main_dict['MRData']['RaceTable'] #is een dict
    RACEINFO = RACETABLE['Races'][0] #item 0 (dict) uit list, is alles
    RACERESULTS = RACEINFO['Results'] #is een lijst met dicts
    #make an html table and save it
    racetablelist = []
    for result in RACERESULTS:
        racetableline = []
        if 'position' in result.keys():
            pos = result['position']
        if 'Driver' in result.keys():
            driver = result['Driver']['givenName'] + ' ' + result['Driver']['familyName']
            nationality = result['Driver']['nationality']
            try:
                countrycode = nationality_to_code(nationality)
                flag = """<span class="flag-icon flag-icon-{}"></span>""".format(countrycode)
            except:
                flag = ' '
        if 'Constructor' in result.keys():
            constructor_id = result['Constructor']['constructorId']
            try:
                hex_code = constructor_id_to_hex(constructor_id)
                teamcircle = """<i class="fa fa-circle" aria-hidden="true" style="color:{}"></i>""".format('#' + str(hex_code))
            except:
                teamcircle = ' '
        fastest_icon = """<i class="fa fa-clock-o" aria-hidden="true"></i>"""
        if 'FastestLap' in result.keys():
            fastest_lap = '<p style="display:inline">' + result['FastestLap']['Time']['time'] + '</p>'
            if result['FastestLap']['rank'] == str(1):
                fastest_lap +=  ' ' + fastest_icon
        else:
            fastest_lap = ''
        if 'status' in result.keys():
            status = result['status']
        if 'Constructor' in result.keys():
            constructor = result['Constructor']['name']
        racetableline.append(pos)
        racetableline.append(teamcircle)
        racetableline.append(constructor)
        racetableline.append(driver)
        racetableline.append(status)
        racetableline.append(str(fastest_lap))
        racetableline.append(flag + ' ' + nationality)
        racetablelist.append(racetableline)

    #create pandas dataframe
    df = pd.DataFrame(racetablelist)

    my_columns = ["POS", "", "Team", "Driver", "Status", "Fastest Lap", "Nationality"]
    #assign column names to the dataframe
    df.columns = my_columns
    #replace the None values with an empty string
    df = df.fillna('')

    pd.set_option('display.max_colwidth', -1)
    #export the dataframe to a HTML table
    # htmltable = df.to_html(index = False, classes='table is-striped', escape=False)

    htmltable = (
        df.style
        .set_table_attributes('border="1" class="table is-striped"') #html op ganse tabel
        .set_properties(**{'text-align': 'right'}, subset=['']) #css op gekozen kolom
        .set_table_styles([{'selector': '.row_heading, .blank', 'props': [('display', 'none;')]}]) #verberg index
        .render()
    )

    season = RACETABLE['season']
    race_round = RACETABLE['round']
    return htmltable
