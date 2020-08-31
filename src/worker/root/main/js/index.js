if (!time_timer) {
    time_timer = setInterval(() => {
    const date = new Date();
    document.getElementById("modify").textContent = `${date.toLocaleString("ja-JP", {
        weekday: "short", year: "numeric", month: "long", day: "numeric",
         hour: "numeric", minute: "numeric", second: "numeric", timeZone: "Asia/Tokyo"})}`;
    }, 1000);
}

function onYouTubeIframeAPIReady() {
    document.getElementById("open").onclick = () => {
        const info = document.getElementById("youtube");
        if (info.childElementCount === 0) {
            ["https://www.youtube-nocookie.com/embed/?rel=0&disablekb=1&controls=0&modestbranding=1", "https://www.youtube-nocookie.com/embed/ikgFvU_4rI8?rel=0&showinfo=0&controls=0&modestbranding=1&disablekb=1", "https://www.youtube-nocookie.com/embed/videoseries?list=PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr"].forEach(i => {
                const add = document.createElement("iframe");
                add.width = 560;
                add.height = 315;
                add.src = i;
                add.allowFullscreen = true;
                info.appendChild(add);
            });
            info.hidden = false;
            open.innerText = "Close";
        } else {
            info.clearChildren();
            info.hidden = true;
            open.innerText = "Open";
        }
    };
}

document.getElementById("speak").onclick = () => {
    const ssu = new SpeechSynthesisUtterance("Welcome to console tlf server.");
    ssu.lang = "en-US";
    speechSynthesis.speak(ssu);
};

setTimeout(() => {
    const yt_js = document.createElement("script");
    yt_js.src = "https://www.youtube.com/iframe_api";
    document.head.appendChild(yt_js);
}, 500);
