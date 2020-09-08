from random import random
from typing import List, Set, Tuple

import networkx as nx
from matplotlib import pyplot as plt

import operations as o


def id_func(x):
    return x


def create_conflict_graph_from_cnts_and_conflicting_machine_list(
        job_cnt: int,
        machine_cnt: int,
        conflicting_machines: Set[Tuple[int, int]],
        show=True) -> nx.Graph:

    G = nx.Graph()
    for job_idx in range(job_cnt):
        job_nodes = [(job_idx,machine_idx) for machine_idx
            in range(machine_cnt)]
        G.add_nodes_from(job_nodes)

        for cm1, cm2 in conflicting_machines:
            G.add_edge((job_idx,cm1), (job_idx,cm2))
        
        for prev_job_idx in range(job_idx):
            for machine_idx in range(machine_cnt):
                G.add_edge((prev_job_idx,machine_idx), (job_idx,machine_idx))

    if show:
        plt.figure(figsize=(6,6))
        pos = {(x,y):(y+random()/3,-x) for x,y in G.nodes()}
        
        nx.draw(G, with_labels=True, pos=pos, connectionstyle='arc3, rad=2')
        plt.show()
    
    return G


class Cfg:
    def __init__(self, filepath: str):
        self.index_cols = ['id',]
        self.grouping_cols = ['gr1',]
        self.conflicting_machines = {(1,2),}
        self.operation_addresses = {
            0: o.operation_a, 1: o.operation_b, 2: o.operation_c}
        self.beam_width = 5
