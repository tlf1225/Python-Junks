const info = document.getElementById("youtube");
const open = document.getElementById("open");
const speak = document.getElementById("speak");
const ssu = new SpeechSynthesisUtterance("Welcome to tlf1225 Server");

if (!window.timer_id) {
    window.timer_id = setInterval(() => {
    const date = new Date();
    document.getElementById("modify").textContent = `${date.toLocaleString("ja-JP", {
        weekday: "short", year: "numeric", month: "long", day: "numeric",
         hour: "numeric", minute: "numeric", second: "numeric", timeZone: "Asia/Tokyo"})}`;
    }, 1000);
} else {
    clearInterval(window.timer_id);
    window.timer_id = undefined;
}

open.onclick = () => {
    if (info.childElementCount === 0) {
        ["https://www.youtube-nocookie.com/embed/7svmoZcY8UA?rel=0&disablekb=1&controls=0&showinfo=0&modestbranding=1", "https://www.youtube-nocookie.com/embed/_Wm_Sce1U44?playlist=_Wm_Sce1U44&version=3&autoplay=0&disablekb=1&controls=0&hl=en&loop=1&showinfo=0&rel=0&modestbranding=1", "https://www.youtube-nocookie.com/embed/ikgFvU_4rI8?rel=0&showinfo=0&controls=0&modestbranding=1&disablekb=1", "https://www.youtube-nocookie.com/embed/videoseries?list=PLfwcn8kB8EmMQSt88kswhY-QqJtWfVYEr"].forEach(i => {
            const add = document.createElement("iframe");
            add.width = 560;
            add.height = 315;
            add.src = i;
            add.setAttribute("allowfullscreen", "");
            info.appendChild(add);
        });
        info.removeAttribute("hidden");
        open.innerText = "Close";
    } else {
        while (info.firstChild) {
            info.removeChild(info.firstChild);
        }
        info.setAttribute("hidden", "");
        open.innerText = "Open";
    }
};

speak.onclick = () => {
    ssu.lang = "en-US";
    speechSynthesis.speak(ssu);
};
