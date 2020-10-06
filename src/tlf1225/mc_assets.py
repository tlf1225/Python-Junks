from code import interact
from getpass import getpass
from json import loads, dumps
from urllib.request import Request, urlopen


def launcher():
    with urlopen("https://launchermeta.mojang.com/mc/game/version_manifest.json") as manifest:
        info = loads(manifest.read())
    with urlopen(info["versions"][0]["url"]) as assets:
        info2 = loads(assets.read())
    print(info2["downloads"]["client"]["url"])
    print(info2["downloads"]["server"]["url"])
    return info, info2


def auth(username: str = "", password: str = ""):
    req = {
        "agent": {
            "name": "Minecraft",
            "version": 1
        },
        "username": input("UserName: ") or username,
        "password": getpass("Password: ") or password
    }

    head = {
        "Content-Type": "application/json"
    }

    # refresh
    with urlopen(Request("https://authserver.mojang.com/authenticate", dumps(req).encode(), head)) as authenticate:
        authorized = loads(authenticate.read())
    return authorized


def ref(authorized: dict):
    req = {
        "accessToken": authorized["accessToken"],
        "clientToken": authorized["clientToken"]
    }

    head = {
        "Content-Type": "application/json"
    }

    # refresh
    with urlopen(Request("https://authserver.mojang.com/refresh", dumps(req).encode(), head)) as refresh:
        authorized = loads(refresh.read())
    return authorized


def sign_out(username: str = "", password: str = ""):
    req = {
        "username": input("UserName: ") or username,
        "password": getpass("Password: ") or password
    }

    head = {
        "Content-Type": "application/json"
    }

    # refresh validate signout
    with urlopen(Request("https://authserver.mojang.com/signout", dumps(req).encode(), head)) as sign:
        print(sign.read())


def valid(authorized: dict):
    req = {
        "accessToken": authorized["accessToken"],
        "clientToken": authorized["clientToken"]
    }

    head = {
        "Content-Type": "application/json"
    }

    with urlopen(Request("https://authserver.mojang.com/validate", dumps(req).encode(), head)) as invalidate:
        print(invalidate.read())


def invalid(authorized: dict):
    req = {
        "accessToken": authorized["accessToken"],
        "clientToken": authorized["clientToken"]
    }

    head = {
        "Content-Type": "application/json"
    }

    with urlopen(Request("https://authserver.mojang.com/invalidate", dumps(req).encode(), head)) as invalidate:
        print(invalidate.read())


if __name__ == '__main__':
    interact(banner="Minecraft", local=locals(), exitmsg="Exit")
