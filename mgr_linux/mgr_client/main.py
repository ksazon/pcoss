import asyncio
from typing import List, Set, Tuple

import pandas as pd

import algorithms as a
import constants as c
import helpers as h
import operations as o
import scheduler as s
import create_problem_input as cpi


async def main():
    pi = cpi.ProblemInput()

    sc = s.Scheduler(pi.table_in)
    sc.column_operation_dict = pi.column_operation_dict
    sc.conflict_graph = pi.conflict_graph_in
    sc.processing_times = pi.table_in
    sc.prepare()
    
    await sc.run()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
