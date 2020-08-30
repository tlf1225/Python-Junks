def update_check():
    """
    For Windows 10 x64 LibMPV and YoutubeDL

    :return: LibMPV and YoutubeDL Download URL
    """

    from re import search
    from urllib.request import urlopen
    from xml.etree.ElementTree import fromstring

    with urlopen("https://github.com/ytdl-org/youtube-dl/releases.atom") as m:
        youtube_dl = fromstring(m.read())
    down_youtube_dl = "https://github.com/ytdl-org/youtube-dl/releases/download/" + \
                      search(r"\d{4}\.\d{2}\.\d{2}(?:\.\d)?", youtube_dl[5][3].text).group() + "/youtube-dl.exe"
    with urlopen("https://sourceforge.net/projects/mpv-player-windows/rss?path=/libmpv") as y:
        lib_mpv = fromstring(y.read())
    down_mpv = lib_mpv[0][6][1].text
    return down_youtube_dl, down_mpv


# noinspection SpellCheckingInspection
def add_playlist(play):
    """
    Player Class Execute Function Replace

    :param play: Player Class
    :return: None
    """
    if not isinstance(play, Player) or not hasattr(play, "player"):
        return

    for t in ["7kHDRCO43iw", "thDKz6QQtQk", "fZLptuqF9pk", "Oiud3DLGloA", "v0jb3Ld8bF8",
              "Xuf2Kt2CfkQ", "xoNDIBcNI-I", "sNuNR8v9MLU", "oMr0y0hZ2HA", "aKtHNlP0_zo",
              "OjYskFbYJTI", "9m3qeiAgZvA", "BVGUA5vLsl8", "Rf9ppDaIxAI", "QRcagfSTRE0",
              "mfZVElthNHA", "e3yq5UBR0hQ", "I42W9RyGvF4", "ZRWq2JFOSXw", "EHY4GTg1wpM",
              "6G5PS8alMuM", "oejeamt3akY", "B5nzIG1B45g"]:
        play.player.playlist_append(f"ytdl://{t}")


# noinspection SpellCheckingInspection
class Player:
    """
    MPV Player Wrapper

    Testing
    """

    def __init__(self) -> None:
        """
        Constructor
        """

        from sys import stderr
        from io import StringIO
        try:
            from mpv import MPV
        except (OSError, ImportError) as e:
            print("Couldn't Initialize MPV", file=stderr)
            print(e, file=stderr)
            return

        self.log = StringIO()
        self.player = MPV(loglevel="warn", log_handler=self.log_mpv, ytdl=True, input_default_bindings=True, input_vo_keyboard=True, osc=True)

        self.event_handler = []

        self.__setup()

    def log_mpv(self, loglevel, component, message) -> None:
        """
        Logging with Buffer

        :param loglevel: LogLevel
        :param component: Component
        :param message: Message
        :return: None
        """

        self.log.write(f"[{loglevel}] {component}: {message}\n")
        if self.log.tell() > 16384:
            self.log.seek(0)
            print("".join(set(self.log.readlines())))
            self.log.truncate(0)
            self.log.seek(0)

    def __setup(self) -> None:
        """
        Construtor with Initialize

        :return: None
        """

        self.player["vo"] = "gpu,direct3d,sdl"
        self.player["ao"] = "wasapi,openal,sdl"
        self.player.hwdec = "auto-copy-safe"
        self.player.loop_playlist = "inf"
        self.player.geometry = self.player.autofit = "1280x720"
        self.player.af = "lavfi=[dynaudnorm=b=1:c=1:r=0.11],asoftclip=type=atan"
        self.player.vf = "lavfi=[fade=in:0:60]"
        self.player.input_media_keys = True
        self.player.ytdl_raw_options = "no-cache="
        # self.player.playlist_pos = 33
        # self.player.command("osd-bar", "show-progress")
        # self.player.osd_duration = 5000
        # self.player.script_opts = "osc-hidetimeout=8000,osc-fadeduration=1000,osc-visibility=always"
        # self.player.cycle("pause")
        # self.player.input_bindings # key binding list
        # self.player.time_pos # playback time
        # add_playlist(ax)

        """
        from getopt import getopt
        opts, other = getopt(argv, "a:m:t", ["arg=", "mpv=", "toggle"])
        
        from argparse import ArgumentParser
        self.parser = ArgumentParser(prog="mpv", description="mpv parser")
        self.parser.add_argument("type", help="execute type")
            
        @self.player.event_callback("start-file")
        def test_handler(_):
            from ctypes import windll
            windll.kernel32.SetConsoleTitleW(self.player.media_title)
        """

    def play_mpv(self, url) -> None:
        """
        Play with url

        :param url: Play URL
        :return: None
        """

        self.player.shuffle = True
        self.player.play(url)
        self.player.playlist_shuffle()

    def reader(self, prompt=""):
        """
        data = input(prompt)
        if data.startswith("/"):
            parser = self.parser.parse_args(data[1::].split(" "))
            if parser[""]:
                pass
            parsed = data[1::].split(" ")
            if len(parsed) > 2:
                cmd, mot, other = parsed[0], parsed[1], parsed[2::]
                if cmd == "mpv":
                    if mot == "set":
                        return f"self.player.{other[0]} = {other[1]}"
                    elif mot == "get":
                        return f"self.player.{other[0]}"
                    elif mot == "call":
                        return f"self.player.{other[0]}({','.join(other[1::])})"
            return ""
        else:
            return data
        """
        self.player.command("loadfile")
        return input(prompt)

    def wait_loop(self) -> None:
        """
        Console Interpreter

        :return: None
        """

        from code import interact
        from sys import stderr
        while not self.player.core_shutdown:
            loc = locals().copy()
            glo = globals().copy()
            glo.update(loc)
            try:
                interact(banner="Interpreter", readfunc=self.reader, local=glo, exitmsg="Continue")
            except SystemExit as e:
                if e.code is not None and e.code != 0:
                    break
                else:
                    self.player.wait_until_paused()
            except Exception as e:
                print(e, file=stderr)
            del loc, glo

    def stop_mpv(self) -> None:
        """
        Stop and Terminate MPV Player

        :return: None
        """
        for x in self.event_handler:
            x.unregister_mpv_events()
        self.player.quit()
        self.player.terminate()

    @staticmethod
    def ytdl_info(url="https://www.youtube.com/playlist?list=PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr", ffloc="D:/") -> list:
        """
        YoutubeDL Information Extractor

        :param url: Youtube URL
        :param ffloc: FFmpeg Location
        :return: Format Requests
        """

        from youtube_dl import YoutubeDL

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

    def __del__(self) -> None:
        """
        Deconstructor

        :return: None
        """

        if hasattr(self, "player"):
            if not self.player.core_shutdown:
                self.stop_mpv()
            del self.player
        if hasattr(self, "event_handler"):
            del self.event_handler
        if hasattr(self, "log"):
            self.log.close()
            del self.log


# noinspection SpellCheckingInspection
def load_with_ffmpeg(p=Player(), url="https://www.youtube.com/watch?v=YoPx9EhxR0g"):
    # noinspection SpellCheckingInspection
    @p.player.python_stream("abcd")
    def reader():
        """
        Reading MPV

        :return:
        """

        import ffmpeg

        information = p.ytdl_info(url=url)
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
    p.play_mpv("python://abcd")
    p.wait_loop()
    if hasattr(process, "terminate"):
        process.terminate()
        print("FFmpeg Terminate")
    p.stop_mpv()


# noinspection SpellCheckingInspection
def main():
    ax = Player()
    if hasattr(ax, "player"):
        from time import sleep
        ax.play_mpv("ytdl://PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr")
        sleep(3)
        ax.wait_loop()
        ax.stop_mpv()
        sleep(1)
    del ax


if __name__ == '__main__':
    from os import scandir, environ, pathsep, add_dll_directory

    with open(__file__) as file:
        print(file.read())

    for i in scandir():
        if "ffmpeg" in i.name:
            environ["PATH"] += pathsep + i.path

    with add_dll_directory("D:/Depends/mpv") as dll:
        environ["PATH"] += pathsep + dll.path
        main()
