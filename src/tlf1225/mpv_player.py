# noinspection PyUnresolvedReferences
from argparse import ArgumentParser
from ctypes import windll
from io import StringIO
from os import scandir, environ, pathsep
from re import search
# noinspection PyUnresolvedReferences
from sys import argv, stderr
from time import sleep
from urllib.request import urlopen
from xml.etree.ElementTree import fromstring

# noinspection PyUnresolvedReferences
from code import interact
# noinspection PyUnresolvedReferences
from getopt import getopt

try:
    for i in scandir():
        if "ffmpeg" in i.name:
            environ["PATH"] += pathsep + i.path
    environ["PATH"] += pathsep + "D:/Depends/mpv"

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
    if p is None or "player" not in p:
        return

    player = p["player"]

    # noinspection SpellCheckingInspection
    @player.python_stream("abcd")
    def reader():
        """
        Reading MPV

        :return:
        """

        information = ytdl_info(url=url)
        if not information:
            return

        for j in information:
            nonlocal process
            video = ffmpeg.input(j["137"], fflags="discardcorrupt")
            audio = ffmpeg.input(j["140"], fflags="discardcorrupt")
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
        "format": "best",
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
    data = {"log": StringIO(), "event_handler": []}

    # noinspection SpellCheckingInspection
    def log_mpv(loglevel, component, message) -> None:
        """
        Logging with Buffer

        :param loglevel: LogLevel
        :param component: Component
        :param message: Message
        :return: None
        """

        data["log"].write(f"[{loglevel}] {component}: {message}\n")
        if data["log"].tell() > 16384:
            data["log"].seek(0)
            print("".join(set(data["log"].readlines())))
            data["log"].truncate(0)
            data["log"].seek(0)

    data["log_mpv"] = log_mpv
    data["player"] = MPV(loglevel="warn", log_handler=data["log_mpv"], ytdl=True, input_default_bindings=True, input_vo_keyboard=True, osc=True)

    player = data["player"]
    player["vo"] = "gpu,direct3d,sdl"
    player["ao"] = "wasapi,openal,sdl"
    player.hwdec = "auto-copy-safe"
    player.loop_playlist = "inf"
    player.geometry = player.autofit = "1280x720"
    player.af = "lavfi=[dynaudnorm=b=1:c=1:r=0.11],asoftclip=type=atan"
    player.vf = "lavfi=[fade=in:0:60]"
    player.input_media_keys = True
    player.ytdl_raw_options = "no-cache="
    player.shuffle = True

    # player.playlist_pos = 33
    # player.command("osd-bar", "show-progress")
    # player.osd_duration = 5000
    # player.script_opts = "osc-hidetimeout=8000,osc-fadeduration=1000,osc-visibility=always"
    # player.cycle("pause")
    # player.input_bindings # key binding list
    # player.time_pos # playback time
    # add_playlist(player)

    # noinspection PyUnusedReferences
    # opts, other = getopt(argv, "a:m:t", ["arg=", "mpv=", "toggle"])

    # self.parser = ArgumentParser(prog="mpv", description="mpv parser")
    # self.parser.add_argument("type", help="execute type")

    @player.event_callback("start-file")
    def test_handler(_):
        windll.kernel32.SetConsoleTitleW(player.media_title)

    # noinspection SpellCheckingInspection
    def add_playlist():
        """
        Player Class Execute Function Replace

        :return: None
        """

        for t in ["7kHDRCO43iw", "thDKz6QQtQk", "fZLptuqF9pk", "Oiud3DLGloA", "v0jb3Ld8bF8",
                  "Xuf2Kt2CfkQ", "xoNDIBcNI-I", "sNuNR8v9MLU", "oMr0y0hZ2HA", "aKtHNlP0_zo",
                  "OjYskFbYJTI", "9m3qeiAgZvA", "BVGUA5vLsl8", "Rf9ppDaIxAI", "QRcagfSTRE0",
                  "mfZVElthNHA", "e3yq5UBR0hQ", "I42W9RyGvF4", "ZRWq2JFOSXw", "EHY4GTg1wpM",
                  "6G5PS8alMuM", "oejeamt3akY", "B5nzIG1B45g"]:
            data["player"].playlist_append(f"ytdl://{t}")

    data["add_list"] = add_playlist
    return data


# noinspection SpellCheckingInspection
def loop(data, url="ytdl://PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr"):
    player = data["player"]
    player.play(url)
    player.playlist_shuffle()

    def reader(prompt=""):
        return input(prompt)

    while not player.core_shutdown:
        try:
            interact(banner="Interpreter", readfunc=reader, local=locals(), exitmsg="Continue")
        except SystemExit as e:
            if e.code is not None and e.code != 0:
                break
            else:
                player.wait_until_paused()
        except Exception as e:
            print(e, file=stderr)


# noinspection SpellCheckingInspection
def main(url="ytdl://PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr"):
    data = setup()
    player = data["player"], event_handler = data["event_handler"]
    loop(data, url)
    for x in event_handler:
        x.unregister_mpv_events()
    player.quit()
    player.terminate()
    sleep(1)


if __name__ == '__main__':
    with open(__file__) as file:
        print(file.read())
    main()
