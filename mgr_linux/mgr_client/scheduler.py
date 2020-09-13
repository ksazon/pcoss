import asyncio
import sched
import time
from typing import Dict

import networkx as nx
import numpy as np
import pandas as pd

import algorithms as a
import constants as c
import helpers as h
import operations as o

import aiohttp


class Scheduler:
    def __init__(self, table: pd.DataFrame):
        self.table: pd.DataFrame = table
        self._table: pd.DataFrame = table.to_numpy()
        self.row_grouping_func = h.id_func
        self.cloumn_grouping_func = h.id_func
        self.operations: Dict = {}
        self.column_operation_dict: Dict = {}
        self.conflict_graph: nx.Graph = None
        self.complexity_table: pd.DataFrame = None
        self.processing_times: pd.DataFrame = None
        self._processing_times: pd.DataFrame = None
        self.algorithm = None
        self.objective = c.DEFAULT_OBJECTIVE
        self._schedule = []
        self._scheduler = sched.scheduler(time.time, time.sleep)
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
            self._processing_times = self.processing_times.to_numpy() / 10
            return
        
        # todo
        if self.complexity_table:
            self._processing_times = self._table * self.complexity_table
            return
        
        self._processing_times = self._assses_aproximate_execution_times()


    def _assses_aproximate_execution_times(self):
        # todo
        return np.ones(self._table.shape)


    def _prepare_data(self):
        self._group_rows()
        self._group_columns()
        self._fill_times()
        self._find_best_algorithm()
    

    def _prepare_schedule(self):
        t1 = time.monotonic()
        self._schedule = (
            a.ALGORITHM_CLASS_DICT[self.algorithm]
            (self._processing_times, self.conflict_graph)
            .run()
        )
        t2 = time.monotonic()
        print(t2-t1)

        # for (t, (row, col)) in self._schedule:
        #     self._scheduler.enter(t, 0, self.operations[col],
        #         argument=(self._table[row][col],))

    def prepare(self):
        self._prepare_data()
        self._prepare_schedule()
        
    async def run(self):
        await asyncio.gather(*[
            o.operation(
                endpoint=self.column_operation_dict[col],
                item=self._table[row][col],
                sched_time=t,
                operation_duration=int(self._processing_times[row][col]),
                session=self._session
                )
            for (t, (row, col)) in self._schedule])
        
        try:
            await self._session.close()
        except Exception as e:
            pass

    def gantt_chart(self):
        import plotly.express as px
        import pandas as pd

        df = pd.DataFrame([
            dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28', Resource="Alex"),
            dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15', Resource="Alex"),
            dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30', Resource="Max")
        ])

        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Resource", color="Resource")
        fig.show()