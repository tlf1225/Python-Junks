from youtube_dl import YoutubeDL


def main(url="https://www.youtube.com/playlist?list=PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr", ffmpeg="D:/"):
    ytdl = YoutubeDL(params={
        "no_cache": True,
        "no_warnings": False,
        "ignoreerrors": True,
        "quiet": True,
        "skip_download": True,
        "simulate": True,
        "ffmpeg_location": ffmpeg
    })
    result = ytdl.extract_info(url=url, download=False, ie_key="Youtube")
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
    main(url="https://www.youtube.com/watch?v=WJ16v-hD1mw", ffmpeg="D:/ffmpeg-20200628-4cfcfb3-win64-shared/bin")
