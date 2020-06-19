import time
import numpy as np
import sched
import random
import requests


requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)


def id_func(x):
    return x     


def alg_random(table):
    return [
        (random.random() * 5, (r_idx, c_idx))
        for (r_idx, r) in enumerate(table)
        for (c_idx, c) in enumerate(r)
        ]


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
    table = [
        ('pol', range(5), range(10)),
        ('ger', range(10), range(5)),
        ('rus', range(20), range(20)),
        ('nor', range(50), range(50)),
        ('fin', range(100), range(5)),
        ('usa', range(5), range(20)),
        ('bel', range(10), range(0)),
        ]

    O = {0: operation_a, 1: operation_b, 2: operation_c}

    sc = Scheduler(table)
    sc.operations = O
    sc.prepare()
    sc.run()
