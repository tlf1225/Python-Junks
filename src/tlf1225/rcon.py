from code import interact
from random import randint
from re import compile as rc, IGNORECASE
from socket import socket, AF_INET6, SOCK_STREAM, IPPROTO_TCP
from struct import pack, unpack, calcsize
from sys import argv, stderr


# noinspection SpellCheckingInspection
class MCRcon(socket):

    # noinspection SpellCheckingInspection
    def __init__(self, family: int = ..., sock_type: int = ..., proto: int = ..., client_id: int = -1) -> None:
        super().__init__(family, sock_type, proto)
        self.client_id = client_id
        self.COLOR = {
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
        self.I3 = "<3i"
        self.I3L = calcsize(self.I3)
        self.S2 = "2s"
        self.I2S2L = calcsize("<2i") + calcsize(self.S2)
        self.CR = rc(r"\u00a7(\w)", IGNORECASE)

    def rcon_send(self, request: int, data: bytes) -> None:
        self.send(pack(self.I3, self.I2S2L + calcsize(f"{len(data)}s"), self.client_id, request) + data + b"\x00\x00")

    def rcon_recv(self) -> str:
        res = b''
        while True:
            a, b, c = unpack(self.I3, self.recv(self.I3L))
            a -= self.I2S2L
            again = a // 4096
            s = f"{a if 0 <= a <= 4096 else 0 if a < 0 else 4096}s{self.S2}"
            sl = calcsize(s)
            d, pad = unpack(s, self.recv(sl))
            if pad:
                print(f"Response: {c}", file=stderr)
                if b != self.client_id:
                    print(f"Client: {b} not valid {self.client_id}", file=stderr)
                    break
                res += d
                if again:
                    continue
                else:
                    return res.decode()
            else:
                break
        return res.decode()

    def exec(self, req: int, command: bytes):
        self.rcon_send(req, command)
        print(f"{self.CR.sub(lambda m: self.COLOR.get(m.group(1)), self.rcon_recv())}")

    def login(self, password: str):
        password = (password or input("Password: ")).encode()
        self.exec(3, password)

    def command(self, command: str):
        self.exec(2, command.encode())

    def reader(self, prompt: str):
        raw = input(prompt)
        if raw.startswith("/"):
            self.command(raw[1:])
            return ""
        return raw


def main():
    try:
        client_id = randint(11, 2147483647)
        with MCRcon(AF_INET6, SOCK_STREAM, IPPROTO_TCP, client_id) as sock:
            address = input("IP: ") or (argv[1] if len(argv) > 1 else "localhost")
            port = int(input("Port: ") or (int(argv[2]) if len(argv) > 2 else 25575))
            sock.connect((address, port))
            sock.login(argv[3] if len(argv) > 3 else "")
            work = globals().copy()
            work.update(locals())
            interact(banner="Minecraft RCon", readfunc=sock.reader, local=work, exitmsg="Exit")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
