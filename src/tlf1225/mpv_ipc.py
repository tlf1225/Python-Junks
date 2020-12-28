from code import interact
from json import loads, dumps
from random import randint

# noinspection PyUnresolvedReferences
from pywintypes import error
from win32file import CreateFile, WriteFile, ReadFile, CloseHandle, GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from win32pipe import SetNamedPipeHandleState, PIPE_READMODE_MESSAGE, PIPE_NOWAIT


def setup(pipe=r"\\.\pipe\tlf1225"):
    handle = CreateFile(pipe, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, None)
    res = SetNamedPipeHandleState(handle, PIPE_READMODE_MESSAGE | PIPE_NOWAIT, None, None)
    return -1 if res else handle


def request(com: list):
    js = {"command": com, "request_id": randint(1, 4096), "async": True}
    print(dumps(js, sort_keys=True, indent=4))
    return (dumps(js, sort_keys=True) + '\n').encode()


def response(handle):
    try:
        while True:
            try:
                res = ReadFile(handle, 128)
                print(dumps(loads(res[1].decode()), sort_keys=True, indent=4))
            except error:
                pass
    except KeyboardInterrupt:
        pass


def main():
    handle = setup()

    # test message
    test = request(["set_property", "volume", 100])
    WriteFile(handle, test)

    response(handle)

    var = globals()
    var.update(locals())
    try:
        interact(banner="mpv ipc", local=var, exitmsg="exit")
    except Exception as e:
        print(e)

    CloseHandle(handle)


if __name__ == '__main__':
    main()
