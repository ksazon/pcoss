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


# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# def id_func(x):
#     return x     


# def alg_random(table):
#     return [
#         (random.random() * 5, (r_idx, c_idx))
#         for (r_idx, r) in enumerate(table)
#         for (c_idx, c) in enumerate(r)
#         ]


# def alg_insertion_beam(processing_times: pd.DataFrame, conflict_graph: nx.Graph):
#     pt = processing_times.to_numpy()
#     candidate_schedules = [np.full(pt.shape, np.nan),]

#     def solve_conflicts(rm: np.ndarray, changed_rows: Set[int], changed_cols: Set[int]):
#         new_changed_rows = set()
#         new_changed_cols = set()

#         for cr in changed_rows:
#             for cc in changed_cols:
#                 for cv in np.where(rm[:,cc] == rm[cr,cc])[0]:
#                     if cv == cr:
#                         continue
#                     new_changed_rows.add(cr)
#                     new_changed_cols.add(cc)
#                     rm[cv] += 1
        
#         if new_changed_rows:
#             return solve_conflicts(rm, new_changed_rows, new_changed_cols)
        
#         return rm

#     def row_conflicts(rm: np.ndarray, row: int, col: int):
#         if col == 2 and not np.isnan(rm[row,3]): return [(row,3),]
#         if col == 3 and not np.isnan(rm[row,2]): return [(row,2),]
#         return []

#     def insertion_order():
#         # TODO better function
#         return np.random.permutation(list(np.ndindex(pt.shape)))

#     def beam_search(rm: Set[np.ndarray]):
#         # TODO better function
#         return random.sample(rm, min(len(rm), 5))

#     for row, col in insertion_order():
#         candidate_schedules_with_children = []
#         for cs in candidate_schedules:
#             potential_rank = set()
#             # children = []

#             potential_rank.add(1)
#             for e in np.argwhere(~np.isnan(cs[:,col])):
#                 potential_rank.add(cs[(e,col)][0]+1)
#             for cell in row_conflicts(cs, row, col):
#                 potential_rank.add(cs[cell]+1)

#             for pr in potential_rank:
#                 cs_with_child = cs.copy()
#                 cs_with_child[row, col] = pr
#                 cs_with_child = solve_conflicts(cs_with_child, {row,}, {col,})
#                 candidate_schedules_with_children.append(cs_with_child)
        
#         candidate_schedules = beam_search(candidate_schedules_with_children)
        


class Scheduler:
    # _default_algorithm = 'random'
    # _default_objective = 'cmax'

    # _algorithm_dict = {
    #     'random': alg_random,
    # }


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



# def create_conflict_graph_from_machine_list(show=True) -> nx.Graph:
#     G = nx.Graph()
#     for job_idx in range(job_cnt):
#         job_nodes = [(job_idx,machine_idx) for machine_idx in range(machine_cnt)]
#         G.add_nodes_from(job_nodes)

#         for cm1, cm2 in conflicting_machines:
#             G.add_edge((job_idx,cm1), (job_idx,cm2))
        
#         for prev_job_idx in range(job_idx):
#             for machine_idx in range(machine_cnt):
#                 G.add_edge((prev_job_idx,machine_idx), (job_idx,machine_idx))

#     if show:
#         plt.figure(figsize=(6,6))
#         pos = {(x,y):(y+random.random()/3,-x+random.random()/3)
#             for x,y in G.nodes()}
        
#         nx.draw(G, with_labels=True, pos=pos, connectionstyle='arc3, rad=2')
#         plt.show()
    
#     return G


def main():
    index_cols = ['id',]
    grouping_cols = ['gr1',]
    table_in = pd.read_csv(
        '../data/data.csv',
        index_col=index_cols,
        nrows=10,
        usecols=lambda c: c not in grouping_cols)

    O = {0: o.operation_a, 1: o.operation_b, 2: o.operation_c}

    # sc = Scheduler(table_in)
    # sc.operations = O
    # sc.prepare()
    # sc.run()

    # alg_insertion_beam(table_in, conflits=table_in)

    job_cnt, machine_cnt = table_in.shape
    conflicting_machines = {(1,2),}

    conflict_graph_in = h.create_conflict_graph_from_cnts_and_conflicting_machine_list(
        job_cnt=job_cnt,
        machine_cnt=machine_cnt,
        conflicting_machines=conflicting_machines)

    alg_insertion_beam(table_in, conflits=conflict_graph_in)

if __name__ == '__main__':
    main()
