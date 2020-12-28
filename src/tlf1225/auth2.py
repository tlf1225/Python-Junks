from getpass import getpass
from hashlib import sha256
from time import sleep, monotonic


def wait(sec):
    now = monotonic()
    dest = now + sec
    while True:
        now = monotonic()
        if dest < now:
            break
        print(f"残り{dest - now:3.2f}秒", end="\t")
        print(f"{(now - dest) + sec:3.2f}秒経過", end="\r")
        sleep(0.01)
    print("\t" * 8, end="\r")


def initialize():
    identity = input("Input ID: ")
    password = getpass("Input Password: ")
    return identity, password


def main():
    try:
        id_1, pass_1 = initialize()
        # Pattern 2
        hash_1 = sha256(id_1.encode())
        hash_2 = sha256(pass_1.encode())
        while True:
            id_2 = input("Check ID: ")
            pass_2 = getpass("Check Password: ")
            # Pattern 1
            if hash(id_1) == hash(id_2) and hash(pass_1) == hash(pass_2):
                print("OK")
                break

            # Pattern 2
            hash_3 = sha256(id_2.encode())
            hash_4 = sha256(pass_2.encode())
            if hash_1.digest() == hash_3.digest() and hash_2.digest() == hash_4.digest():
                print("OK")
                break

            wait(10)
    except KeyboardInterrupt as e:
        print(e)


if __name__ == '__main__':
    main()
