import time
import numpy as np
import sched
import random
import requests
import urllib3
import pandas as pd
import networkx
from typing import List, Tuple

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def id_func(x):
    return x     


def alg_random(table):
    return [
        (random.random() * 5, (r_idx, c_idx))
        for (r_idx, r) in enumerate(table)
        for (c_idx, c) in enumerate(r)
        ]


# def alg_insertion_beam(table: pd.DataFrame, conflits: pd.DataFrame):
#     t_table = table.T
#     conflits_arr = conflits.to_numpy()
#     rank_matrix = np.full(table.shape, np.nan)
#     sheduled_operations = []

#     for row_idx, r in t_table.iterrows():
#         for col_idx, cell in r.iteritems():
#             if np.isnan(np.nanmax(rank_matrix[:,col_idx])):
#                 rank_matrix[row_idx, col_idx] = 1
#             else:
#                 rank_matrix[row_idx, col_idx] = np.nanmax(rank_matrix[:col_idx]) + 1
#             if not np.isnan(np.nanmax(rank_matrix[row_idx:])) and conflits_arr[np.argmax(rank_matrix[row_idx:])]:
#                 rank_matrix[row_idx, col_idx] = np.nanmax(rank_matrix[row_idx,:]) + 1

#     print('x')
#     return rank_matrix


def alg_insertion_beam(table: pd.DataFrame, conflits: pd.DataFrame):
    t_table = table.to_numpy()
    t_conflits = conflits.to_numpy()
    rank_matrix = np.full(t_table.shape, np.nan)

    for row, col in np.ndindex(t_table.shape):
        if np.isnan(np.nanmax(rank_matrix[:,col])):
            rank_matrix[row, col] = 1
        else:
            rank_matrix[row, col] = np.nanmax(rank_matrix[:,col]) + 1
        if not np.isnan(np.nanmax(rank_matrix[row,:])) and t_conflits[row, np.argmax(rank_matrix[row,:])] == 1:
            rank_matrix[row, col] = np.nanmax(rank_matrix[row,:]) + 1

    print('x')
    return rank_matrix


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
