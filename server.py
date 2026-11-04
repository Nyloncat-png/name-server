import asyncio.streams

class NameServer:
    def __init__(self, host='127.0.0.1', port=6000):
        self.reader = None
        self.writer = None
        self.host = host
        self.port = port

class TimeServer:
    def __init__(self, host='127.0.0.1', port=6001):
        self.reader = None
        self.writer = None
        self.host = host
        self.port = port

class EchoServer:
    def __init__(self, host='127.0.0.1', port=6002):
        self.reader = None
        self.writer = None
        self.host = host
        self.port = port

async def main():
    name_server = NameServer()
    time_server = TimeServer()
    echo_server = EchoServer()



if __name__ == '__main__':
    asyncio.run(main())