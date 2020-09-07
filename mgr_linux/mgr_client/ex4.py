# import operator
import random
import sched
import time
from typing import List, Tuple, Set

import networkx as nx
import numpy as np
import pandas as pd
import urllib3
import requests

from bokeh.io import output_file, show
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool,)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx

from matplotlib import pyplot as plt


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def id_func(x):
    return x     


def alg_random(table):
    return [
        (random.random() * 5, (r_idx, c_idx))
        for (r_idx, r) in enumerate(table)
        for (c_idx, c) in enumerate(r)
        ]


def alg_insertion_beam(table: pd.DataFrame, conflits: pd.DataFrame):
    t_table = table.to_numpy()
    t_conflits = conflits.to_numpy()
    # rank_matrix = np.full(t_table.shape, np.nan)
    candidate_schedules = [np.full(t_table.shape, np.nan),]

    def solve_conflicts(rm: np.ndarray, changed_rows: Set[int], changed_cols: Set[int]):
        new_changed_rows = set()
        new_changed_cols = set()

        for cr in changed_rows:
            for cc in changed_cols:
                for cv in np.where(rm[:,cc] == rm[cr,cc])[0]:
                    if cv == cr:
                        continue
                    new_changed_rows.add(cr)
                    new_changed_cols.add(cc)
                    rm[cv] += 1
        
        if new_changed_rows:
            return solve_conflicts(rm, new_changed_rows, new_changed_cols)
        
        return rm

    def row_conflicts(rm: np.ndarray, row: int, col: int):
        if col == 2 and not np.isnan(rm[row,3]): return [(row,3),]
        if col == 3 and not np.isnan(rm[row,2]): return [(row,2),]
        return []

    def insertion_order():
        # TODO better function
        return np.random.permutation(list(np.ndindex(t_table.shape)))

    def beam_search(rm: Set[np.ndarray]):
        # TODO better function
        return random.sample(rm, min(len(rm), 5))

    for row, col in insertion_order():
        candidate_schedules_with_children = []
        for cs in candidate_schedules:
            potential_rank = set()
            # children = []

            potential_rank.add(1)
            for e in np.argwhere(~np.isnan(cs[:,col])):
                potential_rank.add(cs[(e,col)][0]+1)
            for cell in row_conflicts(cs, row, col):
                potential_rank.add(cs[cell]+1)

            for pr in potential_rank:
                cs_with_child = cs.copy()
                cs_with_child[row, col] = pr
                cs_with_child = solve_conflicts(cs_with_child, {row,}, {col,})
                candidate_schedules_with_children.append(cs_with_child)
        
        candidate_schedules = beam_search(candidate_schedules_with_children)
        


class Scheduler:
    _default_algorithm = 'random'
    _default_objective = 'cmax'

    _algorithm_dict = {
        'random': alg_random,
    }


    def __init__(self, table, processing_times=None, conflict_graph=None):
        self.table = table
        self._table = table
        self.row_grouping_func = id_func
        self.cloumn_grouping_func = id_func
        self.operations = []
        self.conflict_graph = conflict_graph
        self.complexity_table = []
        self.processing_times = processing_times
        self._processing_times = []
        self.algorithm = self._default_algorithm
        self.objective = self._default_objective
        self._schedule = []
        self._scheduler = sched.scheduler(time.time, time.sleep)


    def _find_best_algorithm(self):
        if self.algorithm:
            return
        
        # todo
        self.algorithm = self._default_algorithm


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
        self._schedule = self._algorithm_dict[self.algorithm](self._table)

        for (t, (r, c)) in self._schedule:
            self._scheduler.enter(t, 0, self.operations[c], argument=(self._table[r][c],))


    def prepare(self):
        self._prepare_data()
        self._prepare_schedule()
        

    def run(self):
        self._scheduler.run()


BASE_URL = r'https://localhost:44320/Operations'


def operation_a(x):
    ret = requests.get(f'{BASE_URL}/A/{x}/0', verify=False).content
    print('a', ret)
    return ret


def operation_b(x):
    ret = requests.get(f'{BASE_URL}/B/{len(x)}/0', verify=False).content
    print('b', ret)
    return ret


def operation_c(x):
    ret = requests.get(f'{BASE_URL}/C/{len(x)}/0', verify=False).content
    print('c', ret)
    return ret


if __name__ == '__main__':
    table_in = [
        ('pol', range(5), range(10)),
        ('ger', range(10), range(5)),
        ('rus', range(20), range(20)),
        ('nor', range(50), range(50)),
        ('fin', range(100), range(5)),
        ('usa', range(5), range(20)),
        ('bel', range(10), range(0)),
        ]
    
    index_cols = ['id',]
    grouping_cols = ['g1']
    table_in = pd.read_csv('../data/data.csv', index_col=index_cols, nrows=10, usecols=lambda c: c not in ['gr1',])

    O = {0: operation_a, 1: operation_b, 2: operation_c}

    # sc = Scheduler(table_in)
    # sc.operations = O
    # sc.prepare()
    # sc.run()

    # alg_insertion_beam(table_in, conflits=table_in)

    # conflict_graph = nx.from_numpy_array(np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]]))
    job_cnt, machines_cnt = table_in.shape
    conflicting_machines = [(1,2),]

    def create_conflict_graph(show=True) -> nx.Graph:
        G = nx.Graph()
        for job_idx in range(job_cnt):
            job_nodes = [(job_idx,machine_idx) for machine_idx in range(machine_cnt)]
            G.add_nodes_from(job_nodes)

            for cm1, cm2 in conflicting_machines:
                G.add_edge((job_idx,cm1), (job_idx,cm2))
            
            for prev_job_idx in range(job_idx):
                for machine_idx in range(machine_cnt):
                    G.add_edge((prev_job_idx,machine_idx), (job_idx,machine_idx))

        if show:
            plt.figure(figsize=(6,6))
            pos = {(x,y):(y+random()/3,-x+random()/3) for x,y in G.nodes()}
            nx.draw(G, with_labels=True, pos=pos, connectionstyle='arc3, rad=2')
            plt.show()

    conflict_graph_in = create_conflict_graph()
    # conflict_graph_in.re
    # conflict_graph.
    
    # # plot = Plot(plot_width=400, plot_height=400,
    # #         x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
            
    # plot = Plot(plot_width=400, plot_height=400)

    # plot.title.text = "Graph Interaction Demonstration"

    # # node_hover_tool = HoverTool(tooltips=[("index", "@index"), ("club", "@club")])
    # # plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

    # graph_renderer = from_networkx(conflict_graph, nx.spring_layout, scale=1, center=(0, 0))

    # graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
    # # graph_renderer.edge_renderer.glyph = MultiLine(line_color="edge_color", line_alpha=0.8, line_width=1)
    # plot.renderers.append(graph_renderer)

    # output_file("interactive_graphs.html")
    # show(plot)

    # plt.figure(figsize=(6,6))
    # pos = {(x,y):(y,-x) for x,y in conflict_graph_in.nodes()}
    # nx.draw(conflict_graph_in, with_labels=True, pos=pos)
    plt.show()
