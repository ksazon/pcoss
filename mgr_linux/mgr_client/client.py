import requests
import asyncio
import time

async def a():
    return requests.get(r'https://localhost:44320/OperationA/3000', verify=False).content

async def main():
    print("1")
    print(await a())
    print("2")

asyncio.run(main())
