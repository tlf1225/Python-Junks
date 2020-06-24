from socket import socket, AF_INET, SOCK_DGRAM, IPPROTO_UDP, SOL_SOCKET, SO_BROADCAST
from sys import argv
from time import sleep


def main(mac="FF" * 6):
    with socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP) as wol:
        wol.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        wol.sendto(b'\xFF' * 6 + bytes.fromhex(mac) * 16, ("255.255.255.255", 9))
        print(f"target: {mac}")


if __name__ == '__main__':
    if len(argv) > 1:
        main(argv[1])
    else:
        [main(x.replace(":", "", 5)[:12])
         for x in
         ["50:26:90:A4:E0:AB"
          # , "04:92:26:C2:4E:0F"
          # , "70:85:C2:AC:A9:B1"
          ]]

        sleep(2)
