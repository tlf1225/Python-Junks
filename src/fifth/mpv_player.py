from code import interact as console
from os import environ, pathsep
from sys import stderr
from time import sleep

if "PYTHONPATH" in environ:
    environ["PATH"] = f"{environ.get('PYTHONPATH').split(pathsep)[0] or ''}\\lib{pathsep}{environ.get('PATH') or ''}"

from mpv import MPV


class Player:

    def __init__(self) -> None:
        super().__init__()
        self.flag = True

        def log_mpv(loglevel, component, message):
            print(f"[{loglevel}] {component}: {message}")

        self.player = MPV(loglevel="warn", log_handler=log_mpv, ytdl=True, input_default_bindings=True, input_vo_keyboard=True, osc=True)

        @self.player.event_callback("end-file")
        def event_handler(event):
            if event["event"]["reason"] == 3:
                self.flag = False

        self.event_handler = event_handler

    def setup(self) -> None:
        self.player["vo"] = "gpu"
        self.player.loop_playlist = "inf"
        self.player.geometry = "1280x720"
        self.player.autofit = "1280x720"

    def play_mpv(self, url) -> None:
        self.player.play(url)
        self.player.shuffle = True
        sleep(5)

    def wait_loop(self) -> None:
        while self.flag:
            # noinspection
            try:
                console(banner="Interpreter", local=locals().update(globals()), exitmsg="Continue")
            except SystemExit as e:
                print(f"Exit: {e.code}")
                if e.code is not None and e.code != 0:
                    self.flag = False
            except Exception as e:
                print(e, file=stderr)
            except:
                print("Unknown Error", file=stderr)
            finally:
                self.player.wait_for_playback()

    def stop_mpv(self) -> None:
        self.event_handler.unregister_mpv_events()
        self.player.quit()
        self.player.terminate()
        sleep(3)

    def __del__(self) -> None:
        del self.player
        del self.event_handler


if __name__ == '__main__':
    ax = Player()
    ax.play_mpv("ytdl://PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr")
    sleep(0.5)
    ax.player.playlist_pos = 33
    ax.wait_loop()
    sleep(1)
    ax.stop_mpv()
    del ax
