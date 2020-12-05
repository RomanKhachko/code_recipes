import asyncio
from asyncio import Protocol
from threading import Thread

PORT = 9999


async def sample_coro(sleep_time):
    print("coroutine is called")
    await asyncio.sleep(sleep_time)
    return "Awake again"


def short_lived_loop_example():
    local_loop = asyncio.new_event_loop()
    thread_running_loop = Thread(target=local_loop.run_forever)
    thread_running_loop.start()
    fut = asyncio.run_coroutine_threadsafe(
        local_loop.create_connection(lambda: Protocol(), host='0.0.0.0', port=PORT), local_loop)
    transport, protocol = fut.result()
    transport.write("A message from client".encode())
    # loop should be properly stopped and closed, since it's not the end of the program and resources have to be released
    local_loop.call_soon_threadsafe(local_loop.stop)
    thread_running_loop.join()
    local_loop.close()
    print(local_loop.is_closed())


class RomanServerProtocol(Protocol):
    def connection_made(self, transport):
        print("Connection from: {}".format(transport.get_extra_info('peername')))

    def data_received(self, data):
        message = data.decode()
        print('Received from client: ', message)


async def run_server():
    server = await asyncio.get_running_loop().create_server(
        lambda: RomanServerProtocol(), '127.0.0.1', PORT)

    async with server:
        await server.serve_forever()


main_loop = asyncio.new_event_loop()
Thread(target=main_loop.run_forever).start()

# calling async code and wait till execution is finished:
future = asyncio.run_coroutine_threadsafe(sample_coro(1), main_loop)
print(future.result())

# calling async code taking longer than our timeout and excepting exception to be raised
try:
    asyncio.run_coroutine_threadsafe(sample_coro(2), main_loop).result(1)
except Exception:
    print("execution took longer than expected")

# running server accepting connections from the client
asyncio.run_coroutine_threadsafe(run_server(), main_loop)

# running client connecting and sending some data to the server running in a separate loop
short_lived_loop_example()

# stopping main loop
main_loop.call_soon_threadsafe(main_loop.stop)
