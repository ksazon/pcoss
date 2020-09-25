import pandas as pd

import constants as c
import helpers as h

from typing import List, Set, Tuple, Dict
import toml


# class Cfg:
#     def __init__(self, filepath: str):
#         self.index_cols = ['id']
#         self.grouping_cols = ['gr1']
#         self.conflicting_machines = {
#             (1, 2),
#             (5, 8),
#             (16, 19),
#             }
#         self.beam_width = 5


class ProblemInput:
    def __init__(self, init_dict: Dict):
        # cfg = Cfg('a')

        self.table_in = pd.read_csv(
            init_dict['files']['data'],
            index_col=init_dict['problem_data']['index_cols'],
            # TODO remove
            # nrows=5,
            # TODO remove
            usecols=lambda col: col not in init_dict['problem_data']['grouping_cols'],
            )

        '''
        TODO remove -start
        '''
        self.column_operation_dict = {}
        avaliable_operations_list = ['A', 'B', 'C']

        use_operation_num = 0

        for cm in init_dict['problem_data']['conflicting_machines']:
            self.column_operation_dict[cm[0]] = avaliable_operations_list[use_operation_num]
            self.column_operation_dict[cm[1]] = avaliable_operations_list[use_operation_num]
            use_operation_num = (use_operation_num + 1) % 3

        for col_num in range(len(self.table_in.columns)):
            if col_num not in [cm for te in init_dict['problem_data']['conflicting_machines'] for cm in te]:
                self.column_operation_dict[col_num] = '0'
        '''
        TODO remove -end
        '''

        job_cnt, machine_cnt = self.table_in.shape

        self.conflict_graph_in = (
            h.create_conflict_graph_from_cnts_and_conflicting_machine_list(
                job_cnt=job_cnt,
                machine_cnt=machine_cnt,
                conflicting_machines=init_dict['problem_data']['conflicting_machines'],
                show=c.SHOW_CONFLICT_GRAPH))

        self.processing_times = pd.read_csv(
            init_dict['files']['processing_times'],
            index_col=init_dict['problem_data']['index_cols'],
            # TODO remove
            # nrows=5,
            # TODO remove
            usecols=lambda col: col not in init_dict['problem_data']['grouping_cols'],
            ) * 100 + 1000
        
        self.conflicting_machines_list = init_dict['problem_data']['conflicting_machines']
        
        # (self.table_in * 100) + 1000




    
    # def __init__(self):
    #     cfg = Cfg('a')

    #     self.table_in = pd.read_csv(
    #         '../data/data2.csv',
    #         index_col=cfg.index_cols,
    #         nrows=5,
    #         usecols=lambda col: col not in cfg.grouping_cols)

    #     self.column_operation_dict = {}
    #     avaliable_operations_list = ['A', 'B', 'C']

    #     use_operation_num = 0

    #     for cm in cfg.conflicting_machines:
    #         self.column_operation_dict[cm[0]] = avaliable_operations_list[use_operation_num]
    #         self.column_operation_dict[cm[1]] = avaliable_operations_list[use_operation_num]
    #         use_operation_num += 1

    #     for col_num in range(len(self.table_in.columns)):
    #         if col_num not in [cm for te in cfg.conflicting_machines for cm in te]:
    #             self.column_operation_dict[col_num] = '0'

    #     job_cnt, machine_cnt = self.table_in.shape

    #     self.conflict_graph_in = (
    #         h.create_conflict_graph_from_cnts_and_conflicting_machine_list(
    #             job_cnt=job_cnt,
    #             machine_cnt=machine_cnt,
    #             conflicting_machines=cfg.conflicting_machines,
    #             show=c.SHOW_CONFLICT_GRAPH))

    #     self.processing_times = (self.table_in * 100) + 1000

    #             self.table_in = pd.read_csv(
    #         '../data/data2.csv',
    #         index_col=cfg.index_cols,
    #         nrows=5,
    #         usecols=lambda col: col not in cfg.grouping_cols)

    #     self.column_operation_dict = {}
    #     avaliable_operations_list = ['A', 'B', 'C']

    #     use_operation_num = 0

    #     for cm in cfg.conflicting_machines:
    #         self.column_operation_dict[cm[0]] = avaliable_operations_list[use_operation_num]
    #         self.column_operation_dict[cm[1]] = avaliable_operations_list[use_operation_num]
    #         use_operation_num += 1

    #     for col_num in range(len(self.table_in.columns)):
    #         if col_num not in [cm for te in cfg.conflicting_machines for cm in te]:
    #             self.column_operation_dict[col_num] = '0'

    #     job_cnt, machine_cnt = self.table_in.shape

    #     self.conflict_graph_in = (
    #         h.create_conflict_graph_from_cnts_and_conflicting_machine_list(
    #             job_cnt=job_cnt,
    #             machine_cnt=machine_cnt,
    #             conflicting_machines=cfg.conflicting_machines,
    #             show=c.SHOW_CONFLICT_GRAPH))


    @classmethod
    def from_toml(cls, toml_file: str):
        config_dict = toml.load(toml_file)
        
        config_dict['problem_data']['conflicting_machines'] = list(
            map(tuple, config_dict['problem_data']['conflicting_machines'])
            )
        
        return cls(config_dict)
