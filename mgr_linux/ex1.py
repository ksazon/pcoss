from multiprocessing import Pool
import time
from random import random
import math

def operation(x):
    return sum([math.cosh(v / math.pi) ** math.pi for v in x]) / len(x)

if __name__ == '__main__':
    dataset_size = 5*10**6
    datasets_count = 12
    processes_count = 8

    ts0 = time.monotonic()

    datasets = [
        [random() for _ in range(dataset_size)]
        for _ in range(datasets_count)]

    te0 = time.monotonic()
    print(f'generate = {te0-ts0:.3f}s')

    ts_seq = time.monotonic()
    
    z = [operation(x) for x in datasets]
    
    te_seq = time.monotonic()
    t_seq = te_seq - ts_seq
    print(f'sequential = {t_seq:.3f}s')

    ts_par = time.monotonic()
    with Pool(processes_count) as p:
        u = p.map_async(operation, datasets)
        l = [x for x in u.get()]
        
    te_par = time.monotonic()
    t_par = te_par - ts_par

    print(f'parallel = {t_par:.3f}s')
    print(f'sequential to parallel = {t_seq/t_par:.2f}x')
