import sched
import time
import asyncio

sc = sched.scheduler(time.time, time.sleep)

def o1():
    print('1 -s')
    asyncio.sleep(5)
    print('1 -e')
    # yield '1'

def o2():
    print('2 -s')
    asyncio.sleep(5)
    print('2 -e')
    # yield '2'

sc.enter(0, 0, o1)
sc.enter(0, 0, o2)

ts = time.monotonic()
sc.run()
te = time.monotonic()

print(te-ts)
