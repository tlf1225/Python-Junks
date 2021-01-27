from code import interact
from ctypes import c_char_p, c_int64, windll
from random import randint
from sys import stderr
from threading import Thread
from time import sleep

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
    set_option_string(mpv_handle, b"audio-display", b"yes")
    # set_option_string(mpv_handle, b"idle", b"yes")
    # set_option_string(mpv_handle, b"input-terminal", b"no")
    # set_option_string(mpv_handle, b"terminal", b"no")

    load_config_file(mpv_handle, b"mpv.conf")

    initialize(mpv_handle)

    ho_n = client_name(mpv_handle)
    ho_i = client_id(mpv_handle)

    mpv_client_handle = create_client(mpv_handle, b"Worker")

    request_log_messages(mpv_client_handle, b"info")

    cl_n = client_name(mpv_client_handle)
    cl_i = client_id(mpv_client_handle)

    print(ho_n.decode(), cl_n.decode(), file=stderr)
    print(ho_i, cl_i, file=stderr)

    test = (c_char_p * 4)(b"loadfile", b"ytdl://PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr")

    command(mpv_client_handle, test)

    """
    from json import loads
    
    command(mpv_client_handle, (c_char_p * 2)(b"keypress", b"i"))
    
    x = c_int64()
    get_property(mpv_client_handle, b"duration", 4, byref(x))
    set_property(mpv_client_handle, b"playlist-pos", 4, byref(x))
    
    y = loads(get_property_string(mpv_client_handle, b"playlist"))

    get_property_string(mpv_client_handle, b"wid")    
    set_property_string(mpv_client_handle, b"loop", b"inf")
    set_property_string(mpv_client_handle, b"speed", b"1.25")
    set_property_string(mpv_client_handle, b"playlist-pos", b"22")
    
    command_string(mpv_client_handle, b"seek 120")
    command_string(mpv_client_handle, b"keypress i")
    command_string(mpv_client_handle, b"playlist-next")
    
    frame = c_int64()
    get_property(mpv_client_handle, b"estimated-frame-count", 4, byref(frame))
    """

    event_user_id = randint(0, 32768)

    observe_property(mpv_client_handle, event_user_id, b"estimated-frame-count", 4)
    observe_property(mpv_client_handle, event_user_id, b"media-title", 1)

    flag = 0

    # noinspection SpellCheckingInspection
    def check_shutdown():
        nonlocal flag
        while not flag:
            try:
                evt = wait_event(mpv_client_handle, 10)
                if not evt:
                    continue
                event_id, error_code, reply_userdata, data = \
                    getattr(evt.contents, "event_id"), getattr(evt.contents, "error"), \
                    getattr(evt.contents, "reply_userdata"), getattr(evt.contents, "data")
                if event_id == 0:
                    continue
                elif event_id == 1:
                    print("Mpv Shutdown", file=stderr)
                    break
                elif event_id == 2:
                    log = MPVEventLogMessage.from_address(data)
                    prefix, level, text, log_level = getattr(log, "prefix"), getattr(log, "level"), getattr(log, "text"), getattr(log, "log_level")
                    print(f"[{prefix.decode()}] {level.decode()}({log_level}): {text.decode()}", file=stderr, end="")
                elif event_id == 3:
                    pass
                elif event_id == 22:
                    if reply_userdata == event_user_id:
                        pro = MPVEventProperty.from_address(data)
                        name, info, work = getattr(pro, "name"), getattr(pro, "format"), getattr(pro, "data")
                        if name == b"estimated-frame-count" and info == 4:
                            frame = c_int64.from_address(work)
                            if not frame:
                                continue
                            print(f"Name: {name.decode()}, Frame: {frame.value}", file=stderr)
                            if frame.value > 0:
                                command(mpv_client_handle, (c_char_p * 4)(b"vf", b"remove", b"@temp"))
                                command(mpv_client_handle, (c_char_p * 4)(b"vf", b"toggle", f"@temp:lavfi=[fade=out:{frame.value - 60}:60]".encode()))
                        elif name == b"media-title" and info == 1:
                            media = c_char_p.from_address(work)
                            windll.kernel32.SetConsoleTitleW(media.value.decode())
                else:
                    print(f"Event ID: {event_id}, Error Code: {error_code}, UserData: {reply_userdata}, Additional Data: {data}", file=stderr)
            except Exception as h:
                print(h, file=stderr)

    th = Thread(target=check_shutdown)

    th.setDaemon(True)

    th.start()

    sleep(5)

    command(mpv_client_handle, c_char_p(b"playlist-shuffle"))

    set_property_string(mpv_client_handle, b"playlist-pos", b"0")

    playlist = [f"ytdl://{yt}" for yt in
                ('0mxpCgVE_4c', '14C7d1LO8bU', '340ZzONBHhQ', '4mbtk45j6rc', '5aFDb2aUI-o',
                 '5gzJ7uk74UA', '6G5PS8alMuM', '6gBbpbRSRiY', '6it-y7zyt8s', '7U1qiS7B8Nk',
                 '7kHDRCO43iw', '9avbb6e9eBw', '9c0gAfV7M_4', '9m3qeiAgZvA', 'B1g1djVfweY',
                 'B5nzIG1B45g', 'BVGUA5vLsl8', 'BaB0e3O08I4', 'BahP4Pixv5w', 'E46l605KSlg',
                 'EHY4GTg1wpM', 'FnVLrIV2Ook', 'I42W9RyGvF4', 'IHCrqdLTWKo', 'JDocJA7hDKY',
                 'K0lw3qXBQ0g', 'Lk7t7m8uXgg', 'NgCGAIKdcYI', 'Oiud3DLGloA', 'OjYskFbYJTI',
                 'PhbB4eGV-fI', 'QRcagfSTRE0', 'Q_as_NVMfB4', 'Rf9ppDaIxAI', 'qU_H0z6fCls',
                 'VLng2Eu1YyQ', 'WcNIJldE7U8', 'Xuf2Kt2CfkQ', 'Ys2p_bXOaAc', 'ZRWq2JFOSXw',
                 'ZojVSmK_3-c', '_W90dohDz1s', '_lRkDv7gelw', 'aKtHNlP0_zo', 'cN5S-fHGhAA',
                 'co-YIaCO1ig', 'cxWJK8VJkoQ', 'e3yq5UBR0hQ', 'ejZan8kKjsY', 'fZLptuqF9pk',
                 'iPNkYAA_f90', 'j33hMzdsq9k', 'jFvB1WleWNU', 'jtH_nLso2Gg', 'jztI5SZ6lEc',
                 'm4zkuc_wU2s', 'mfZVElthNHA', 'oMr0y0hZ2HA', 'oag5Wb93ah0', 'oejeamt3akY',
                 'sLz2CsN0NZU', 'sNuNR8v9MLU', 'thDKz6QQtQk', 'uk2c0qLhOaY', 'v0jb3Ld8bF8',
                 'vaYdSkvJAdU', 'vw-we-8-vwc', 'w-l9a4KggYs', 'xoNDIBcNI-I', 'xxOcLcPrs2w',
                 'yQ3pFBrZqak', 'mg6PCPVUg7I', 'CH9cHp-QM1c', 'lg6RecLKxXU', 'DZgGQboLTm4',
                 'i75oLwv286U', 'ZHUDc38ncAA')] + \
               [f"https://nico.ms/{nc}" for nc in
                ('nm4624881',)] + \
               [f"https://www.bilibili.com/video/{bb}" for bb in
                ('BV1Es41127k8', 'BV1Zs411C7K8', 'BV1ds411C7pL')]

    for i in playlist:
        command(mpv_client_handle, (c_char_p * 4)(b"loadfile", i.encode(), b"append"))

    while th.is_alive():
        g = globals().copy()
        g.update(locals().copy())
        try:
            interact(banner="Mpv Player", local=g, exitmsg="Exit")
        except SystemExit as ex:
            if ex.code:
                flag = ex.code
        except Exception as e:
            print(e, file=stderr)
        if flag:
            break
        del g
    else:
        flag = 10

    command(mpv_client_handle, c_char_p(b"quit"))

    th.join(3)

    destroy(mpv_client_handle)

    terminate_destroy(mpv_handle)


if __name__ == '__main__':
    cw = windll.kernel32.GetConsoleWindow()
    sm = windll.user32.GetSystemMenu(cw, False)
    windll.user32.EnableMenuItem(sm, 0xF060, 3)
    main()
    windll.user32.EnableMenuItem(sm, 0xF060, 0)
