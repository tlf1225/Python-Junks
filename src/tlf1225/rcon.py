from random import randint
from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP
from struct import pack, unpack, calcsize
from sys import argv

I2 = "<2i"
I = "<i"
I2L = calcsize(I2)
IL = calcsize(I)
S2L = calcsize("2s")


# noinspection SpellCheckingInspection
def send(so: socket, client: int, request: int, data: bytes):
    auth = pack(I2, client, request) + data + b"\x00\x00"
    so.send(pack(I, len(auth)) + auth)


# noinspection SpellCheckingInspection
def recv(so: socket):
    a = unpack(I, so.recv(IL))[0] - 10
    b, c = unpack(I2, so.recv(I2L))
    s = f"{a}s"
    sl = calcsize(s)
    d = unpack(s, so.recv(sl))[0]
    if so.recv(S2L) == b'\x00\x00':
        return a, b, c, d


if __name__ == '__main__':
    try:
        with socket(AF_INET, SOCK_STREAM, IPPROTO_TCP) as sock:
            address = input("IP: ") or argv[1]
            port = int(input("Port: ") or argv[2])
            sock.connect((address, port))
            client_id = randint(11, 2147483647)
            password = input("Password: ").encode() or argv[3].encode()
            send(sock, client_id, 3, password)
            res = recv(sock)
            while True:
                try:
                    print(f"len: {res[0]}, id: {res[1]}, type: {res[2]}, data: {res[3].decode()}")
                    command = input(">> ").encode()
                    send(sock, client_id, 2, command)
                    res = recv(sock)
                except EOFError as e:
                    break
    except Exception as e:
        print(e)
