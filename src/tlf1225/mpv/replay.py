from code import interact
from ctypes import c_void_p, c_char_p, c_int, c_int64, c_uint64, sizeof
from threading import Thread

from .back_fork import search_background
from .remake import *


# noinspection SpellCheckingInspection
def main():
    mpv_handle = create()

    request_log_messages(mpv_handle, b"warn")
    set_option_string(mpv_handle, b"input-vo-keyboard", b"yes")
    set_option_string(mpv_handle, b"input-default-bindings", b"yes")
    set_option_string(mpv_handle, b"input-media-keys", b"yes")
    set_option_string(mpv_handle, b"osc", b"yes")
    set_option_string(mpv_handle, b"shuffle", b"yes")
    set_option_string(mpv_handle, b"vo", b"gpu,direct3d,sdl")
    set_option_string(mpv_handle, b"ao", b"wasapi,openal,sdl")
    set_option_string(mpv_handle, b"hwdec", b"auto-copy-safe")
    set_option_string(mpv_handle, b"gpu-api", b"auto")
    set_option_string(mpv_handle, b"loop-playlist", b"inf")
    set_option_string(mpv_handle, b"volume-max", b"100")
    set_option_string(mpv_handle, b"input-ipc-server", rb"\\.\pipe\tlf1225")
    set_option_string(mpv_handle, b"autofit", b"1280x720")
    set_option_string(mpv_handle, b"gemetry", b"1280x720")
    set_option_string(mpv_handle, b"ytdl-format", b"bestvideo+bestaudio/best")
    set_option_string(mpv_handle, b"ytdl-raw-options", b"no-cache-dir=")
    set_option_string(mpv_handle, b"wid", str(search_background()[1][6]).encode())
    set_option_string(mpv_handle, b"af", b"@default:lavfi=[dynaudnorm=b=1:c=1:g=11:r=1.0],asoftclip=type=tanh")
    set_option_string(mpv_handle, b"vf", b"@default:lavfi=[fade=in:0:60,pad=0:ih+80:-1:-1:0x008fbf:0:16/9]")

    load_config_file(mpv_handle, b"mpv.conf")

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

    command(mpv_handle, c_char_p(b"playlist-shuffle"))

    """
    from ctypes import windll, byref
    from json import loads
    
    command(mpv_handle, (c_char_p * 2)(b"keypress", b"i"))
    command(mpv_handle, c_char_p(b"playlist-next"))
    command(mpv_handle, c_char_p(b"playlist-shuffle"))
    command(mpv_handle, (c_char_p * 2)(b"cycle", "pause"))
    
    x = c_int64()
    get_property(mpv_handle, b"duration", 4, byref(x))
    set_property(mpv_handle, b"playlist-pos", 4, byref(x))
    set_property(mpv_handle, b"playlist-pos", 4, byref(c_int(0)))
    
    y = loads(get_property_string(mpv_handle, b"playlist"))

    get_property_string(mpv_handle, b"wid")    
    set_property_string(mpv_handle, b"loop", b"inf")
    set_property_string(mpv_handle, b"speed", b"1.25")
    set_property_string(mpv_handle, b"playlist-pos", b"22")
    
    for i in playlist:
        command(mpv_handle, (c_char_p * 4)(b"loadfile", i.encode(), b"append"))
    
    command_string(mpv_handle, b"seek 120")
    command_string(mpv_handle, b"keypress i")
    command_string(mpv_handle, b"playlist-next")
    
    windll.kernel32.SetConsoleTitleA(get_property_string(mpv_handle, b"media-title"))
    
    frame = c_int64()
    get_property(mpv_handle, b"estimated-frame-count", 4, byref(frame))
    command(mpv_handle, (c_char_p * 3)(b"vf", b"toggle", f"@temp:lavfi=[fade=out:{frame.value}:60]".encode()))
    command(mpv_handle, (c_char_p * 3)(b"vf", b"remove", b"@temp"))
    """

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
