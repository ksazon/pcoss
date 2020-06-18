from multiprocessing import Pool
import time
# from random import random
# import math
# from operator import itemgetter
import requests
# import asyncio
import time

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

BASE_URL = r'https://localhost:44320/Operations'

def operationA(x):
    return requests.get(f'{BASE_URL}/A/{len(x) * 1000}', verify=False).content

def operationB(x):
    return requests.get(f'{BASE_URL}/B/{len(x) * 20}', verify=False).content

def operationC(x):
    return requests.get(f'{BASE_URL}/C/{len(x) * 100}', verify=False).content

if __name__ == '__main__':
    tl = [
        ('pol', range(5), range(10)),
        ('ger', range(10), range(5)),
        ('rus', range(20), range(20)),
        ('nor', range(50), range(50)),
        ('fin', range(100), range(5)),
        ('usa', range(5), range(20)),
        ('bel', range(10), range(0)),
        ]

    # print(sum([len(y) for x in tl for y in x]))
    # print('longest row')
    # print(max(
    #     [sum([len(e) for e in r]) for r in tl])
    #     )
    # print('longest column')
    # print(max(
    #     sum([len(r[0]) for r in tl]),
    #     sum([len(r[1]) for r in tl]),
    #     sum([len(r[2]) for r in tl]),
    #     ))

    # print(max(
    #     sum([len(r[c]

    #         for c in range(len(r[0])
    #         for r in tl))))

    processes_count = 3

    # ts_seq = time.monotonic()
    
    # z = [(operationA(a), operationB(b), operationC(c)) for (a,b,c) in tl]
    
    # te_seq = time.monotonic()
    # t_seq = te_seq - ts_seq
    # print(f'sequential = {t_seq:.3f}s')

    time.sleep(2)

    t0 = time.monotonic()
    with Pool(processes_count) as p:
        t1 = time.monotonic()

        u0 = p.map_async(operationA, [x[0] for x in tl])
        u1 = p.map_async(operationB, [x[1] for x in tl])
        u2 = p.map_async(operationC, [x[2] for x in tl])

        t2 = time.monotonic()
        
        # print(time.time())
        # u0g = u0.get()
        # print(time.time())
        # u1g = u1.get()
        # print(time.time())
        # u2g = u2.get()
        # print(time.time())
        # p.

        l = [x for x in zip(u0.get(), u1.get(), u2.get())]

        t3 = time.monotonic()
        
    t4 = time.monotonic()

    print(f't1-t0: {t1-t0} \t t2-t1: {t2-t1} \t t3-t2: {t3-t2}')
    print(f't4-t3: {t4-t3}')
    print(f't3-t1: {t3-t1}')
