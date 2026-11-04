import socket

def main():
    host = 127.0.0.1
    port = 6000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))



if __name__ == '__main__':
    main()