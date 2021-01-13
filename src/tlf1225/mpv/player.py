"""
This file is implemented with mpv.
"""
# from argparse import ArgumentParser
from code import interact
from ctypes import windll
# from getopt import getopt
from io import StringIO
from os import environ, pathsep, scandir, sep
from os.path import isdir
from re import search
from sys import argv, path, stderr
from time import sleep
from urllib.request import urlopen
from xml.etree.ElementTree import fromstring

try:
    path_list = environ["PATH"].split(pathsep)
    for act_dir in path:
        if isdir(act_dir):
            for working in scandir(act_dir):
                name = getattr(working, "name")
                if "ffmpeg-latest" in name:
                    path_list.insert(-1, f"{name}{sep}bin")
                # noinspection SpellCheckingInspection
                if "libmpv" in name:
                    path_list.insert(-1, name)

    environ["PATH"] = pathsep.join(sorted(set(path_list), key=path_list.index))
    from mpv import MPV
except (OSError, NameError, ImportError) as fail:
    print(fail, file=stderr)


def update_check():
    """
    For Windows 10 x64 LibMPV and YoutubeDL

    :returns: down_youtube_dl, down_mpv
    :rtype: tuple
    """

    with urlopen("https://github.com/ytdl-org/youtube-dl/releases.atom") as m:
        youtube_dl = fromstring(m.read())
    down_youtube_dl = "https://github.com/ytdl-org/youtube-dl/releases/download/" + \
                      search(r"\d{4}\.\d{2}\.\d{2}(?:\.\d)?", youtube_dl[5][3].text).group() + "/youtube-dl.exe"
    with urlopen("https://sourceforge.net/projects/mpv-player-windows/rss?path=/libmpv") as y:
        lib_mpv = fromstring(y.read())
    down_mpv = lib_mpv[0][6][1].text
    return down_youtube_dl, down_mpv


# noinspection SpellCheckingInspection
def setup():
    """
    setup player with mpv

    :returns: player, loop, event_handler, log
    :rtype: tuple
    """

    event_handler = []
    log = StringIO()

    # noinspection SpellCheckingInspection
    def log_mpv(loglevel, component, message) -> None:
        """
        Logging with Buffer

        :param loglevel: LogLevel
        :param component: Component
        :param message: Message
        :return: None
        """
        nonlocal log

        log.write(f"[{loglevel}] {component}: {message}\n")
        if log.tell() > 16384:
            log.seek(0)
            print(pathsep.join(set(log.readlines())), file=stderr)
            log.truncate(0)
            log.seek(0)

    player = MPV(loglevel="warn", log_handler=log_mpv, ytdl=True, input_default_bindings=True, input_vo_keyboard=True, input_media_keys=True,
                 osc=True, vo="gpu,direct3d,sdl", ao="wasapi,openal,sdl", hwdec="auto-copy-safe", gpu_api="auto", loop_playlist="inf", volume_max=100,
                 shuffle=True, config_dir=path[0], input_ipc_server=r"\\.\pipe\tlf1225", geometry="1280x720", autofit="1280x720",
                 ytdl_format="bestvideo+bestaudio/best", ytdl_raw_options="no-cache-dir=",
                 af="@default:lavfi=[dynaudnorm=b=1:c=1:g=11:r=1.0],asoftclip=type=tanh",
                 vf="@default:!lavfi=[fade=in:0:60,pad=0:ih+80:-1:-1:0x008fbf:0:16/9]")

    @player.event_callback("file-loaded")
    def test_handler(_):
        """
        Console Title Changes when start file.

        :return: None
        """

        windll.kernel32.SetConsoleTitleW(player.media_title)

    event_handler.append(test_handler)

    @player.property_observer("estimated-frame-count")
    def test2_handler(_, *arg):
        if all(arg):
            player.command("vf", "toggle", f"@temp:lavfi=[fade=out:{arg[0] - 60}:60]")
        else:
            player.command("vf", "remove", "@temp")

    event_handler.append(test2_handler)

    # noinspection SpellCheckingInspection
    def loop(url=None):
        """
        Loop with data
        :param url:
        :return: None
        """

        nonlocal player, event_handler, log, log_mpv
        if not url:
            return

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

        # noinspection SpellCheckingInspection
        def start(de=False, to=False, bind=False, prog=False, osc=False):
            """
            Simple Start

            :param de: Default Playlist
            :param to: Touhou Playlist
            :param bind: Key Binding list
            :param prog: Progress Bar
            :param osc: OSC Configure
            :return None
            """

            if de:
                player.play(url)
                sleep(3)

            if to:
                for pid in playlist:
                    player.playlist_append(pid)
                player.playlist_shuffle()
                player.playlist_pos = 0

            if bind:
                for x in player.input_bindings:
                    for i, j in x.items():
                        print(f"{i}: {j}", file=stderr)

            if prog:
                player.command("osd-bar", "show-progress")
                player.script_message_to("stats", "display-stats")
                # player.script_message_to("stats", "display-stats-toggle")
                # player.command("cycle-values", "osd-level", 3, 1)
                print(player.time_pos, file=stderr)

            if osc:
                player.osd_duration = 3000
                player.script_opts = "osc-hidetimeout=3000,osc-fadeduration=1000,osc-visibility=always"
                player.cycle("input-default-bindings")
                player.cycle("input-vo-keyboard")

        # noinspection PyUnusedReferences, SpellCheckingInspection
        def reader(prompt=""):
            # opts, other = getopt(argv, "a:m:t", ["arg=", "mpv=", "toggle"])

            # self.parser = ArgumentParser(prog="mpv", description="mpv parser")
            # self.parser.add_argument("type", help="execute type")
            return input(prompt)

        while not player.core_shutdown:
            loc = locals().copy()
            glo = globals().copy()
            loc.update(glo)
            try:
                interact(banner="Interpreter", readfunc=reader, local=loc, exitmsg="Continue")
            except SystemExit as e:
                if e.code is not None:
                    break
                else:
                    player.wait_until_paused()
            except Exception as e:
                print(e, file=stderr)
            del loc, glo

    return player, loop, event_handler, log


# noinspection SpellCheckingInspection
def main(url="ytdl://PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr"):
    """
    play with setup

    :param url: Play URI
    :return: None
    """
    player, loop, event_handler, _ = setup()
    if not isinstance(player, MPV) or not callable(loop) or not isinstance(event_handler, list):
        return
    sleep(1)
    loop(url)
    for x in event_handler:
        for func in [z for z in [getattr(x, y) for y in dir(x) if y.startswith("un")] if callable(z)]:
            func()
            print(f"Unregister: {func}", file=stderr)

    event_handler.clear()
    player.quit()
    player.terminate()
    del player, loop, event_handler


if __name__ == '__main__':
    with open(__file__) as file:
        print(file.read(), file=stderr)
    if len(argv) > 1:
        main(argv[1])
    else:
        main()
