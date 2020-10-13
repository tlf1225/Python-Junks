from random import randint
from socket import socket, AF_INET6, SOCK_DGRAM, IPPROTO_UDP
from struct import pack, unpack

if __name__ == '__main__':
    with socket(AF_INET6, SOCK_DGRAM, IPPROTO_UDP) as sock:
        sock.connect(("localhost", 25565))
        session_id = randint(11, 2147483647) & 0x0F0F0F
        packet1 = b"\xFE\xFD\x09" + pack(">i", session_id)
        sock.send(packet1)
        packet2 = sock.recv(1024)
        tp, res_id = unpack(">ci", packet2[:5])
        challenge_token = int(packet2[5:].split(b'\x00')[0])
        if res_id == session_id:
            packet3 = b"\xFE\xFD\x00" + pack(">2i", session_id, challenge_token)
            sock.send(packet3)
            packet4 = sock.recv(1024)
            tp, res_id = unpack(">ci", packet4[:5])
            if session_id == res_id:
                info1 = [c for c in packet4[5:].split(b'\x00') if c]
                # noinspection SpellCheckingInspection
                print(f"Motd: {info1[0].decode()} Type: {info1[1].decode()} Map: {info1[2].decode()}")
                print(f"Now Player / Max Player: {info1[3].decode()} / {info1[4].decode()}")
                print(f"PORT: {unpack('<h', info1[5][:2])[0]} IP: {info1[5][2:].decode()}")
                packet5 = packet3 + b'\x00\x00\x00\x00'
                sock.send(packet5)
                packet6 = sock.recv(1024)
                tp, res_id = unpack(">ci", packet6[:5])
                if session_id == res_id:
                    # print(packet6[5:16])
                    info2 = [c for c in packet6[16:].split(b'\x00') if c]
                    for i in range(0, len(info2), 2):
                        if info2[i][1:-1] == b"player":
                            i += 1
                            break
                        print(f"{info2[i].decode()}: {info2[i + 1].decode()}")
                    print("Player")
                    print(b"\n".join(info2[i:]).decode())
