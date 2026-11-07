import socket, json

def lookup_service(name_service):
    host = "127.0.0.1"
    port = 6000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))

        reply = {"cmd": "lookup", "service": name_service}
        sock.sendall((json.dumps(reply) + "\n").encode())
        buffer = b''
        while b'\n' not in buffer:
            datas = sock.recv(1024)
            if not datas:
                break
            buffer += datas

        response = json.loads(buffer.decode().strip())
        if response["status"] == "ok":
            return response["host"], response["port"]
        else:
            print(f"Error from NameServer: {response['message']}")
            return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None
    finally:
        sock.close()


def main():
    try:
        while True:
            decision = input("Select 1 for time, 2 for echo: ")
            if decision == "1":
                response = lookup_service("time")

                if response[1] is not None:
                    host = response[0]
                    port = response[1]

                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        sock.connect((host, port))
                        reply = {"cmd": "time"}
                        sock.sendall((json.dumps(reply) + "\n").encode())

                        buffer = b''
                        while b'\n' not in buffer:
                            datas = sock.recv(1024)
                            if not datas:
                                break
                            buffer += datas

                        response = json.loads(buffer.decode().strip())
                        if response["status"] == "ok":
                            print(f"Time: {response['time']}")
                        else:
                            print(f"Error from TimeServer: {response['message']}")
                    except Exception as e:
                        print(f"Error: {e}")
                    finally:
                        sock.close()
            elif decision == "2":
                pass
            else:
                print("Invalid choice")
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == '__main__':
    main()