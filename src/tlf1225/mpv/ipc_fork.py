from code import interact
from json import loads, dumps
from random import randint


def test(handle, req):
    def request(com: list):
        nonlocal handle
        js = {"command": com, "request_id": randint(1, 4096), "async": True}
        handle.write((dumps(js, sort_keys=True) + '\n').encode())
        return dumps(js, sort_keys=True, indent=4)

    def response():
        nonlocal handle
        buf = handle.readline()
        return dumps(loads(buf.decode()), sort_keys=True, indent=4)

    return request(req), response()


def main():
    with open(r"\\.\pipe\tlf1225", "rb+") as handle:
        def call(ary: list):
            print("\n".join(test(handle, ary)))

        # test message
        call(["set_property", "volume", 100])

        while True:
            var = globals().copy()
            var.update(locals().copy())
            try:
                interact(banner="mpv ipc", local=var, exitmsg="exit")
            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()
