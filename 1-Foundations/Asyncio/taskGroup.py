import asyncio

async def fetch_data(id, sleeptime):
    print(f"Coroutine{id} starting to fetch data")
    await asyncio.sleep(sleeptime)
    return{"id": id, "data": f"Sample data from coroutine{id}"}

async def main():
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for i, sleeptime in enumerate([2,1,3], start=1):
            task = tg.create_task(fetch_data(i, sleeptime))
            tasks.append(task)
    
    results = [task.result() for task in tasks]

    for result in results:
        print(f"Received Result:{result}")

asyncio.run(main())