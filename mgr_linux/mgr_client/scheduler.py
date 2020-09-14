import asyncio
# import sched
import time
from dataclasses import asdict
from typing import Dict, List, Tuple

import aiohttp
import networkx as nx
import numpy as np
import pandas as pd

import algorithms as a
import constants as c
import helpers as h
import operations as o
from create_problem_input import ProblemInput


class Scheduler:
    def __init__(self, table: pd.DataFrame):
        self.table: pd.DataFrame = table
        self._table: pd.DataFrame = table.to_numpy()
        self.row_grouping_func = h.id_func
        self.cloumn_grouping_func = h.id_func
        # self.operations: Dict = {}
        self.column_operation_dict: Dict = {}
        self.conflict_graph: nx.Graph = None
        self._conflict_graph: nx.Graph = None
        self.complexity_table: pd.DataFrame = None
        self.processing_times: pd.DataFrame = None
        self._processing_times: pd.DataFrame = None
        self.algorithm = None
        self.objective = c.DEFAULT_OBJECTIVE
        self.schedule: List[h.scheduled_operation] = []
        # self._scheduler = sched.scheduler(time.time, time.sleep)
        self._session = aiohttp.ClientSession()

    def _find_best_algorithm(self):
        if self.algorithm:
            return
        
        self.algorithm = c.DEFAULT_ALGORITHM

    def _group_rows(self):
        self._table = self.row_grouping_func(self._table)

    def _group_columns(self):
        self._table = self.cloumn_grouping_func(self._table)

    def _fill_times(self):
        if not self.processing_times.empty:
            self._processing_times = self.processing_times.to_numpy()
            return
        
        # todo
        if self.complexity_table:
            self._processing_times = self._table * self.complexity_table
            return
        
        self._processing_times = self._assses_aproximate_execution_times()

    def _assses_aproximate_execution_times(self):
        # todo
        return np.ones(self._table.shape)

    @h.get_func_exec_time_decorator
    def _prepare_data(self):
        self._group_rows()
        self._group_columns()
        self._fill_times()
        self._find_best_algorithm()
    
    @h.get_func_exec_time_decorator
    def _prepare_schedule(self):
        self.schedule = (
            a.ALGORITHM_CLASS_DICT[self.algorithm]
            (self._processing_times, self.conflict_graph)
            .run()
        )

    def prepare(self):
        self._prepare_data()
        self._prepare_schedule()

    async def run(self):
        t0 = time.perf_counter()

        al = []
        for so in self.schedule:
            so.endpoint = '0'  # self.column_operation_dict[so.machine]
            so.item = self._table[so.job][so.machine]
            
            al.append(o.operation(so, self._session, t0))
        t1 = time.perf_counter()
        await asyncio.gather(*al)
        t2 = time.perf_counter()
        try:
            await self._session.close()
        except Exception as e:
            pass
        t3 = time.perf_counter()
        if c.PRINT_DEBUG_MESSSAGES:
            print(f't1-t0: {t1-t0}\tt2-t1: {t2-t1}\tt3-t2: {t3-t2}\tt3-t0: {t3-t0}')

    @classmethod
    def from_toml(cls, toml_file):
        config_dict = ProblemInput.from_toml(toml_file)
