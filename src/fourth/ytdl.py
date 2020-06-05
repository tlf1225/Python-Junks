from youtube_dl import YoutubeDL


def main():
    ytdl = YoutubeDL(params={
        "no_cache": True,
        "no_warnings": False,
        "ignoreerrors": True,
        "quiet": True,
        "skip_download": True,
        "simulate": True,
        "ffmpeg_location": "D:/ffmpeg-20200603-b6d7c4c-win64-shared/bin"
    })
    result = ytdl.extract_info(url="https://www.youtube.com/playlist?list=PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr", download=False)
    if "entries" not in result:
        print(result["title"])
        for url in sorted(result["formats"], key=lambda x: int(x["format_id"])):
            print(f"{url['format']} {url['url']}")
    else:
        for entries in result["entries"]:
            print(entries["title"])
            for url in sorted(entries["formats"], key=lambda x: int(x["format_id"])):
                print(f"{url['format']} {url['url']}")
            print()


if __name__ == '__main__':
    main()
