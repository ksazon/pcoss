import pandas as pd

import constants as c
import helpers as h


class ProblemInput:
    def __init__(self):
        cfg = h.Cfg('a')

        self.table_in = pd.read_csv(
            '../data/data2.csv',
            index_col=cfg.index_cols,
            nrows=20,
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
