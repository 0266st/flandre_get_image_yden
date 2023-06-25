import asyncio

async def boil_udon():
    print('  うどんを茹でます。')
    await asyncio.sleep(3)
    print('  うどんが茹であがりました.')

async def make_tuyu():
    print('  ツユを作ります。')
    await asyncio.sleep(2)
    print('  ツユができました.')

async def main():
    print('うどんを作ります.')
    task1 = asyncio.create_task(boil_udon())
    task2 = asyncio.create_task(make_tuyu())
    await task1
    await task2
    print('盛り付けます.')
    print('うどんができました.')

asyncio.run(main())
