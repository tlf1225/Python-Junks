from youtube_dl import YoutubeDL
from getpass import getpass


def main():
    ytdl = YoutubeDL(params={
        "username": "bulemasa5727",
        "password": getpass("Password:"),
        "no_cache": True,
        "no_warnings": False,
        "ignoreerrors": True,
        "simulate": True
    })
    ytdl.extract_info(url="https://www.youtube.com/playlist?list=PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr", download=False)


if __name__ == '__main__':
    main()
