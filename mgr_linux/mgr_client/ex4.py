import time
import sched
import random
import requests


requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)


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
    tl = [
        ('pol', range(5), range(10)),
        ('ger', range(10), range(5)),
        ('rus', range(20), range(20)),
        ('nor', range(50), range(50)),
        ('fin', range(100), range(5)),
        ('usa', range(5), range(20)),
        ('bel', range(10), range(0)),
        ]

    schedule = [
        (0,     (0, 2)),
        (0.5,   (0, 1)),
        (0.5,   (4, 1)),
        (1,     (3, 2)),
        (1,     (3, 0)),
        (0,     (0, 0))
    ]

    S = sched.scheduler(time.time, time.sleep)
    O = {0: operation_a, 1: operation_b, 2: operation_c}

    for (t, (r, c)) in schedule:
        S.enter(t, 0, O[c], argument=(tl[r][c],))

    S.run()


def id_func(x):
    return x     


class Scheduler:
    _default_algorithm = 'random'
    _default_objective = 'cmax'

    _algorithm_dict = {
        'random': _random,
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
        self.algorithm = self._default_algorithm
        self.objective = self._default_objective


    def _find_best_algorithm(self):
        if self.algorithm:
            return
        
        # todo
        self.algorithm = self._default_algorithm


    def _group_rows(self):
        self._table = self.row_grouping_func(self._table)


    def _group_columns(self):
        self._table = self.cloumn_grouping_func(self._table)


    def _assses_aproximate_execution_times(self):
        if self.times_table:
            return
        
        # todo
        if self.complexity_table:
            return
        

    def _random(self):
        return [(random.random() * 5, (r, c)) for r in self._table for c in r]


    def prepare_schedule(self):
        self._group_rows()
        self._group_columns()
        self._assses_aproximate_execution_times()
        self._find_best_algorithm()


    def run(self):
        return self._algorithm_dict[self.algorithm](self._table)

        
