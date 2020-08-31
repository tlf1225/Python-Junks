if (!time_timer) {
    time_timer = setInterval(() => {
    date = new Date();
    modify.textContent = `${date.toLocaleString("ja-JP", {
        weekday: "short", year: "numeric", month: "long", day: "numeric",
         hour: "numeric", minute: "numeric", second: "numeric", timeZone: "Asia/Tokyo"})}`;
    }, 1000);
}

function onYouTubeIframeAPIReady() {
    open.onclick = () => {
        if (youtube.childElementCount === 0) {
            ["https://www.youtube-nocookie.com/embed/?rel=0&disablekb=1&controls=0&modestbranding=1", "https://www.youtube-nocookie.com/embed/ikgFvU_4rI8?rel=0&showinfo=0&controls=0&modestbranding=1&disablekb=1", "https://www.youtube-nocookie.com/embed/videoseries?list=PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr"].forEach(i => {
                const add = document.createElement("iframe");
                add.width = 560;
                add.height = 315;
                add.src = i;
                add.allowFullscreen = true;
                youtube.appendChild(add);
            });
            youtube.hidden = false;
            open.innerText = "Close";
        } else {
            youtube.clearChildren();
            youtube.hidden = true;
            open.innerText = "Open";
        }
    };
}

speak.onclick = () => {
    const ssu = new SpeechSynthesisUtterance("Welcome to console tlf server.");
    ssu.lang = "en-US";
    speechSynthesis.speak(ssu);
};

setTimeout(() => {
    const yt_js = document.createElement("script");
    yt_js.src = "https://www.youtube.com/iframe_api";
    document.head.appendChild(yt_js);
}, 500);
