import requests
import urllib3
import asyncio
import aiohttp

import constants as c

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def operation(endpoint: str, item, sched_time: float = 0,
        operation_duration: int = 0, session=None):

    url = f'{c.BASE_URL}/{endpoint}/{item}/{operation_duration}'
    
    await asyncio.sleep(sched_time)
    # async with session.get(url, verify=False) as resp:
    async with session.get(url, ssl=False) as resp:
        ret = await resp.text()
    # ret = await requests.get(url, verify=False).content
    
    if c.PRINT_RESPONSES:
        print(f'{endpoint=}\t{item=}\t{sched_time=}\t{operation_duration=}\t{ret=}')
    
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
