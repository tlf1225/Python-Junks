time_timer = setInterval(() => {
    date = new Date();
    modify.textContent = `${date.toLocaleString("ja-JP", {
        weekday: "short", year: "numeric", month: "long", day: "numeric",
         hour: "numeric", minute: "numeric", second: "numeric", timeZone: "Asia/Tokyo"})}`;
}, 1000);

yt_list = []

function onYouTubeIframeAPIReady() {
    document.getElementById("open").onclick = () => {
        if (youtube.childElementCount == 0) {
            a = document.createElement("div");
            a.id = "abc";
            youtube.appendChild(a);
            yt_list.push(new YT.Player("abc", {
                width: innerWidth / 3,
                height: innerHeight / 3,
                videoId: "videoseries",
                host: "https://www.youtube-nocookie.com",
                playerVars: {
                    list: "PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr",
                    loop: 1,
                    rel: 0,
                    disablekb: 1,
                    controls: 0,
                    modestbranding: 1,
                    widget_referrer: location.href
                }
            }));
            b = document.createElement("div");
            b.id = "def";
            youtube.appendChild(b);
            yt_list.push(new YT.Player("def", {
                width: innerWidth / 3,
                height: innerHeight / 3,
                videoId: "ikgFvU_4rI8",
                host: "https://www.youtube-nocookie.com",
                playerVars: {
                    rel: 0,
                    disablekb: 1,
                    controls: 0,
                    modestbranding: 1,
                    widget_referrer: location.href
                }
            }));
            /*
            c = document.createElement("div");
            c.id = "ghi";
            youtube.appendChild(c);
            yt_list.push(new YT.Player("ghi", {
                width: innerWidth / 3,
                height: innerHeight / 3,
                videoId: "ikgFvU_4rI8",
                host: "https://www.youtube-nocookie.com",
                playerVars: {
                    rel: 0,
                    disablekb: 1,
                    controls: 0,
                    modestbranding: 1,
                    widget_referrer: location.href
                }
            }));
            */
            youtube.hidden = false;
            document.getElementById("open").innerText = "Close";
        } else {
            for (z of yt_list) {
                z.destroy();
            }
            yt_list.length = 0;
            youtube.clearChildren();
            youtube.hidden = true;
            document.getElementById("open").innerText = "Open";
        }
    };
}

document.getElementById("speak").onclick = () => {
    ssu = new SpeechSynthesisUtterance("Welcome to console tlf server.");
    ssu.lang = "en-US";
    speechSynthesis.speak(ssu);
};

setTimeout(youtube_iframe, 500);
