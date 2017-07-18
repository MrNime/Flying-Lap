import glob
import os
import datetime
import pickle
import pandas as pd

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
        qualytableline.append(pos)
        driver = result['Driver']['code']
        qualytableline.append(driver)
        if 'Q1' in result.keys():
            q1 = result['Q1']
        qualytableline.append(q1)
        if 'Q2' in result.keys():
            q2 = result['Q2']
        else:
            q2 = None
        qualytableline.append(q2)
        if 'Q3' in result.keys():
            q3 = result['Q3']
        else:
            q3 = None
        qualytableline.append(q3)
        curr_fastest_time = '0:00.000'
        time_format = '%M:%S.%f'
        pole_time = datetime.datetime.strptime(QUALIFYINGRESULTS[0]['Q3'], time_format)
        if q3:
            curr_fastest_time = q3
        elif q2:
            curr_fastest_time = q2
        elif q1:
            curr_fastest_time = q1
        curr_fastest_time = datetime.datetime.strptime(curr_fastest_time, time_format)
        time_delta = curr_fastest_time - pole_time
        if time_delta.seconds == 0 and time_delta.microseconds == 0:
            gap = None
        else:
            gap = '+' + str(time_delta.seconds) + '.' + str(time_delta.microseconds)[:3]
        qualytableline.append(gap)
        qualytablelist.append(qualytableline)

    #create pandas dataframe
    df = pd.DataFrame(qualytablelist)

    my_columns = ["POS", "Driver", "Q1 Time", "Q2 Time", "Q3 Time", "Gap"]
    #assign column names to the dataframe
    df.columns = my_columns
    #replace the None values with an empty string
    df = df.fillna('')
    #export the dataframe to a HTML table
    htmltable = df.to_html(index = False, classes='table is-striped')
    season = RACETABLE['season']
    race_round = RACETABLE['round']
    with open('F1Project\\templates\\includes\\QualifyingTable_f1_{}_round{}.html'.format(season, race_round), "w", encoding="utf-8") as html_file:
        html_file.write(htmltable)

# for filepath in get_filepaths('F1Project\\pickles\\qualifying_results\\'):
#     make_qualy_htmltable(filepath)

def make_schedule_htmltable(schedule_pickle_path):
    with open(schedule_pickle_path, 'rb') as f:
        main_dict = pickle.load(f)

    RACETABLE = main_dict['MRData']['RaceTable']
    RACE_LIST = RACETABLE['Races']
    season = RACETABLE['season']

    #create pandas dataframe
    df = pd.DataFrame(make_schedule_list(RACE_LIST))

    my_columns = ["Round", "Race Name", "Circuit", "Date", "Q Results"]
    #assign column names to the dataframe
    df.columns = my_columns

    #avoid truncating, dat em de string afkapt en 3 puntjes zet
    pd.set_option('display.max_colwidth', -1)
    htmltable = df.to_html(index = False, classes='table is-striped', escape=False)

    with open('F1Project\\templates\\includes\\ScheduleTable_f1_{}.html'.format(season), "w", encoding="utf-8") as f:
        f.write(htmltable)

#helper function that makes schedule list to pass
def make_schedule_list(race_list):
    schedule_table_list = []
    for result in race_list:
        table_line = []
        season = result['season']
        round_nr = result['round']
        race_url = result['url']
        # race_name = result['raceName']
        race_name = '<a href=' + race_url + '>' + result['raceName']
        # circuit_name = result['Circuit']['circuitName']
        circuit_url = result['Circuit']['url']
        circuit_name = '<a href=' + circuit_url + '>' + result['Circuit']['circuitName']
        date = result['date']
        url = 'qualifying/{}/{}'.format(season, round_nr)
        results = """<a class="button is-info" href="{}"><span class="icon is-small"><i class="fa fa-list-ul" aria-hidden="true"></i></span></a>""".format(url)
        table_line.append(round_nr)
        table_line.append(race_name)
        table_line.append(circuit_name)
        table_line.append(date)
        table_line.append(results)
        schedule_table_list.append(table_line)
    return schedule_table_list

# make_schedule_htmltable('F1Project\\pickles\\schedules\\ScheduleTable_f1_2017.pickle')
