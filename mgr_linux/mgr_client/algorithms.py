import random

# _algorithm_dict = {
#     'random': alg_random,
# }

def alg_random(table):
    return [
        (random.random() * 5, (r_idx, c_idx))
        for (r_idx, r) in enumerate(table)
        for (c_idx, c) in enumerate(r)
        ]

def alg_insertion_beam(processing_times: pd.DataFrame, conflict_graph: nx.Graph):
    pt = processing_times.to_numpy()
    candidate_schedules = [np.full(pt.shape, np.nan),]

    def solve_conflicts(rm: np.ndarray, changed_rows: Set[int], changed_cols: Set[int]):
        new_changed_rows = set()
        new_changed_cols = set()

        for cr in changed_rows:
            for cc in changed_cols:
                for cv in np.where(rm[:,cc] == rm[cr,cc])[0]:
                    if cv == cr:
                        continue
                    new_changed_rows.add(cr)
                    new_changed_cols.add(cc)
                    rm[cv] += 1
        
        if new_changed_rows:
            return solve_conflicts(rm, new_changed_rows, new_changed_cols)
        
        return rm

    def row_conflicts(rm: np.ndarray, row: int, col: int):
        if col == 2 and not np.isnan(rm[row,3]): return [(row,3),]
        if col == 3 and not np.isnan(rm[row,2]): return [(row,2),]
        return []

    def insertion_order():
        # TODO better function
        return np.random.permutation(list(np.ndindex(pt.shape)))

    def beam_search(rm: Set[np.ndarray]):
        # TODO better function
        return random.sample(rm, min(len(rm), 5))

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
                cs_with_child = solve_conflicts(cs_with_child, {row,}, {col,})
                candidate_schedules_with_children.append(cs_with_child)
        
        candidate_schedules = beam_search(candidate_schedules_with_children)
