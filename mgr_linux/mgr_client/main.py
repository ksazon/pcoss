import asyncio
import time
from typing import List, Set, Tuple

import pandas as pd

import algorithms as a
import constants as c
import create_problem_input as cpi
import helpers as h
import operations as o
import scheduler as s


async def main():
    pi = cpi.ProblemInput()

    sc = s.Scheduler(pi.table_in)
    sc.column_operation_dict = pi.column_operation_dict
    sc.conflict_graph = pi.conflict_graph_in
    sc.processing_times = pi.processing_times
    sc.prepare()
    
    ts = time.perf_counter()
    await sc.run()
    te = time.perf_counter()

    if c.PRINT_TIMES:
        print(f'Function "run" execution time: {te-ts:.3f}s')

    if c.SHOW_RESULT_SCHEDULE_GRAPH:
        h.plot_schedule_graph(sc.outcome_graph)

    if c.SHOW_GANTT:
        h.plot_gantt_chart(sc.schedule)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
