import random
from typing import Dict, List, Set, Tuple

import networkx as nx
import numpy as np
import pandas as pd

import constants as c


class ScheduleAlgorithmBase:
    def __init__(self, processing_times: pd.DataFrame,
            conflict_graph: nx.Graph):

        self.pt = processing_times.to_numpy()
        self.conflict_graph = conflict_graph
        self.candidate_schedules = [np.full(self.pt.shape, np.nan),]

    def run(self):
        raise NotImplementedError


class Randomized(ScheduleAlgorithmBase):
    def run(self):
        return [
            (random.random() * 5, (r_idx, c_idx))
            for (r_idx, r) in enumerate(self.pt)
            for (c_idx, c) in enumerate(self.pt)
            ]


class InsertionBeam(ScheduleAlgorithmBase):
    def insertion_order(self):
        first_order = []
        h = min(self.pt.shape)
        pt_i = self.pt[:h,:].copy()
        i = 0

        for i in range(h):
            ma = np.argmax(pt_i[i,:])
            first_order += [(ma,i)]
            pt_i = np.delete(pt_i, ma, axis=1)
        
        other_order = [(x[0], x[1]) for x in filter(
            lambda e: (e[0], e[1]) not in first_order,
            np.transpose(np.unravel_index(
                np.argsort(self.pt,axis=None)[::-1],
                    shape=self.pt.shape)))]

        return first_order + other_order
        # return np.random.permutation(list(np.ndindex(self.pt.shape)))

    
    def solve_conflicting_ranks(self, rm: np.ndarray, changed_rows: Set[int],
            changed_cols: Set[int]
            ) -> np.ndarray:

        new_changed_rows = set()
        new_changed_cols = set()

        for cr in changed_rows:
            for cc in changed_cols:
                cv = rm[cr,cc]

                # for same_rank_cell_r in np.where(rm[:,cc] == cv)[0]:
                #     if same_rank_cell_r == cr:
                #         continue
                #     new_changed_rows.add(cr)
                #     new_changed_cols.add(cc)
                #     rm[cr, cc] += 1
                
                for n in filter(lambda n: rm[n] == cv, self.conflict_graph[(cr, cc)]):
                    new_changed_rows.add(n[0])
                    new_changed_cols.add(n[1])
                    rm[n] += 1
        
        if new_changed_rows:
            return self.solve_conflicting_ranks(
                rm,
                new_changed_rows,
                new_changed_cols)
        
        return rm

    def row_conflicts(self, rm: np.ndarray, row: int, col: int
            ) -> List[Tuple[int, int]]:
        
        # TODO rewrite
        if col == 2 and not np.isnan(rm[row,3]):
            return [(row,3),]
        if col == 3 and not np.isnan(rm[row,2]):
            return [(row,2),]
        
        return []

    def path_rec(self, rm: np.ndarray, e: Tuple[int, int], asc: bool
            ) -> List[Tuple[int, int]]:
        
        step = 1 if asc else -1
        next_val = rm[e]+step
        next_e = next(filter(lambda n: rm[n] == next_val, self.conflict_graph[e]), None) 

        if next_e:
            return [next_e] + self.path_rec(rm, next_e, asc)

        return []

    def _path_rec(self, rm: np.ndarray, e: Tuple[int, int], asc: bool
            ) -> List[Tuple[int, int]]:
        
        cg = self.conflict_graph
        step = 1 if asc else -1
        l = []
        n = e

        while n:
            next_val = rm[n]+step
            n = next(filter(lambda nn: rm[nn] == next_val, cg[n]), None)

            if n:
                l += [n]
        
        return l

    def get_path(self, rm: np.ndarray, added_element_idx: Tuple[int, int]
            ) -> List[Tuple[int, int]]:
        
        pr = self.path_rec

        return (
            pr(rm, added_element_idx, False)
            + [added_element_idx]
            + pr(rm, added_element_idx, True)
        )

    def beam_search(self, rm_list: List[np.ndarray],
            added_element_idx: Tuple[int, int]) -> List[np.ndarray]:

        rm_costs = {}

        for rm_idx, rm_cur in enumerate(rm_list):
            jobs, machines = np.transpose(
                self.get_path(rm_cur, added_element_idx))
            cost = sum(self.pt[jobs, machines])
            rm_costs[rm_idx] = cost

        return ([rm_list[k] for k, v in
            sorted(rm_costs.items(), key=lambda e: e[1])]
            [:c.DEFAULT_BEAM_WIDTH]
            )


    def schedule_as_list_of_tuples(self, rm: np.ndarray
            ) -> List[Tuple[float, Tuple[int, int]]]:
        scheduled_operations = []
        cur_rank = 1
        st = 0
        
        while len(scheduled_operations) < rm.size:
            idxs = np.nonzero(rm==cur_rank)
            for idx in np.transpose(idxs):
                scheduled_operations.append((st, idx))

            st += max(self.pt[idxs])
            cur_rank += 1
        
        return scheduled_operations

    def run(self) -> List[Tuple[float, Tuple[int, int]]]:
        for job, machine in self.insertion_order():
            candidate_schedules_with_children = []
            for cs in self.candidate_schedules:
                potential_rank = set()

                potential_rank.add(1)
                for e in np.argwhere(~np.isnan(cs[:,machine])):
                    potential_rank.add(cs[(e,machine)][0]+1)
                for cell in self.row_conflicts(cs, job, machine):
                    potential_rank.add(cs[cell]+1)

                for pr in potential_rank:
                    cs_with_child = cs.copy()
                    cs_with_child[job, machine] = pr
                    cs_with_child = self.solve_conflicting_ranks(
                        cs_with_child, {job,}, {machine,})
                    candidate_schedules_with_children.append(cs_with_child)
            
            self.candidate_schedules = self.beam_search(
                candidate_schedules_with_children, (job, machine))
        
        return self.schedule_as_list_of_tuples(self.candidate_schedules[0])


ALGORITHM_CLASS_DICT = {
    'randomized': Randomized,
    'insertion_beam': InsertionBeam,
}
