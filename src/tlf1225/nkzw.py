# coding: utf-8
from re import compile as recompile
from string import ascii_letters, digits


def main():
    password = input()
    test = recompile(r"(.)\1{2,}")
    dup = True if test.findall(password) else False
    verify = len(password) == len([i for i in password if i in ascii_letters + digits])

    if verify and len(password) >= 6 and not dup:
        print('Valid')
    else:
        print('Invalid')


if __name__ == '__main__':
    main()
