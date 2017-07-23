import platform
from pathlib import Path
print(platform.python_version())
import datetime

print(Path('pickles/race_results/RaceResult_f1_{}_round{}.pickle'))

print(str(datetime.timedelta(milliseconds=7169133)))
print('=========')
time_format= '%M:%S.%f'
alonso = datetime.datetime.strptime('1:25.504', time_format)
pole = datetime.datetime.strptime('1:26.202', time_format)

delta = alonso - pole
print(delta.total_seconds())
