import asyncio.streams, json
from datetime import datetime
from json import JSONDecodeError

host = "127.0.0.1"
portname = 6000
porttime = 6001
portecho = 6002

class NameServer:
    async def handle_stream(self, reader, writer):
        """
        json structure:
            status: ok/error
            service: time/echo
            host
            port
        """
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break

                try:
                    request = json.loads(data.decode().strip())

                    if "cmd" not in request:
                        reply = {"status": "error", "message": "missing cmd"}
                    elif request["cmd"] == "lookup":
                        if "service" not in request:
                            reply = {"status": "error", "message": "missing service"}
                        elif request["service"] == "time":
                            reply = {"status": "ok", "service": "time", "host": host, "port": porttime}
                        elif request["service"] == "echo":
                            reply = {"status": "ok", "service": "echo", "host": host, "port": portecho}
                        else:
                            reply = {"status": "error", "message": f"service '{request['service']}' not found"}
                    else:
                        reply = {"status": "error", "message": "unknown command"}

                except JSONDecodeError:
                    reply = {"status": "error", "message": "invalid json"}

                writer.write((json.dumps(reply) + "\n").encode())
                await writer.drain()

        except Exception as e:
            print(f"Error NameServer: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

class TimeServer:
    async def handle_stream(self, reader, writer):
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break

                try:
                    request = json.loads(data.decode().strip())

                    if "cmd" not in request:
                        reply = {"status": "error", "message": "missing cmd"}
                    elif request["cmd"] == "time":
                        reply = {"status": "ok", "time": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}
                    else:
                        reply = {"status": "error", "message": f"unknown command"}

                except JSONDecodeError:
                    reply = {"status": "error", "message": "invalid json"}

                writer.write((json.dumps(reply) + "\n").encode())
                await writer.drain()

        except Exception as e:
            print(f"Error TimeServer: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

class EchoServer:
    async def handle_stream(self, reader, writer):
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break

                try:
                    request = json.loads(data.decode().strip())

                    if "cmd" not in request:
                        reply = {"status": "error", "message": "missing cmd"}
                    elif request["cmd"] == "echo":
                        if "text" not in request:
                            reply = {"status": "error", "message": "missing text"}
                        else:
                            reply = {"status": "ok", "text": request["text"]}
                    else:
                        reply = {"status": "error", "message": f"unknown command"}

                except JSONDecodeError:
                    reply = {"status": "error", "message": "invalid json"}

                writer.write((json.dumps(reply) + "\n").encode())
                await writer.drain()

        except Exception as e:
            print(f"Error EchoServer: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

async def main():
    name_server = NameServer()
    time_server = TimeServer()
    echo_server = EchoServer()

    name = await asyncio.start_server(name_server.handle_stream, host, portname)
    time = await asyncio.start_server(time_server.handle_stream, host, porttime)
    echo = await asyncio.start_server(echo_server.handle_stream, host, portecho)

    print("Started servers")

    async with name, time, echo:
        await asyncio.gather(name.serve_forever(), time.serve_forever(), echo.serve_forever())

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Closing servers")