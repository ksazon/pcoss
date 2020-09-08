import random
import pandas as pd
import networkx as nx
import numpy as np
from typing import Set, Tuple, List, Dict
import constants as c

algorithm_dict = {
    'random': alg_random,
}


def alg_random(table):
    return [
        (random.random() * 5, (r_idx, c_idx))
        for (r_idx, r) in enumerate(table)
        for (c_idx, c) in enumerate(r)
        ]


def alg_insertion_beam(processing_times: pd.DataFrame, conflict_graph: nx.Graph):
    pt = processing_times.to_numpy()
    candidate_schedules = [np.full(pt.shape, np.nan),]

    def solve_conflicting_ranks(rm: np.ndarray, changed_rows: Set[int], changed_cols: Set[int]):
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
                
                for n in conflict_graph.neighbors((cr, cc)):
                    if rm[n] == cv:
                        new_changed_rows.add(n[0])
                        new_changed_cols.add(n[1])
                        rm[n] += 1
        
        if new_changed_rows:
            return solve_conflicting_ranks(rm, new_changed_rows, new_changed_cols)
        
        return rm

    def row_conflicts(rm: np.ndarray, row: int, col: int):
        if col == 2 and not np.isnan(rm[row,3]): return [(row,3),]
        if col == 3 and not np.isnan(rm[row,2]): return [(row,2),]
        return []

    def insertion_order():
        # TODO better function
        return np.random.permutation(list(np.ndindex(pt.shape)))

    def beam_search(rm_list: List[np.ndarray], added_element_idx: Tuple[int, int]) -> List[np.ndarray]:
        def get_path(rm: np.ndarray) -> List[Tuple[int, int]]:
            def path_rec(e, asc):
                step = 1 if asc else -1
                next_e = list(filter(lambda x: rm[x] == rm[e]+step, conflict_graph.neighbors(e)))
                
                if next_e:
                    return [next_e[0]] + path_rec(next_e[0], asc)
                return []

            return (
                path_rec(added_element_idx, False)
                + [added_element_idx]
                + path_rec(added_element_idx, True)
            )
        
        rm_costs = {}
        for rm_idx, rm_cur in enumerate(rm_list):
            path_t = np.transpose(get_path(rm_cur))
            cost = sum(processing_times.to_numpy()[path_t[0], path_t[1]])
            rm_costs[rm_idx] = cost

        return ([rm_list[k] for k, v in
            sorted(rm_costs.items(), key=lambda e: e[1])]
            [:c.DEFAULT_BEAM_WIDTH])

        # return random.sample(rm_list, min(len(rm_list), c.DEFAULT_BEAM_WIDTH))

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
                cs_with_child = solve_conflicting_ranks(cs_with_child, {row,}, {col,})
                candidate_schedules_with_children.append(cs_with_child)
        
        candidate_schedules = beam_search(candidate_schedules_with_children, (row, col))
