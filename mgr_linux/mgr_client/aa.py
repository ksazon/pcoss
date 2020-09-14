import sched
import time
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def o1():
    print('1 -s')
    await asyncio.sleep(5)
    print('1 -e')
    return '1'
    # yield '1'

async def o2():
    print('2 -s')
    await asyncio.sleep(2)
    print('dupa')
    await asyncio.sleep(2)
    print('2 -e')
    return '2'
    # yield '2'

async def main():
    # sc = sched.scheduler(time.time, time.sleep)
    # sc = AsyncIOScheduler()
    # print('x')
    # sc.enter(0, 0, o1)
    # sc.enter(0, 0, o2)
    # sc.add_job(o1)
    # sc.add_job(o2)

    # ts = time.perf_counter()
    # l = [o1(), o1()]
    # await asyncio.gather(*l)
    # # sc.run(blocking=False)
    # # sc.start()
    # te = time.perf_counter()

    # print(te-ts) 
    gantt()


def gantt():
    import plotly.express as px
    import pandas as pd
    from datetime import timedelta

    x = eval('[(0, 15, 0, 0.4), (1, 5, 0, 0.3), (3, 3, 0, 0.7), (4, 7, 0, 1.0), (5, 19, 0, 1.1), (6, 1, 0, 0.5), (7, 0, 0, 4.3), (9, 4, 0, 0.3), (10, 2, 0, 0.5), (11, 8, 0, 2.1), (12, 16, 0, 4.1), (12, 17, 0, 0.2), (14, 18, 0, 0.5), (15, 9, 0, 0.8), (15, 14, 0, 0.7), (16, 12, 0, 5.9), (17, 10, 0, 0.1), (18, 6, 0, 0.5), (19, 11, 0, 3.3), (19, 13, 0, 0.5), (0, 17, 5.9, 6.7), (1, 0, 5.9, 10.2), (1, 6, 5.9, 6.7), (2, 2, 5.9, 6.6000000000000005), (2, 7, 5.9, 7.6000000000000005), (3, 1, 5.9, 8.9), (4, 11, 5.9, 10.2), (4, 15, 5.9, 6.800000000000001), (5, 16, 5.9, 10.4), (6, 18, 5.9, 8.2), (8, 10, 5.9, 7.2), (8, 14, 5.9, 7.6000000000000005), (9, 5, 5.9, 6.300000000000001), (9, 9, 5.9, 6.9), (10, 12, 5.9, 13.3), (10, 13, 5.9, 7.0), (11, 3, 5.9, 7.2), (13, 4, 5.9, 6.7), (19, 19, 5.9, 6.7), (2, 3, 13.3, 15.100000000000001), (3, 6, 13.3, 14.3), (3, 10, 13.3, 14.700000000000001), (5, 4, 13.3, 14.3), (6, 19, 13.3, 17.1), (7, 9, 13.3, 14.3), (8, 18, 13.3, 15.700000000000001), (9, 8, 13.3, 21.0), (10, 5, 13.3, 15.200000000000001), (10, 7, 13.3, 15.200000000000001), (10, 11, 13.3, 19.700000000000003), (11, 0, 13.3, 14.0), (11, 15, 13.3, 14.600000000000001), (12, 2, 13.3, 15.3), (13, 17, 13.3, 14.4), (18, 13, 13.3, 15.200000000000001), (18, 14, 13.3, 16.0), (19, 12, 13.3, 21.4), (19, 16, 13.3, 22.0), (0, 0, 22.0, 26.9), (1, 3, 22.0, 25.5), (2, 9, 22.0, 23.5), (2, 12, 22.0, 30.3), (3, 7, 22.0, 24.7), (5, 15, 22.0, 23.3), (6, 6, 22.0, 23.0), (6, 16, 22.0, 22.1), (6, 17, 22.0, 24.1), (7, 18, 22.0, 25.7), (8, 4, 22.0, 23.6), (9, 19, 22.0, 27.6), (11, 10, 22.0, 23.5), (12, 1, 22.0, 31.0), (13, 13, 22.0, 24.7), (13, 14, 22.0, 25.2), (15, 11, 22.0, 28.4), (17, 5, 22.0, 24.1), (19, 2, 22.0, 22.7), (0, 2, 31.0, 34.7), (0, 10, 31.0, 32.7), (0, 18, 31.0, 35.0), (4, 13, 31.0, 35.0), (5, 3, 31.0, 34.9), (5, 14, 31.0, 35.3), (7, 5, 31.0, 36.2), (7, 7, 31.0, 35.4), (8, 6, 31.0, 32.3), (9, 12, 31.0, 39.6), (10, 17, 31.0, 33.2), (11, 11, 31.0, 38.1), (13, 0, 31.0, 34.2), (14, 19, 31.0, 38.7), (16, 9, 31.0, 33.2), (17, 1, 31.0, 32.8), (17, 8, 31.0, 32.6), (18, 4, 31.0, 32.7), (18, 15, 31.0, 32.4), (2, 10, 39.6, 44.9), (3, 8, 39.6, 40.300000000000004), (5, 18, 39.6, 43.800000000000004), (6, 5, 39.6, 41.800000000000004), (6, 12, 39.6, 45.300000000000004), (9, 11, 39.6, 45.300000000000004), (10, 4, 39.6, 41.5), (10, 15, 39.6, 42.6), (11, 7, 39.6, 41.2), (11, 13, 39.6, 43.800000000000004), (11, 19, 39.6, 44.1), (14, 9, 39.6, 43.2), (14, 16, 39.6, 49.3), (15, 2, 39.6, 43.7), (15, 3, 39.6, 45.1), (15, 6, 39.6, 41.800000000000004), (15, 17, 39.6, 42.6), (18, 0, 39.6, 44.6), (19, 14, 39.6, 44.1), (1, 12, 49.3, 58.9), (1, 17, 49.3, 53.599999999999994), (2, 13, 49.3, 51.699999999999996), (3, 14, 49.3, 51.699999999999996), (3, 16, 49.3, 50.9), (4, 18, 49.3, 53.8), (5, 5, 49.3, 53.0), (5, 6, 49.3, 51.5), (6, 15, 49.3, 54.5), (7, 3, 49.3, 55.0), (9, 2, 49.3, 50.099999999999994), (10, 9, 49.3, 53.4), (12, 4, 49.3, 51.699999999999996), (14, 8, 49.3, 50.5), (15, 0, 49.3, 55.0), (15, 1, 49.3, 52.8), (16, 10, 49.3, 55.9), (16, 11, 49.3, 56.8), (18, 19, 49.3, 50.8), (19, 7, 49.3, 53.8), (3, 13, 58.9, 62.0), (4, 16, 58.9, 61.0), (7, 8, 58.9, 67.1), (7, 10, 58.9, 61.6), (8, 9, 58.9, 62.5), (8, 12, 58.9, 68.6), (8, 15, 58.9, 64.3), (9, 0, 58.9, 64.9), (11, 5, 58.9, 64.4), (12, 7, 58.9, 63.8), (13, 18, 58.9, 64.6), (13, 19, 58.9, 60.9), (14, 17, 58.9, 64.3), (16, 2, 58.9, 61.3), (16, 3, 58.9, 65.2), (16, 4, 58.9, 61.6), (17, 6, 58.9, 61.699999999999996), (17, 14, 58.9, 63.4), (18, 11, 58.9, 59.4), (0, 3, 68.6, 76.5), (0, 4, 68.6, 70.19999999999999), (1, 7, 68.6, 75.1), (1, 15, 68.6, 74.3), (1, 19, 68.6, 70.6), (2, 11, 68.6, 69.6), (4, 12, 68.6, 74.0), (4, 17, 68.6, 74.3), (5, 8, 68.6, 73.39999999999999), (7, 13, 68.6, 69.5), (10, 6, 68.6, 71.69999999999999), (10, 16, 68.6, 70.8), (11, 9, 68.6, 73.1), (12, 5, 68.6, 74.5), (12, 18, 68.6, 74.39999999999999), (13, 2, 68.6, 73.89999999999999), (14, 0, 68.6, 74.8), (14, 14, 68.6, 73.19999999999999), (15, 10, 68.6, 75.6), (16, 1, 68.6, 69.69999999999999), (0, 5, 76.5, 82.9), (0, 7, 76.5, 83.0), (0, 16, 76.5, 78.1), (2, 15, 76.5, 82.7), (2, 18, 76.5, 78.8), (3, 11, 76.5, 77.7), (3, 19, 76.5, 78.0), (4, 4, 76.5, 81.0), (5, 9, 76.5, 81.5), (8, 13, 76.5, 81.5), (9, 3, 76.5, 84.6), (9, 10, 76.5, 83.6), (9, 14, 76.5, 81.4), (9, 17, 76.5, 82.7), (10, 1, 76.5, 84.2), (10, 8, 76.5, 79.1), (11, 2, 76.5, 81.1), (15, 12, 76.5, 82.0), (16, 0, 76.5, 78.0), (16, 6, 76.5, 80.0), (3, 0, 84.6, 86.39999999999999), (3, 2, 84.6, 92.6), (4, 9, 84.6, 89.8), (5, 10, 84.6, 92.19999999999999), (7, 19, 84.6, 86.8), (9, 18, 84.6, 88.69999999999999), (11, 1, 84.6, 93.5), (11, 12, 84.6, 90.3), (12, 6, 84.6, 85.39999999999999), (12, 8, 84.6, 89.89999999999999), (12, 14, 84.6, 90.5), (13, 15, 84.6, 92.0), (13, 16, 84.6, 86.89999999999999), (14, 3, 84.6, 94.19999999999999), (15, 13, 84.6, 89.89999999999999), (16, 7, 84.6, 86.8), (17, 11, 84.6, 86.19999999999999), (17, 17, 84.6, 92.19999999999999), (19, 4, 84.6, 89.1), (19, 5, 84.6, 91.8), (0, 13, 94.19999999999999, 99.89999999999999), (1, 4, 94.19999999999999, 99.89999999999999), (2, 5, 94.19999999999999, 101.79999999999998), (2, 6, 94.19999999999999, 98.29999999999998), (4, 0, 94.19999999999999, 97.29999999999998), (5, 12, 94.19999999999999, 99.89999999999999), (6, 7, 94.19999999999999, 101.19999999999999), (7, 14, 94.19999999999999, 100.39999999999999), (8, 8, 94.19999999999999, 97.69999999999999), (10, 3, 94.19999999999999, 103.89999999999999), (11, 18, 94.19999999999999, 97.79999999999998), (12, 9, 94.19999999999999, 99.49999999999999), (13, 1, 94.19999999999999, 96.49999999999999), (13, 10, 94.19999999999999, 96.99999999999999), (13, 11, 94.19999999999999, 95.79999999999998), (14, 2, 94.19999999999999, 102.1), (14, 15, 94.19999999999999, 102.29999999999998), (17, 19, 94.19999999999999, 99.49999999999999), (18, 16, 94.19999999999999, 97.79999999999998), (18, 17, 94.19999999999999, 99.89999999999999), (0, 9, 103.89999999999999, 108.3), (2, 1, 103.89999999999999, 108.8), (4, 5, 103.89999999999999, 110.89999999999999), (4, 6, 103.89999999999999, 109.6), (4, 10, 103.89999999999999, 106.69999999999999), (5, 0, 103.89999999999999, 110.89999999999999), (6, 11, 103.89999999999999, 105.69999999999999), (6, 13, 103.89999999999999, 104.19999999999999), (6, 14, 103.89999999999999, 112.1), (7, 2, 103.89999999999999, 110.6), (7, 12, 103.89999999999999, 112.8), (7, 15, 103.89999999999999, 104.49999999999999), (7, 17, 103.89999999999999, 107.19999999999999), (8, 7, 103.89999999999999, 111.19999999999999), (8, 16, 103.89999999999999, 107.39999999999999), (12, 3, 103.89999999999999, 109.99999999999999), (15, 4, 103.89999999999999, 111.1), (18, 8, 103.89999999999999, 104.3), (18, 18, 103.89999999999999, 109.8), (0, 1, 112.8, 118.6), (0, 12, 112.8, 122.7), (3, 17, 112.8, 116.1), (6, 0, 112.8, 120.8), (6, 2, 112.8, 118.1), (6, 3, 112.8, 122.5), (6, 4, 112.8, 120.3), (7, 11, 112.8, 115.1), (8, 5, 112.8, 120.8), (8, 19, 112.8, 118.39999999999999), (12, 15, 112.8, 113.89999999999999), (15, 7, 112.8, 120.89999999999999), (15, 8, 112.8, 113.39999999999999), (16, 14, 112.8, 115.89999999999999), (17, 13, 112.8, 118.7), (17, 16, 112.8, 119.7), (18, 10, 112.8, 117.2), (19, 6, 112.8, 118.89999999999999), (19, 9, 112.8, 118.2), (19, 18, 112.8, 118.89999999999999), (0, 6, 122.7, 129.8), (1, 1, 122.7, 129.2), (2, 0, 122.7, 130.9), (2, 17, 122.7, 130.4), (3, 5, 122.7, 131.1), (7, 16, 122.7, 126.5), (8, 3, 122.7, 125.2), (10, 10, 122.7, 130.4), (11, 4, 122.7, 126.0), (11, 14, 122.7, 130.9), (12, 19, 122.7, 127.3), (13, 7, 122.7, 128.0), (14, 11, 122.7, 126.4), (14, 12, 122.7, 122.9), (15, 15, 122.7, 126.5), (15, 18, 122.7, 131.0), (16, 8, 122.7, 128.0), (16, 13, 122.7, 130.7), (18, 9, 122.7, 131.5), (1, 10, 131.5, 139.7), (1, 16, 131.5, 138.8), (2, 14, 131.5, 139.4), (2, 19, 131.5, 138.5), (3, 9, 131.5, 140.6), (3, 12, 131.5, 132.2), (3, 18, 131.5, 141.4), (5, 11, 131.5, 136.3), (7, 4, 131.5, 134.8), (8, 2, 131.5, 132.0), (9, 6, 131.5, 136.3), (9, 13, 131.5, 140.9), (10, 0, 131.5, 134.6), (14, 7, 131.5, 136.8), (16, 15, 131.5, 140.6), (16, 17, 131.5, 139.7), (18, 5, 131.5, 140.0), (19, 3, 131.5, 137.6), (19, 8, 131.5, 137.6), (0, 19, 141.4, 148.0), (1, 2, 141.4, 145.6), (2, 8, 141.4, 145.70000000000002), (2, 16, 141.4, 146.70000000000002), (3, 4, 141.4, 151.1), (3, 15, 141.4, 151.1), (4, 3, 141.4, 150.9), (4, 14, 141.4, 149.70000000000002), (5, 7, 141.4, 146.70000000000002), (6, 9, 141.4, 150.6), (8, 1, 141.4, 143.4), (8, 11, 141.4, 146.70000000000002), (12, 10, 141.4, 149.70000000000002), (12, 12, 141.4, 144.20000000000002), (13, 6, 141.4, 151.1), (14, 5, 141.4, 149.9), (14, 13, 141.4, 146.20000000000002), (16, 18, 141.4, 151.3), (19, 0, 141.4, 148.5), (19, 17, 141.4, 149.6), (1, 8, 151.3, 159.20000000000002), (1, 14, 151.3, 161.10000000000002), (1, 18, 151.3, 151.9), (4, 1, 151.3, 157.8), (5, 2, 151.3, 156.10000000000002), (7, 6, 151.3, 151.4), (8, 0, 151.3, 158.10000000000002), (8, 17, 151.3, 159.9), (12, 11, 151.3, 158.9), (12, 13, 151.3, 157.5), (14, 4, 151.3, 157.5), (16, 5, 151.3, 160.3), (16, 19, 151.3, 157.5), (17, 9, 151.3, 153.9), (18, 7, 151.3, 159.9), (18, 12, 151.3, 154.20000000000002), (19, 10, 151.3, 160.3), (19, 15, 151.3, 157.70000000000002), (1, 9, 161.10000000000002, 168.70000000000002), (1, 11, 161.10000000000002, 169.10000000000002), (4, 2, 161.10000000000002, 166.20000000000002), (4, 8, 161.10000000000002, 169.50000000000003), (5, 13, 161.10000000000002, 161.70000000000002), (5, 17, 161.10000000000002, 170.40000000000003), (9, 1, 161.10000000000002, 169.40000000000003), (9, 15, 161.10000000000002, 164.70000000000002), (10, 14, 161.10000000000002, 170.90000000000003), (10, 19, 161.10000000000002, 167.20000000000002), (13, 5, 161.10000000000002, 170.20000000000002), (14, 6, 161.10000000000002, 165.40000000000003), (14, 10, 161.10000000000002, 170.60000000000002), (16, 16, 161.10000000000002, 167.40000000000003), (17, 0, 161.10000000000002, 161.50000000000003), (17, 4, 161.10000000000002, 167.60000000000002), (17, 7, 161.10000000000002, 170.40000000000003), (17, 12, 161.10000000000002, 165.70000000000002), (17, 18, 161.10000000000002, 163.60000000000002), (0, 11, 170.90000000000003, 179.40000000000003), (0, 14, 170.90000000000003, 179.80000000000004), (1, 13, 170.90000000000003, 179.10000000000002), (2, 4, 170.90000000000003, 180.30000000000004), (4, 19, 170.90000000000003, 177.60000000000002), (6, 8, 170.90000000000003, 178.80000000000004), (6, 10, 170.90000000000003, 180.50000000000003), (9, 7, 170.90000000000003, 172.30000000000004), (10, 18, 170.90000000000003, 174.20000000000005), (11, 6, 170.90000000000003, 179.30000000000004), (11, 17, 170.90000000000003, 180.70000000000005), (12, 0, 170.90000000000003, 179.30000000000004), (13, 9, 170.90000000000003, 179.90000000000003), (13, 12, 170.90000000000003, 177.00000000000003), (15, 5, 170.90000000000003, 180.70000000000005), (15, 16, 170.90000000000003, 176.70000000000005), (17, 15, 170.90000000000003, 179.90000000000003), (18, 1, 170.90000000000003, 173.30000000000004), (0, 8, 180.70000000000005, 181.30000000000004), (9, 16, 180.70000000000005, 186.90000000000003), (14, 1, 180.70000000000005, 189.20000000000005), (15, 19, 180.70000000000005, 188.80000000000004), (17, 3, 180.70000000000005, 181.30000000000004), (18, 2, 180.70000000000005, 187.30000000000004), (5, 1, 189.20000000000005, 193.70000000000005), (11, 16, 189.20000000000005, 195.40000000000003), (13, 8, 189.20000000000005, 198.20000000000005), (17, 2, 189.20000000000005, 199.10000000000005), (18, 3, 189.20000000000005, 189.40000000000003), (7, 1, 199.10000000000005, 207.00000000000006), (13, 3, 199.10000000000005, 199.60000000000005), (19, 1, 207.00000000000006, 214.90000000000006)]')

    df = pd.DataFrame(x, columns=['j', 'm', 'st', 'et'])
    df['st2'] =  df.st.apply(lambda x: pd.to_datetime('2020-01-01') + pd.DateOffset(int(x)))
    df['et2'] =  df.et.apply(lambda x: pd.to_datetime('2020-01-01') + pd.DateOffset(int(x)))
    # pd.to_datetime('2020-01-01') + pd.Timedelta(days=df.st)
    # df['et2'] = pd.to_datetime('2020-01-01') + timedelta(days=df.et)
    # df = pd.DataFrame([
    #     dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28', Resource="Alex"),
    #     dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15', Resource="Alex"),
    #     dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30', Resource="Max")
    # ])

    fig = px.timeline(df, x_start="st2", x_end="et2", y="m", color="j")
    fig.show()

if __name__ == '__main__':
    asyncio.run(main())
    # await main()