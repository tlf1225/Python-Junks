"""
This file is implemented with mpv.
"""

# noinspection PyUnresolvedReferences
from argparse import ArgumentParser
from ctypes import windll
from io import StringIO
from os import scandir, environ, pathsep, sep
from os.path import isdir
from re import search
# noinspection PyUnresolvedReferences
from sys import argv, path, stderr
from time import sleep
from urllib.request import urlopen
from xml.etree.ElementTree import fromstring

# noinspection PyUnresolvedReferences
from code import interact
# noinspection PyUnresolvedReferences
from getopt import getopt

try:
    path_list = environ["PATH"].split(pathsep)
    # path_list.remove(r"D:\Python\Scripts")
    for i in [k for k in path if isdir(k)]:
        for j in scandir(i):
            if "ffmpeg-latest" in j.name:
                path_list.insert(-1, f"{j.path}{sep}bin")
            # noinspection SpellCheckingInspection
            if "libmpv" in j.name:
                path_list.insert(-1, j.path)
    environ["PATH"] = pathsep.join(sorted(set(path_list), key=path_list.index))
    from mpv import MPV
    from youtube_dl import YoutubeDL
    import ffmpeg
except (OSError, NameError) as fail:
    print(fail, file=stderr)


def update_check():
    """
    For Windows 10 x64 LibMPV and YoutubeDL

    :return: LibMPV and YoutubeDL Download URL
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
def load_with_ffmpeg(p=None, url="https://www.youtube.com/watch?v=YoPx9EhxR0g"):
    """
    mpv load with ffmpeg and youtube-dl

    :param p: predefined dictionary
    :param url: Youtube Link
    :return: No return
    """
    if p is None or "player" not in p:
        return

    player = p.get("player")

    # noinspection SpellCheckingInspection
    @player.python_stream("abcd")
    def reader():
        """
        Reading MPV

        :return: No return
        """

        information = ytdl_info(url=url)
        if not information:
            return

        for format_list in information:
            nonlocal process
            video = ffmpeg.input(format_list["137"], fflags="discardcorrupt")
            audio = ffmpeg.input(format_list["140"], fflags="discardcorrupt")
            process = ffmpeg.output(video, audio, "pipe:", codec="copy", format="hls"). \
                global_args("-hide_banner", "-loglevel", "warning"). \
                run_async(pipe_stdout=True)
            buf = process.stdout
            while True:
                ttt = buf.read(1024)
                if not ttt:
                    break
                yield ttt
            del video, audio, buf

    process = None
    loop = p.get("loop")
    loop(p, "python://abcd")
    if hasattr(process, "terminate"):
        process.terminate()
        print("FFmpeg Terminate")
    player.quit()
    player.terminate()


# noinspection SpellCheckingInspection
def ytdl_info(url="https://www.youtube.com/playlist?list=PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr", ffloc="ffmpeg-latest-win64-shared/bin") -> list:
    """
    YoutubeDL Information Extractor

    :param url: Youtube URL
    :param ffloc: FFmpeg Location
    :return: Format Requests
    """

    information = []
    with YoutubeDL(params={
        "no_cache": True,
        "no_warnings": False,
        "ignoreerrors": True,
        "quiet": True,
        "skip_download": True,
        "simulate": True,
        "format": "bestvideo+bestaudio/best",
        "ffmpeg_location": ffloc
    }) as ytdl:
        result = ytdl.extract_info(url=url, download=False)

        if not result:
            return information
        if "entries" not in result:
            print(result["title"])
            mapping = {}
            for url in sorted(result["formats"], key=lambda x: int(x["format_id"])):
                mapping[url['format_id']] = url['url']
                # print(f"{url['format']} {url['url']}")
            information.append(mapping)
        else:
            for entries in result["entries"]:
                mapping = {}
                print(entries["title"])
                for url in sorted(entries["formats"], key=lambda x: int(x["format_id"])):
                    mapping[url['format_id']] = url['url']
                    # print(f"{url['format']} {url['url']}")
                information.append(mapping)
                print()
    return information


# noinspection SpellCheckingInspection
def setup():
    """
    setup player with mpv

    :return: predefined dictionary
    """
    log = StringIO()
    event_handler = []
    data = {"log": log, "event_handler": event_handler}

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
            print("".join(set(log.readlines())))
            log.truncate(0)
            log.seek(0)

    data["log_mpv"] = log_mpv
    data["player"] = MPV(loglevel="warn", log_handler=log_mpv, ytdl=True, input_default_bindings=True, input_vo_keyboard=True, osc=True)

    player = data.get("player")
    player["vo"] = "gpu,direct3d,sdl"
    player["ao"] = "wasapi,openal,sdl"
    player.hwdec = "auto-copy-safe"
    player.loop_playlist = "inf"
    player.geometry = player.autofit = "1280x720"
    player.af = "lavfi=[dynaudnorm=b=1:c=1:g=11:r=0.1],asoftclip=type=sin"
    player.vf = "lavfi=[fade=in:0:60]"
    player.input_media_keys = True
    player.ytdl_format = "bestvideo+bestaudio/best"
    player.ytdl_raw_options = "no-cache-dir="
    player.shuffle = True

    # player.command("osd-bar", "show-progress")
    # player.osd_duration = 5000
    # player.script_opts = "osc-hidetimeout=8000,osc-fadeduration=1000,osc-visibility=always"
    # player.cycle("pause")
    # player.input_bindings # key binding list
    # player.time_pos # playback time

    # noinspection SpellCheckingInspection
    def loop(url=None):
        """
        Loop with data
        :param url:
        :return: No return
        """
        nonlocal data, player, log, event_handler
        if not url:
            return

        # player.play(url)
        # player.playlist_shuffle()

        def reader(prompt=""):
            return input(prompt)

        while not player.core_shutdown:
            loc = locals().copy()
            glo = globals().copy()
            loc.update(glo)
            try:
                interact(banner="Interpreter", readfunc=reader, local=loc, exitmsg="Continue")
            except SystemExit as e:
                if e.code is not None and e.code != 0:
                    break
                else:
                    player.wait_until_paused()
            except Exception as e:
                print(e, file=stderr)
            del loc, glo

    data["loop"] = loop

    # noinspection SpellCheckingInspection
    def add_list():
        """
        Playlist append

        :return: None
        """
        for yt in ['0mxpCgVE_4c', '14C7d1LO8bU', '340ZzONBHhQ', '4mbtk45j6rc', '5aFDb2aUI-o',
                   '5gzJ7uk74UA', '6G5PS8alMuM', '6gBbpbRSRiY', '6it-y7zyt8s', '7U1qiS7B8Nk',
                   '7kHDRCO43iw', '9avbb6e9eBw', '9c0gAfV7M_4', '9m3qeiAgZvA', 'B1g1djVfweY',
                   'B5nzIG1B45g', 'BVGUA5vLsl8', 'BaB0e3O08I4', 'BahP4Pixv5w', 'E46l605KSlg',
                   'EHY4GTg1wpM', 'FnVLrIV2Ook', 'I42W9RyGvF4', 'IHCrqdLTWKo', 'JDocJA7hDKY',
                   'K0lw3qXBQ0g', 'Lk7t7m8uXgg', 'NgCGAIKdcYI', 'Oiud3DLGloA', 'OjYskFbYJTI',
                   'PhbB4eGV-fI', 'QRcagfSTRE0', 'Q_as_NVMfB4', 'Rf9ppDaIxAI', 'SBlpxAxJkMA',
                   'VLng2Eu1YyQ', 'WcNIJldE7U8', 'Xuf2Kt2CfkQ', 'Ys2p_bXOaAc', 'ZRWq2JFOSXw',
                   'ZojVSmK_3-c', '_W90dohDz1s', '_lRkDv7gelw', 'aKtHNlP0_zo', 'cN5S-fHGhAA',
                   'co-YIaCO1ig', 'cxWJK8VJkoQ', 'e3yq5UBR0hQ', 'ejZan8kKjsY', 'fZLptuqF9pk',
                   'iPNkYAA_f90', 'j33hMzdsq9k', 'jFvB1WleWNU', 'jtH_nLso2Gg', 'jztI5SZ6lEc',
                   'm4zkuc_wU2s', 'mfZVElthNHA', 'oMr0y0hZ2HA', 'oag5Wb93ah0', 'oejeamt3akY',
                   'sLz2CsN0NZU', 'sNuNR8v9MLU', 'thDKz6QQtQk', 'uk2c0qLhOaY', 'v0jb3Ld8bF8',
                   'vaYdSkvJAdU', 'vw-we-8-vwc', 'w-l9a4KggYs', 'xoNDIBcNI-I', 'xxOcLcPrs2w',
                   'yQ3pFBrZqak']:
            player.playlist_append(f"ytdl://{yt}")

        for nc in ['nm4624881']:
            player.playlist_append(f"https://nico.ms/{nc}")

        for bb in ['BV1Es41127k8', 'BV1Zs411C7K8', 'BV1ds411C7pL']:
            player.playlist_append(f"https://www.bilibili.com/video/{bb}")

    data["add_list"] = add_list

    # noinspection PyUnusedReferences
    # opts, other = getopt(argv, "a:m:t", ["arg=", "mpv=", "toggle"])

    # self.parser = ArgumentParser(prog="mpv", description="mpv parser")
    # self.parser.add_argument("type", help="execute type")

    @player.event_callback("start-file")
    def test_handler(_):
        """
        Console Title Changes when start file.
        :param _: No Param
        :return: No return
        """
        windll.kernel32.SetConsoleTitleW(player.media_title)

    event_handler.append(test_handler)

    return data


# noinspection SpellCheckingInspection
def main(url="ytdl://PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr"):
    """
    play with setup

    :param url: Play URI
    :return:
    """
    data = setup()
    player = data.get("player")
    event_handler = data.get("event_handler")
    sleep(1)
    loop = data.get("loop")
    loop(url)
    for x in event_handler:
        if callable(x.unregister_mpv_events):
            x.unregister_mpv_events()
    player.quit()
    player.terminate()


if __name__ == '__main__':
    with open(__file__) as file:
        print(file.read())
    main()
