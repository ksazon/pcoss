import asyncio

import aiohttp
import requests
import urllib3

import constants as c

import time
from helpers import scheduled_operation

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def operation(so: scheduled_operation, session, ts):
    url = f'{c.BASE_URL}/{so.endpoint}/{so.machine}/{so.item}/{so.operation_duration-300}'
    
    it0 = time.perf_counter()
    await asyncio.sleep(so.start_time/1000.0)

    it1 = time.perf_counter()
    async with session.get(url, ssl=False, timeout=600) as resp:
        it2 = time.perf_counter()
        ret = await resp.text()

    it3 = time.perf_counter()

    if c.PRINT_RESPONSES:
        print(f'{url=}\t{ret=}')
    
    if c.PRINT_TIMES:
        # print(f'{so.endpoint=}\t{so.item=}\t{so.start_time=:.2f}\t{so.end_time=:.2f}\t{so.operation_duration=:.2f}\t{ret=}')
        print(f'{so.endpoint=}\t{so.machine=}\t{so.start_time=:.2f}\t{so.end_time=:.2f}\t{so.operation_duration=:.2f}')
        # print(f'it1-it0={it1-it0:.2f}\tit2-it1={it2-it1:.2f}\tit3-it2={it3-it2:.2f}\tit2-it0={it2-it0:.2f}\tit0-ts={it0-ts:.2f}')
        print(f'{'***' if it2-it1 > so.operation_duration else ''}\tit2-it1={it2-it1:.2f}')
    
    return ret


async def operation_a(x):
    ret = await requests.get(f'{c.BASE_URL}/A/{x}/0', verify=False).content
    if c.PRINT_RESPONSES:
        print('a', ret)
    return ret


async def operation_b(x):
    ret = await requests.get(f'{c.BASE_URL}/B/{x}/0', verify=False).content
    if c.PRINT_RESPONSES:
        print('b', ret)
    return ret


async def operation_c(x):
    ret = await requests.get(f'{c.BASE_URL}/C/{x}/0', verify=False).content
    if c.PRINT_RESPONSES:
        print('c', ret)
    return ret


async def operation_0(x):
    ret = await requests.get(f'{c.BASE_URL}/0/{x}/0', verify=False).content
    if c.PRINT_RESPONSES:
        print('0', ret)
    return ret
