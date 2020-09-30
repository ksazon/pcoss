import asyncio
import time
from typing import List, Set, Tuple

import pcoss_scheduler_pkg.constants as c
import pcoss_scheduler_pkg.problem_input as cpi
import pcoss_scheduler_pkg.helpers as h
import pcoss_scheduler_pkg.output
import pcoss_scheduler_pkg.scheduler as s
import pandas as pd

import glob


async def main():
    problem_files = glob.glob(r'../../data/auto/*j4m0.toml')
    times = []

    for pf in problem_files:
        print(pf)
        pi = cpi.ProblemInput.from_toml(pf)

        sc = s.Scheduler.from_ProblemInput(pi)
        
        ts = time.perf_counter()
        sc.prepare()
        te = time.perf_counter()

        times.append((pf, te-ts, max([e.end_time for e in sc.schedule])))
    
    pd.DataFrame(times).to_csv('testing_times.csv')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
