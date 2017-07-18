import pickle
import requests
import os

MYDIR = os.path.dirname(__file__)

def make_schedule_pickle(sched_api_url):
    SCHED_RQST = requests.get(str(sched_api_url))
    SCHED_DICT = SCHED_RQST.json()
    RACETABLE = SCHED_DICT['MRData']['RaceTable']
    season = RACETABLE['season']
    pickle_path = os.path.join(MYDIR + '\\' + 'pickles\\schedules\\ScheduleTable_f1_{}.pickle'.format(season))
    with open(pickle_path, "wb") as f:
        pickle.dump(SCHED_DICT, f)

# make_schedule_pickle('http://ergast.com/api/f1/current.json')

def make_race_result_pickle(api_url):
    RQST = requests.get(str(api_url))
    RQST_DICT = RQST.json()
    RACETABLE = RQST_DICT['MRData']['RaceTable']
    season = RACETABLE['season']
    round_nr = RACETABLE['round']

    with open('pickles\\race_results\\RaceResult_f1_{}_round{}.pickle'.format(season, round_nr), "wb") as f:
        pickle.dump(RQST_DICT, f)

# for num in range(1,10):
#     make_race_result_pickle('http://ergast.com/api/f1/2017/{}/results.json'.format(num))
# http://ergast.com/api/f1/{}/{}/results.format(season, round_nr)

def make_qualy_result_pickle(api_url):
    RQST = requests.get(str(api_url))
    RQST_DICT = RQST.json()
    RACETABLE = RQST_DICT['MRData']['RaceTable']
    season = RACETABLE['season']
    round_nr = RACETABLE['round']

    with open('pickles\\qualifying_results\\QualifyingResult_f1_{}_round{}.pickle'.format(season, round_nr), "wb") as f:
        pickle.dump(RQST_DICT, f)
