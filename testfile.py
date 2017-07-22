import platform
from pathlib import Path
print(platform.python_version())
import datetime

print(Path('pickles/race_results/RaceResult_f1_{}_round{}.pickle'))

print(str(datetime.timedelta(milliseconds=7169133)))
