from code import interact
from random import randint
from re import compile, IGNORECASE
from socket import socket, AF_INET6, SOCK_STREAM, IPPROTO_TCP
from struct import pack, unpack, calcsize
from sys import argv, stderr

# from ssl import create_default_context, Purpose

I2 = "<2i"
I = "<i"
I2L = calcsize(I2)
IL = calcsize(I)
S2L = calcsize("2s")

CR = compile(r"\u00a7([\da-fk-or])", IGNORECASE)

COLOR = {
    '0': '\033[0;30m',  # 00 BLACK
    '1': '\033[0;34m',  # 01 BLUE
    '2': '\033[0;32m',  # 02 GREEN
    '3': '\033[0;36m',  # 03 CYAN
    '4': '\033[0;31m',  # 04 RED
    '5': '\033[0;35m',  # 05 PURPLE
    '6': '\033[0;33m',  # 06 GOLD
    '7': '\033[0;37m',  # 07 GREY
    '8': '\033[1;30m',  # 08 DARK_GREY
    '9': '\033[1;34m',  # 09 LIGHT_BLUE
    'a': '\033[1;32m',  # 10 LIGHT_GREEN
    'b': '\033[1;36m',  # 11 LIGHT_CYAN
    'c': '\033[1;31m',  # 12 LIGHT_RED
    'd': '\033[1;35m',  # 13 LIGHT_PURPLE
    'e': '\033[1;33m',  # 14 YELLOW
    'f': '\033[1;37m',  # 15 WHITE
    'k': '\033[6m',  # Obfuscated
    'l': '\033[1m',  # Bold
    'm': '\033[9m',  # Strikethrough
    'n': '\033[4m',  # Underline
    'o': '\033[3m',  # Italic
    'r': '\033[0m'  # Reset
}


def send(so: socket, client: int, request: int, data: bytes) -> None:
    auth = pack(I2, client, request) + data + b"\x00\x00"
    so.send(pack(I, len(auth)) + auth)


def receive(so: socket, client: int) -> str:
    res = b''
    while True:
        a = unpack(I, so.recv(IL))[0] - 10
        b, c = unpack(I2, so.recv(I2L))
        again = a // 4096
        s = f"{a if 0 <= a < 4096 else 0 if a < 0 else 4096}s"
        sl = calcsize(s)
        d = unpack(s, so.recv(sl))[0]
        print(f"Response: {c}", file=stderr)
        if so.recv(S2L) == b'\x00\x00':
            if b != client:
                print(f"{b} not equals {client}", file=stderr)
                break
            res += d
            if again == 0:
                return res.decode()
            else:
                continue
        else:
            break
    return res.decode()


if __name__ == '__main__':
    try:
        # ctx = create_default_context(Purpose.CLIENT_AUTH)
        with socket(AF_INET6, SOCK_STREAM, IPPROTO_TCP) as sock:
            # sock = ctx.wrap_socket(sock, server_hostname="localhost")
            address = input("IP: ") or argv[1]
            port = int(input("Port: ") or argv[2])
            sock.connect((address, port))
            client_id = -1


            def reader(prompt) -> str:
                global client_id
                raw = input(prompt)
                if raw.startswith("/"):
                    command = raw[1:]
                    if command.startswith("login"):
                        client_id = randint(11, 2147483647)
                        password = (input("Password: ") or argv[3]).encode()
                        send(sock, client_id, 3, password)
                    else:
                        send(sock, client_id, 2, command.encode())
                    res = receive(sock, client_id)
                    print(f"{CR.sub(lambda m: COLOR.get(m.group(1)), res)}{COLOR['r']}")
                    return ""
                return raw


            interact(banner="Minecraft RCon", readfunc=reader, local=locals(), exitmsg="Exit")
    except Exception as e:
        print(e)
