import time
from dataclasses import dataclass
from functools import wraps
from random import random
from typing import List, Set, Tuple

import networkx as nx
from matplotlib import pyplot as plt


def id_func(x):
    return x


def create_conflict_graph_from_cnts_and_conflicting_machine_list(
        job_cnt: int,
        machine_cnt: int,
        conflicting_machines: Set[Tuple[int, int]],
        show=True) -> nx.Graph:

    G = nx.Graph()
    for job_idx in range(job_cnt):
        job_nodes = [
            (job_idx, machine_idx)
            for machine_idx
            in range(machine_cnt)
            ]
        
        G.add_nodes_from(job_nodes)

        for cm1, cm2 in conflicting_machines:
            G.add_edge((job_idx, cm1), (job_idx, cm2))
        
        for prev_job_idx in range(job_idx):
            for machine_idx in range(machine_cnt):
                G.add_edge((prev_job_idx, machine_idx), (job_idx, machine_idx))

    if show:
        plt.figure(figsize=(6, 6))
        pos = {
            (x, y): (y + random() / 3, -x + random() / 3)
            for x, y in G.nodes()
            }
        
        nx.draw(G, with_labels=True, pos=pos, connectionstyle='arc3, rad=2')
        plt.show()
    
    return G


def get_func_exec_time_decorator(f: callable):
    @wraps(f)
    def wf(*args, **kwargs):
        st = time.perf_counter()
        f(*args, **kwargs)
        et = time.perf_counter()
        print(f'Function "{f.__name__}" exection time: {et-st:.3f}s')

    return wf


@dataclass
class scheduled_operation:
    rank: int
    start_time: float
    end_time: float
    operation_duration: float
    job: int
    machine: int
    endpoint: str
    item: object


def plot_gantt_chart(schedule: List[scheduled_operation]):
    import plotly.express as px
    import pandas as pd

    def tramsform_opearation_time_to_date(operation_time: float):
        beginning_date = pd.to_datetime('2020-01-01')

        return beginning_date + pd.DateOffset(int(operation_time/1000))

    schedule_df = pd.DataFrame([asdict(so) for so in schedule])

    print(f'max et: {max(schedule_df.end_time)}')
    schedule_df.start_time = schedule_df.start_time.apply(tramsform_opearation_time_to_date)
    schedule_df.end_time = schedule_df.end_time.apply(tramsform_opearation_time_to_date)

    fig = px.timeline(
        schedule_df,
        x_start="start_time",
        x_end="end_time",
        y="machine",
        color="job",
        color_continuous_scale=px.colors.sequential.Greys)
        
    fig.show()


def plot_schedule_graph(graph: nx.DiGraph):
    plt.figure(figsize=(12, 12))
    pos = {
        (x, y): (y + random.random() / 3, -x + random.random() / 3)
        for x, y in self.outcome_graph.nodes()
        }
    
    nx.draw(self.outcome_graph, pos=pos, with_labels=True)
    plt.show()
