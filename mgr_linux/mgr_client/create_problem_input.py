import pandas as pd

import constants as c
import helpers as h


class Cfg:
    def __init__(self, filepath: str):
        self.index_cols = ['id',]
        self.grouping_cols = ['gr1',]
        self.conflicting_machines = {
            (1, 2),
            (5, 8),
            (16, 19),
            }
        self.beam_width = 5


class ProblemInput:
    def __init__(self):
        cfg = Cfg('a')

        self.table_in = pd.read_csv(
            '../data/data2.csv',
            index_col=cfg.index_cols,
            nrows=5,
            usecols=lambda col: col not in cfg.grouping_cols)

        self.column_operation_dict = {}
        avaliable_operations_list = ['A', 'B', 'C',]

        use_operation_num = 0

        for cm in cfg.conflicting_machines:
            self.column_operation_dict[cm[0]] = avaliable_operations_list[use_operation_num]
            self.column_operation_dict[cm[1]] = avaliable_operations_list[use_operation_num]
            use_operation_num += 1

        for col_num in range(len(self.table_in.columns)):
            if col_num not in [cm for te in cfg.conflicting_machines for cm in te]:
                self.column_operation_dict[col_num] = '0'

        job_cnt, machine_cnt = self.table_in.shape

        self.conflict_graph_in = (
            h.create_conflict_graph_from_cnts_and_conflicting_machine_list(
                job_cnt=job_cnt,
                machine_cnt=machine_cnt,
                conflicting_machines=cfg.conflicting_machines,
                show=c.SHOW_CONFLICT_GRAPH))

        self.processing_times = (self.table_in * 100) + 200
