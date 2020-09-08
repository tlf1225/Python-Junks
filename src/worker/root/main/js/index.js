const date = new Date();

time_timer = setInterval(() => {
    modify.textContent = `${date.toLocaleString("ja-JP", {
        weekday: "short", year: "numeric", month: "long", day: "numeric",
         hour: "numeric", minute: "numeric", second: "numeric", timeZone: "Asia/Tokyo"})}`;
}, 1000);

function onYouTubeIframeAPIReady() {
    const yt_list = []
    const base = {
        width: innerWidth / 2,
        height: innerHeight / 2,
        wmode: "transparent",
        host: "https://www.youtube-nocookie.com",
        playerVars: {
            autoplay: 1,
            cc_lang_pref: "en",
            cc_load_policy: 1,
            controls: 1,
            disablekb: 1,
            fs: 1,
            hl: "en",
            iv_load_policy: 3,
            loop: 1,
            modestbranding: 1,
            playsinline: 1,
            rel: 0,
            widget_referrer: location.href
        }
    };
    document.getElementById("open").onclick = () => {
        if (youtube.childElementCount == 0) {
            const a = document.createElement("div");
            a.id = "abc";
            youtube.appendChild(a);
            yt_list.push(new YT.Player(a.id, {
                ...base,
                videoId: "videoseries",
                playerVars: {
                    ...base.playerVars,
                    list: "PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr"
                }
            }));
            const b = document.createElement("div");
            b.id = "def";
            youtube.appendChild(b);
            yt_list.push(new YT.Player(b.id, {
                ...base,
                videoId: "ikgFvU_4rI8"
            }));
            const c = document.createElement("div");
            c.id = "ghi";
            youtube.appendChild(c);
            yt_list.push(new YT.Player(c.id, {
                ...base,
                videoId: "ikgFvU_4rI8"
            }));
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
    const ssu = new SpeechSynthesisUtterance("Welcome to console tlf server.");
    ssu.lang = "en-US";
    speechSynthesis.speak(ssu);
};

setTimeout(youtube_iframe, 500);
