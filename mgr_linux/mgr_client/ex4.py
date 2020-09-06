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
    rank_matrix = np.full(t_table.shape, np.nan)

    def solve_conflicts(rm: np.ndarray, changed_rows: Set[int], changed_cols: Set[int]):
        new_changed_rows = set()
        new_changed_cols = set()

        for cr in changed_rows:
            for cc in changed_cols:
                for cv in np.where(rm[cr,:] == rm[cr,cc]):
                    if cv[0] == cc:
                        continue
                    new_changed_rows.add(cr)
                    new_changed_cols.add(cc)
                    rm[cv] += 1
        
        if new_changed_rows:
            return solve_conflicts(rm, new_changed_rows, new_changed_cols)
        
        return rm

    def conflicts(row, col):
        if col == 2 and not np.isnan(rank_matrix[row,3]): return [(row,3),]
        if col == 3 and not np.isnan(rank_matrix[row,2]): return [(row,2),]
        return []

    def insertion_order():
        # TODO better function
        return np.random.permutation(list(np.ndindex(t_table.shape)))

    def beam_search(rm: Set[np.ndarray]):
        # TODO better function
        return random.sample(rm, min(len(rm), 2))

    for row, col in insertion_order():
        potential_rank = set()
        potential_rank_matrices = []

        potential_rank.add(1)
        for e in np.argwhere(~np.isnan(rank_matrix[:,col])):
            potential_rank.add(rank_matrix[e,col]+1)
        for cell in conflicts(row, col):
            potential_rank.add(rank_matrix[cell]+1)

        for pr in potential_rank:
            prm = rank_matrix.copy()
            prm[row, col] = pr
            prm = solve_conflicts(prm, {row,}, {col,})
            potential_rank_matrices.append(prm)
        
        potential_rank_matrices_truncated = beam_search(potential_rank_matrices)
        


class Scheduler:
    _default_algorithm = 'random'
    _default_objective = 'cmax'

    _algorithm_dict = {
        'random': alg_random,
    }


    def __init__(self, table):
        self.table = table
        self._table = table
        self.row_grouping_func = id_func
        self.cloumn_grouping_func = id_func
        self.operations = []
        self.conflict_graph = []
        self.complexity_table = []
        self.times_table = []
        self._times_table = []
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
        if self.times_table:
            self._times_table = self.times_table
        
        # todo
        if self.complexity_table:
            self._times_table = self._table * self.complexity_table
        
        self._times_table = self._assses_aproximate_execution_times()


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

    alg_insertion_beam(table_in, conflits=table_in)
