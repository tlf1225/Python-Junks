from code import interact
from ctypes import c_void_p, c_char_p, c_int, c_int64, c_uint64, sizeof
from threading import Thread

from back_fork import search_background
from remake import *


# noinspection SpellCheckingInspection
def main():
    mpv_handle = create()

    set_option_string(mpv_handle, b"input-vo-keyboard", b"yes")
    set_option_string(mpv_handle, b"input-default-bindings", b"yes")
    set_option_string(mpv_handle, b"input-media-keys", b"yes")
    set_option_string(mpv_handle, b"osc", b"yes")
    set_option_string(mpv_handle, b"ytdl-raw-options", b"no-cache-dir=")
    set_option_string(mpv_handle, b"shuffle", b"yes")
    set_option_string(mpv_handle, b"wid", str(search_background()[1][6]).encode())
    # set_option_string(mpv_handle, b"audio-display", b"yes")

    initialize(mpv_handle)

    ho_n = client_name(mpv_handle)
    ho_i = client_id(mpv_handle)

    mpv_client_handle = create_client(mpv_handle, b"Worker")

    cl_n = client_name(mpv_client_handle)
    cl_i = client_id(mpv_client_handle)

    print(ho_n, cl_n)
    print(ho_i, cl_i)

    test = (c_char_p * 2)(b"loadfile", b"ytdl://PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr")

    command(mpv_handle, test)

    flag = 0

    def check_shutdown():
        nonlocal flag
        while not flag:
            off = ad = wait_event(mpv_client_handle, 3)
            x = c_int.from_address(off)
            off += sizeof(c_int)
            y = c_int.from_address(off)
            off += sizeof(c_int)
            z = c_int64.from_address(off)
            off += sizeof(c_uint64)
            a = c_void_p.from_address(off)
            if x.value != 0:
                print(ad, off, x.value, y.value, z.value, a.value)
            elif x.value == 1:
                break

    th = Thread(target=check_shutdown)

    th.setDaemon(True)

    th.start()

    while th.is_alive():
        g = globals().copy()
        g.update(locals().copy())
        try:
            interact(banner="Mpv Player", local=g, exitmsg="Exit")
        except SystemExit as ex:
            if ex.code:
                flag = ex.code
        except Exception as e:
            print(e)
        if flag:
            break
        del g
    else:
        flag = 10

    command(mpv_handle, (c_char_p * 1)(b"quit"))

    th.join(3)

    destroy(mpv_client_handle)

    terminate_destroy(mpv_handle)


if __name__ == '__main__':
    main()
