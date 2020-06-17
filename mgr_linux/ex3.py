from multiprocessing import Pool
import time
from random import random
import math
from operator import itemgetter
import requests
import asyncio
import time

def time_amount_function(x):
    return len(x) / 10

def operation0(x):
    time.sleep(time_amount_function(x))
    return x[::-1]

def operation1(x):
    time.sleep(time_amount_function(x))
    return x[::-1]

def operation2(x):
    time.sleep(time_amount_function(x))
    return x[::-1]

def operation3(x):
    time.sleep(time_amount_function(x))
    return x[::-1]

def operation4(x):
    time.sleep(time_amount_function(x))
    return x[::-1]

def operation5(x):
    time.sleep(time_amount_function(x))
    return x[::-1]

def operation6(x):
    time.sleep(time_amount_function(x))
    return x[::-1]

def operation7(x):
    time.sleep(time_amount_function(x))
    return x[::-1]

def operation8(x):
    time.sleep(time_amount_function(x))
    return x[::-1]

def operationA(x):
    return requests.get(rf'https://localhost:44320/OperationA/{len(x) * 1000}', verify=False).content

if __name__ == '__main__':
    tl = [
        ('pol', [1,1,1,1,2,2,1,], 'abc'),
        ('ger', [1,2,1,1,2,], 'abcd'),
        ('rus', [2,1,2,], 'a'),
        ('nor', [5,2,1,1,], 'ab'),
        ('fin', [1,], 'abcde'),
        ('usa', [2,1,3], 'abcdefg'),
        ]

    print(sum([len(y) for x in tl for y in x]))
    print('longest row')
    print(max(
        [sum([len(e) for e in r]) for r in tl])
        )
    print('longest column')
    print(max(
        sum([len(r[0]) for r in tl]),
        sum([len(r[1]) for r in tl]),
        sum([len(r[2]) for r in tl]),
        ))


    processes_count = 8

    ts_seq = time.monotonic()
    
    z = [(operation0(a), operation1(b), operation2(c)) for (a,b,c) in tl]
    
    te_seq = time.monotonic()
    t_seq = te_seq - ts_seq
    print(f'sequential = {t_seq:.3f}s')

    ts_par = time.monotonic()
    with Pool(processes_count) as p:
        u0 = p.map_async(operation0, [x[0] for x in tl])
        u1 = p.map_async(operation1, [x[1] for x in tl])
        u2 = p.map_async(operation2, [x[2] for x in tl])
        print('a')
        
        # print(time.time())
        # u0g = u0.get()
        # print(time.time())
        # u1g = u1.get()
        # print(time.time())
        # u2g = u2.get()
        # print(time.time())
        # p.

        l = [x for x in zip(u0.get(), u1.get(), u2.get())]
        
    te_par = time.monotonic()
    t_par = te_par - ts_par

    print(f'parallel = {t_par:.3f}s')
    print(f'sequential to parallel = {t_seq/t_par:.2f}x')
