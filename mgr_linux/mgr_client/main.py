# import random
# import sched
# import time
from typing import List, Set, Tuple

# import networkx as nx
# import numpy as np
import pandas as pd
# import requests
# import urllib3
# from matplotlib import pyplot as plt

import algorithms as a
import constants as c
import helpers as h
import operations as o
import scheduler as s


def main():
    cfg = h.Cfg('a')

    table_in = pd.read_csv(
        '../data/data2.csv',
        index_col=cfg.index_cols,
        nrows=60,
        usecols=lambda col: col not in cfg.grouping_cols)

    # operatation_dict = {
    #     0: o.operation_a,
    #     1: o.operation_b,
    #     2: o.operation_b,
    #     3: o.operation_c,
    #     }
    operatation_dict = {}
    avaliable_operations_list = [o.operation_a, o.operation_b, o.operation_c]
    use_operation_num = 0

    for cm in cfg.conflicting_machines:
        operatation_dict[cm[0]] = avaliable_operations_list[use_operation_num]
        operatation_dict[cm[1]] = avaliable_operations_list[use_operation_num]

    for c in range(len(table_in.columns)):
        if c not in [cm for te in cfg.conflicting_machines for cm in te]:
            operatation_dict[c] = o.operation_0


    job_cnt, machine_cnt = table_in.shape
    conflict_graph_in = (
        h.create_conflict_graph_from_cnts_and_conflicting_machine_list(
            job_cnt=job_cnt,
            machine_cnt=machine_cnt,
            conflicting_machines=cfg.conflicting_machines,
            show=True))

    sc = s.Scheduler(table_in)
    sc.operations = operatation_dict
    sc.conflict_graph = conflict_graph_in
    sc.prepare()
    # sc.run()


if __name__ == '__main__':
    main()
