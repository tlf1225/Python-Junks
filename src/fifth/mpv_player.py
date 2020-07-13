def update_check():
    """
    For Windows 10 x64 LibMPV and YoutubeDL

    :return: LibMPV and YoutubeDL Download URL
    """

    from re import search
    from urllib.request import urlopen
    from xml.etree.ElementTree import fromstring

    with urlopen("https://github.com/ytdl-org/youtube-dl/releases.atom") as m:
        ytdl = fromstring(m.read())
    down_ytdl = "https://github.com/ytdl-org/youtube-dl/releases/download/" + \
                search(r"\d{4}\.\d{2}\.\d{2}(?:\.\d)?", ytdl[5][3].text).group() + "/youtube-dl.exe"
    with urlopen("https://sourceforge.net/projects/mpv-player-windows/rss?path=/libmpv") as y:
        libmpv = fromstring(y.read())
    down_mpv = libmpv[0][6][1].text
    return down_ytdl, down_mpv


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
              "mfZVElthNHA", "e3yq5UBR0hQ", "I42W9RyGvF4", "ZRWq2JFOSXw", "EHY4GTg1wpM"]:
        play.player.playlist_append(f"ytdl://{t}")


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

        self.flag = True
        self.log = StringIO()
        self.player = MPV(loglevel="warn", log_handler=self.log_mpv, ytdl=True, input_default_bindings=True, input_vo_keyboard=True, osc=True)

        @self.player.event_callback("end-file")
        def event_handler(event):
            """
            Event Handler

            :param event: Callback Event
            :return: None
            """

            if event["event"]["reason"] == 3:
                self.flag = False

        self.event_handler = event_handler
        self.setup()

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

    def setup(self) -> None:
        """
        Construtor with Initialize

        :return: None
        """

        self.player["vo"] = "gpu,direct3d,sdl"
        self.player["ao"] = "wasapi,openal,sdl"
        self.player.hwdec = "auto-copy-safe"
        self.player.loop_playlist = "inf"
        self.player.geometry = self.player.autofit = "1280x720"
        self.player.af = "lavfi=[dynaudnorm=g=31:c=1],asoftclip=type=sin"
        # self.player.playlist_pos = 33
        # add_playlist(ax)
        # self.player.command("playlist_shuffle")
        # self.player.command("osd-bar", "show-progress")
        # self.player.media_keys = True
        # self.player.osd_duration = 5000
        # self.player.script_opts = "osc-hidetimeout=8000,osc-fadeduration=1000,osc-visibility=always"
        # self.player.cycle("pause")
        # self.player.input_bindings key binding list
        # self.player.time_pos playback time

    def play_mpv(self, url) -> None:
        """
        Play with url

        :param url: Play URL
        :return: None
        """

        self.player.shuffle = True
        self.player.play(url)

    def wait_loop(self) -> None:
        """
        Console Interpreter

        :return: None
        """

        from code import interact
        from sys import stderr
        while self.flag:
            try:
                gg = globals().copy()
                ll = locals().copy()
                gg.update(ll)
                interact(banner="Interpreter", local=gg, exitmsg="Continue")
                del gg, ll
            except SystemExit as e:
                if e.code is not None and e.code != 0:
                    if not self.player.playback_abort and not self.player.pause:
                        self.player.wait_for_playback()
                    self.flag = False
            except Exception as e:
                print(e, file=stderr)

    def stop_mpv(self) -> None:
        """
        Stop and Terminate MPV Player

        :return: None
        """

        self.event_handler.unregister_mpv_events()
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

        if hasattr(self, "flag"):
            if self.flag:
                self.stop_mpv()
            del self.flag
        if hasattr(self, "player"):
            del self.player
        if hasattr(self, "event_handler"):
            del self.event_handler
        if hasattr(self, "log"):
            del self.log


def load_with_ffmpeg(p=Player(), url="https://www.youtube.com/watch?v=YoPx9EhxR0g"):
    @p.player.python_stream("abcd")
    def reader():
        """
        Reading MPV

        :return:
        """

        import ffmpeg

        i = p.ytdl_info(url=url)
        if not i:
            return
        
        for j in i:
            nonlocal process
            video = ffmpeg.input(j["137"], fflags="discardcorrupt")
            audio = ffmpeg.input(j["140"], fflags="discardcorrupt")
            process = ffmpeg.output(video, audio, "pipe:", codec="copy", format="hls"). \
                global_args("-hide_banner", "-loglevel", "warning"). \
                run_async(pipe_stdout=True)
            buf = process.stdout
            while True:
                temp = buf.read(1024)
                if not temp:
                    break
                yield temp
            del video, audio, buf

    process = None
    p.play_mpv("python://abcd")
    p.wait_loop()
    if hasattr(process, "terminate"):
        process.terminate()
        print("FFmpeg Terminate")
    p.stop_mpv()


def main():
    ax = Player()
    if hasattr(ax, "flag") and ax.flag:
        ax.play_mpv("ytdl://PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr")
        sleep(3)
        ax.wait_loop()
        ax.stop_mpv()
        sleep(1)
    del ax


if __name__ == '__main__':
    from os import environ, pathsep, sep
    from time import sleep

    if "PYTHONPATH" in environ:
        environ["PATH"] = pathsep.join(
            [f"{environ['PYTHONPATH'].split(pathsep)[0]}{sep}lib", "D:/ffmpeg-20200628-4cfcfb3-win64-shared/bin", environ['PATH']])
    with open(__file__) as file:
        print(file.read())
    main()
