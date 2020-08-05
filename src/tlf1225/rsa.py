from difflib import restore, ndiff
from math import gcd, floor, sqrt
from random import randrange


def sieve_of_eratosthenes(target):
    if target < 2:
        return [1]
    dest = floor(sqrt(target))
    target_list = list(range(2, target + 1))
    prime_list = []
    while True:
        num_min = min(target_list)
        if num_min >= dest:
            prime_list.extend(target_list)
            break
        prime_list.append(num_min)
        i = 0
        while True:
            if i >= len(target_list):
                break
            elif target_list[i] % num_min == 0:
                target_list.pop(i)
            i += 1
    return prime_list


def is_prime(n, prime):
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    m = floor(sqrt(n))
    for p in prime:
        if n % p == 0:
            return False
        if p > m:
            break
    return True


def lcm(p, q):
    return (p * q) // gcd(p, q)


def generate_keys(p, q):
    e, d = 0, 0
    n = p * q
    ll = lcm(p - 1, q - 1)

    for i in range(2, ll):
        if gcd(i, ll) == 1:
            e = i
            break

    for i in range(2, ll):
        if (e * i) % ll == 1:
            d = i
            break

    return (e, n), (d, n)


def encrypt(plain_text, public_key):
    e, n = public_key
    plain_integers = [ord(char) for char in plain_text]
    encrypted_integers = [pow(i, e, n) for i in plain_integers]
    encrypted_text = ''.join(chr(i) for i in encrypted_integers)

    return encrypted_text


def decrypt(encrypted_text, private_key):
    d, n = private_key
    encrypted_integers = [ord(char) for char in encrypted_text]
    decrypted_integers = [pow(i, d, n) for i in encrypted_integers]
    decrypted_text = ''.join(chr(i) for i in decrypted_integers)

    return decrypted_text


def sanitize(encrypted_text):
    return encrypted_text.encode('utf-8', 'replace').decode('utf-8')


def main():
    prime_list = sieve_of_eratosthenes(1024)
    while True:
        key1 = randrange(2, 1024)
        key2 = randrange(2, 1024)
        if is_prime(key1, prime_list) and is_prime(key2, prime_list):
            public_key, private_key = generate_keys(key1, key2)
            plain_text = 'This text is encrypted by Python.'
            encrypted_text = encrypt(plain_text, public_key)
            decrypted_text = decrypt(encrypted_text, private_key)
            print(f'''
秘密鍵: {public_key}
公開鍵: {private_key}

平文:
「{plain_text}」

暗号文:
「{sanitize(encrypted_text)}」

平文 (復号化後):
「{decrypted_text}」
'''[1:-1])
            break
    with open("../first/diff.txt", encoding="ASCII") as e:
        with open("../first/diff2.txt", encoding="ASCII") as f:
            g = e.readlines()
            h = f.readlines()
            u = ndiff(g, h)
            work = list(u)
            print(''.join(work))
            result = list(restore(work, 2))
            print(''.join(result))


if __name__ == '__main__':
    main()
