import asyncio
import time
from typing import List, Set, Tuple

import constants as c
import create_problem_input as cpi
import helpers as h
# import operations as o
import output
import scheduler as s
import pandas as pd

import glob


async def main():
    problem_files = glob.glob(r'../data/auto/*.toml')
    times = []

    for pf in problem_files:
        print(pf)
        pi = cpi.ProblemInput.from_toml(pf)

        sc = s.Scheduler(pi.table_in)
        sc.column_operation_dict = pi.column_operation_dict
        sc.conflict_graph = pi.conflict_graph_in
        sc.processing_times = pi.processing_times
        
        ts = time.perf_counter()
        sc.prepare()
        te = time.perf_counter()

        times.append((pf, te-ts, max([e.end_time for e in sc.schedule])))
    
    pd.DataFrame(times).to_csv('testing_times.csv')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
