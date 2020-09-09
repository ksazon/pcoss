import sched
import time
from typing import Dict

import networkx as nx
import numpy as np
import pandas as pd

import algorithms as a
import constants as c
import helpers as h


class Scheduler:
    def __init__(self, table: pd.DataFrame):
        self.table: pd.DataFrame = table
        self._table: pd.DataFrame = table.to_numpy()
        self.row_grouping_func = h.id_func
        self.cloumn_grouping_func = h.id_func
        self.operations: Dict = {}
        self.conflict_graph: nx.Graph = None
        self.complexity_table: pd.DataFrame = None
        self.processing_times: pd.DataFrame = None
        self._processing_times: pd.DataFrame = None
        self.algorithm = None
        self.objective = c.DEFAULT_OBJECTIVE
        self._schedule = []
        self._scheduler = sched.scheduler(time.time, time.sleep)


    def _find_best_algorithm(self):
        if self.algorithm:
            return
        
        self.algorithm = c.DEFAULT_ALGORITHM


    def _group_rows(self):
        self._table = self.row_grouping_func(self._table)


    def _group_columns(self):
        self._table = self.cloumn_grouping_func(self._table)


    def _fill_times(self):
        if self.processing_times:
            self._processing_times = self.processing_times
        
        # todo
        if self.complexity_table:
            self._processing_times = self._table * self.complexity_table
        
        self._processing_times = self._assses_aproximate_execution_times()


    def _assses_aproximate_execution_times(self):
        # todo
        return pd.DataFrame(
            np.ones(self._table.shape))


    def _prepare_data(self):
        self._group_rows()
        self._group_columns()
        self._fill_times()
        self._find_best_algorithm()
    

    def _prepare_schedule(self):
        self._schedule = (
            a.ALGORITHM_CLASS_DICT[self.algorithm]
            (self._processing_times, self.conflict_graph)
            .run()
        )

        for (t, (row, col)) in self._schedule:
            self._scheduler.enter(t, 0, self.operations[col],
                argument=(self._table[row][col],))


    def prepare(self):
        self._prepare_data()
        self._prepare_schedule()
        

    def run(self):
        self._scheduler.run()
