from code import interact
from datetime import datetime, timezone, timedelta
from json import loads, dumps
from urllib.request import urlopen

# noinspection PyUnresolvedReferences
from tlf1225.mpv.player import setup


# noinspection SpellCheckingInspection
class MirrativAPI:

    def __init__(self, identify) -> None:
        super(MirrativAPI, self).__init__()
        self.id = identify

    def load_userprofile(self):
        with urlopen(f"https://www.mirrativ.com/api/user/profile?user_id={self.id}") as lu:
            return loads(lu.read())

    def load_live_history(self, page=1):
        with urlopen(f"https://www.mirrativ.com/api/live/live_history?user_id={self.id}&page={page}") as llh:
            return loads(llh.read())

    @staticmethod
    def load_live(live_id):
        with urlopen(f"https://www.mirrativ.com/api/live/live?live_id={live_id}") as ll:
            return loads(ll.read())

    @staticmethod
    def load_live_comments(live_id):
        with urlopen(f"https://www.mirrativ.com/api/live/live_comments?live_id={live_id}") as llc:
            return loads(llc.read())

    @staticmethod
    def load_live_polling(live_id):
        with urlopen(f"https://www.mirrativ.com/api/live/live_polling?live_id={live_id}") as llp:
            return loads(llp.read())

    @staticmethod
    def itsukaralink():
        with urlopen("https://api.itsukaralink.jp/livers") as f:
            print(f.info())
            h = loads(f.readline())
            print(h)

        with urlopen("https://api.itsukaralink.jp/events") as e:
            print(e.info())
            j = loads(e.readline())
            print(j)


if __name__ == '__main__':
    a = MirrativAPI(2920158)
    b = a.load_userprofile()
    c = a.load_live_history(1)

    d = c["lives"]

    print(dumps(d[0], indent=4, sort_keys=True))
    print(datetime.fromtimestamp(d[0]["started_at"], timezone(timedelta(hours=9), "JST")))
    print(dumps(d[0]["owner"], indent=4, sort_keys=True))

    with open(__file__) as temp:
        print(temp.read())

    interact(banner="Console", local=locals(), exitmsg="Exit")
