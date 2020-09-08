# import operator
import random
import sched
import time
from typing import List, Set, Tuple

import networkx as nx
import numpy as np
import pandas as pd
import requests
import urllib3
from matplotlib import pyplot as plt

import algorithms as a
import constants as c
import helpers as h
import operations as o

# from bokeh.io import output_file, show
# from bokeh.models import (BoxZoomTool, Circle, HoverTool,
#                           MultiLine, Plot, Range1d, ResetTool,)
# from bokeh.palettes import Spectral4
# from bokeh.plotting import from_networkx        


class Scheduler:
    def __init__(self, table, processing_times=None, conflict_graph=None):
        self.table = table
        self._table = table
        self.row_grouping_func = h.id_func
        self.cloumn_grouping_func = h.id_func
        self.operations = []
        self.conflict_graph = conflict_graph
        self.complexity_table = []
        self.processing_times = processing_times
        self._processing_times = []
        self.algorithm = c.default_algorithm
        self.objective = c.default_objective
        self._schedule = []
        self._scheduler = sched.scheduler(time.time, time.sleep)


    def _find_best_algorithm(self):
        if self.algorithm:
            return
        
        # todo
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
        return np.ones((len(self._table), len(self._table[0]))) 


    def _prepare_data(self):
        self._group_rows()
        self._group_columns()
        self._fill_times()
        self._find_best_algorithm()
    

    def _prepare_schedule(self):
        self._schedule = c.ALGORITHM_DICT[self.algorithm](self._table)

        for (t, (r, c)) in self._schedule:
            self._scheduler.enter(t, 0, self.operations[c], argument=(self._table[r][c],))


    def prepare(self):
        self._prepare_data()
        self._prepare_schedule()
        

    def run(self):
        self._scheduler.run()



def main():
    cfg = h.Cfg('a')

    table_in = pd.read_csv(
        '../data/data.csv',
        index_col=cfg.index_cols,
        nrows=10,
        usecols=lambda c: c not in cfg.grouping_cols)

    # O = {0: o.operation_a, 1: o.operation_b, 2: o.operation_c}

    # sc = Scheduler(table_in)
    # sc.operations = O
    # sc.prepare()
    # sc.run()

    # alg_insertion_beam(table_in, conflits=table_in)

    job_cnt, machine_cnt = table_in.shape

    conflict_graph_in = h.create_conflict_graph_from_cnts_and_conflicting_machine_list(
        job_cnt=job_cnt,
        machine_cnt=machine_cnt,
        conflicting_machines=cfg.conflicting_machines)

    a.alg_insertion_beam(table_in, conflict_graph=conflict_graph_in)

if __name__ == '__main__':
    main()
