import asyncio 

# simulate time consuming task
async def fetch_data(delay):
    print("Fetching data")
    await asyncio.sleep(delay)
    print("Data Fetched")
    return{"data": "Some Data"}

async def main():
    print("Start of coroutine")
    task = fetch_data(2)
    #await 
    result = await task
    print(f"Received Result: {result}")
    print("End of coroutine")

asyncio.run(main())
