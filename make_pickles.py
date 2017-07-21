import pickle
import requests
import os

MYDIR = os.path.dirname(__file__)

def make_schedule_pickle(sched_api_url):
    SCHED_RQST = requests.get(str(sched_api_url))
    SCHED_DICT = SCHED_RQST.json()
    RACETABLE = SCHED_DICT['MRData']['RaceTable']
    season = RACETABLE['season']
    pickle_path = os.path.join(MYDIR + '/pickles/schedules/ScheduleTable_f1_{}.pickle'.format(season))
    with open(pickle_path, "wb") as f:
        pickle.dump(SCHED_DICT, f)

def make_race_result_pickle(api_url):
    RQST = requests.get(str(api_url))
    RQST_DICT = RQST.json()
    RACETABLE = RQST_DICT['MRData']['RaceTable']
    season = RACETABLE['season']
    round_nr = RACETABLE['round']
    pickle_path = os.path.join(MYDIR + '/pickles/race_results/{season}/RaceResult_f1_{season}_round{round}.pickle'.format(season = season, round = round_nr))
    with open(pickle_path, "wb") as f:
        pickle.dump(RQST_DICT, f)

# for season in range(2013, 2017):
#     for round_nr in range(1,11):
#         make_race_result_pickle('http://ergast.com/api/f1/{}/{}/results.json'.format(season, round_nr))

def make_qualy_result_pickle(api_url):
    RQST = requests.get(str(api_url))
    RQST_DICT = RQST.json()
    RACETABLE = RQST_DICT['MRData']['RaceTable']
    season = RACETABLE['season']
    round_nr = RACETABLE['round']

    with open(os.path.join(MYDIR + '\\pickles\\qualifying_results\\{season}\\QualifyingResult_f1_{season}_round{round}.pickle'.format(season = season, round = round_nr)), "wb") as f:
        pickle.dump(RQST_DICT, f)
