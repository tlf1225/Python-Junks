const regex = /(?:(?:https?:\/\/)?(?:(?:(?:www|m)\.)?youtube(?:-nocookie)?\.com|youtu\.be)\/(?:embed\/|watch\?v=|v\/)?)?((?:\w|-){11,11})/;
const youtube = document.getElementById("youtube"),
      query = document.getElementById("query"),
      result = document.getElementById("result"),
      select_video = document.getElementById("select_video"),
      select_audio = document.getElementById("select_audio"),
      preview = document.getElementById("preview"),
      video = document.getElementById("video"),
      audio = document.getElementById("audio"),
      time = document.getElementById("time"),
      info = document.getElementById("info"),
      play = document.getElementById("play"),
      pause = document.getElementById("pause"),
      head = document.getElementById("head"),
      volume = document.getElementById("volume"),
      mute = document.getElementById("mute"),
      full = document.getElementById("full"),
      dialog = document.getElementById("dialog");

let http = null,
    clone = null;

function QA() {
    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        const res = JSON.parse(this.responseText);
        for (const c of res["items"]) {

        }
    }
}

document.query.search.onclick = () => {
    http = new XMLHttpRequest();
    http.onreadystatechange = QA;
    while (query.firstChild) {
        query.removeChild(query.firstChild);
    }
    http.open("POST", "/cgi-bin/youtube.py", true);
    http.send(null);
};

document.query.onsubmit = () => {
    document.query.search.click();
    return false;
};

document.dialog.run.onclick = () => {
    http = new XMLHttpRequest();
    http.onreadystatechange = () => {
        if (http.readyState === XMLHttpRequest.DONE) {
            try {
                const data = JSON.parse(http.responseText);
                if (http.status === 500) {
                    if (!!data["err"]) {
                        const title = document.createElement("p");
                        title.style.color = "red";
                        title.style.textAlign = "center";
                        title.innerText = data["err"];
                        dialog.appendChild(title);
                        if (!!data["message"]) {
                            const verbose = document.createElement("p");
                            verbose.style.color = "blue";
                            verbose.innerText = data["message"];
                            if (!!data["stacktrace"]) {
                                verbose.innerText += `\n${data["stacktrace"]}`;
                            }
                            dialog.appendChild(verbose);
                        }
                        const panel = document.createElement("div");
                        panel.style.textAlign = "center";
                        const cancel = document.createElement("button");
                        cancel.type = "button";
                        cancel.innerText = "Close";
                        cancel.onclick = () => {
                            while (dialog.firstChild) {
                                dialog.removeChild(dialog.firstChild);
                            }
                            dialog.close();
                        };
                        panel.appendChild(cancel);
                        dialog.appendChild(panel);
                        dialog.showModal();
                        return;
                    }
                } else if (http.status === 200) {
                    for (const k in data) {
                        if (data.hasOwnProperty(k)) {
                            const l = data[k];
                            switch (k) {
                                case "title":
                                    const title = document.createElement("p");
                                    title.innerText = l;
                                    result.append(title);
                                    break;
                                case "formats":
                                    for (const m in l) {
                                        if (l.hasOwnProperty(m)) {
                                            const d = l[m];
                                            if (typeof d["url"] === "string") {
                                                const url = document.createElement("a");
                                                const label = document.createElement("label");
                                                const add = document.createElement("input");
                                                add.value = url.href = d["url"];
                                                url.innerText = label.innerText = d["format"];
                                                add.type = "radio";
                                                if (d["vcodec"] === "none") {
                                                    url.type = `audio/${d["ext"]}`;
                                                    label.htmlFor = add.name = url.className = "audio";
                                                    select_audio.appendChild(label);
                                                    select_audio.appendChild(add);
                                                    select_audio.appendChild(document.createElement("br"));
                                                } else if (d["acodec"] === "none") {
                                                    url.type = `video/${d["ext"]}`;
                                                    label.htmlFor = add.name = url.className = "video";
                                                    select_video.appendChild(label);
                                                    select_video.appendChild(add);
                                                    select_video.appendChild(document.createElement("br"));
                                                }
                                                result.append(url);
                                            }
                                        }
                                        result.appendChild(document.createElement("br"));
                                    }
                                    break;
                            }
                        }
                    }
                    result.removeAttribute("hidden");
                }
            } catch (error) {
                if (error === SyntaxError) {
                    const title = document.createElement("p");
                    title.style.color = "red";
                    title.style.textAlign = "center";
                    title.innerText = "Error: Try Again.";
                    dialog.appendChild(title);
                    const panel = document.createElement("div");
                    panel.style.textAlign = "center";
                    const cancel = document.createElement("button");
                    cancel.type = "button";
                    cancel.innerText = "Close";
                    cancel.onclick = () => {
                        while (dialog.firstChild) {
                            dialog.removeChild(dialog.firstChild);
                        }
                        dialog.close();
                    };
                    panel.appendChild(cancel);
                    dialog.appendChild(panel);
                    dialog.showModal();
                }
            }
        }
    };
    while (result.firstChild) {
        result.removeChild(result.firstChild);
    }

    while (select_video.firstChild) {
        select_video.removeChild(select_video.firstChild);
    }

    while (select_audio.firstChild) {
        select_audio.removeChild(select_audio.firstChild);
    }

    const found = regex.exec(document.dialog.data.value);

    if (found && found.length == 2) {
        http.open("POST", "/cgi-bin/youtube.py", true);
        http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        http.send(`id=${found[1]}`);
        return;
    }
    alert("This url is incorrect");
};

document.dialog.onsubmit = () => {
    document.dialog.run.click();
    return false;
};

document.select.execute.onclick = () => {
    let soc = null;
    while (video.firstChild) {
        video.removeChild(video.firstChild);
    }
    while (audio.firstChild) {
        audio.removeChild(audio.firstChild);
    }
    for (const c of select_video.children) {
        if (c instanceof HTMLInputElement) {
            if (c.checked) {
                soc = document.createElement("source");
                soc.src = c.value;
                video.appendChild(soc);
                break;
            }
        }
    }
    for (const c of select_audio.children) {
        if (c instanceof HTMLInputElement) {
            if (c.checked) {
                soc = document.createElement("source");
                soc.src = c.value;
                audio.appendChild(soc);
                break;
            }
        }
    }
    if (video.childElementCount <= 0 && audio.childElementCount <= 0) return;
    video.load();
    audio.load();
    time.onchange = () => {
        audio.currentTime = video.currentTime = time.value;
    };
    play.onclick = () => {
        if (video.readyState >= 1) video.play();
        if (audio.readyState >= 1) audio.play();
        time.max = video.duration;
    };
    pause.onclick = () => {
        if (video.readyState >= 1) video.pause();
        if (audio.readyState >= 1) audio.pause();
    };
    head.onclick = () => {
        video.currentTime = audio.currentTime = 0;
    };
    volume.onchange = () => {
        video.volume = audio.volume = volume.value;
    };
    mute.onclick = () => {
        volume.value = video.volume = audio.volume = (video.muted = audio.muted = !video.muted) ? 1 : 0;
    };
    full.onclick = () => {
        const isInFullScreen = document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement;
        if (!isInFullScreen) {
            if (preview.requestFullscreen) {
                preview.requestFullscreen();
            } else if (preview.mozRequestFullScreen) {
                preview.mozRequestFullScreen();
            } else if (video.webkitRequestFullScreen) {
                preview.webkitRequestFullScreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.mozCancelFullScreen) {
                document.mozCancelFullScreen();
            }
        }
    };
    video.onended = () => {
        if (video.paused) audio.pause();
    };
    video.ontimeupdate = () => {
        info.innerText = time.value = video.currentTime;
        if (video.readyState >= 1 && audio.readyState >= 1) {
            if (Math.ceil(video.currentTime) !== Math.ceil(audio.currentTime)) {
                video.currentTime = audio.currentTime;
            }
        }
    };
};

document.select.onsubmit = () => {
    preview.click();
    return false;
};

youtube.oncontextmenu = preview.oncontextmenu = e => e.preventDefault();
