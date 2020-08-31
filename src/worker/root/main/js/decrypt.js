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

document.query.search.onclick = () => {
    const http = new XMLHttpRequest();
    http.onreadystatechange = () => {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            const res = JSON.parse(this.responseText);
        }
    };
    query.clearChildren();
    http.open("POST", "/cgi-bin/youtube.py", true);
    http.send(`keyword=${document.query.keyword.value}`);
};

document.query.onsubmit = () => {
    document.query.search.click();
    return false;
};

function error_message(d){
    if (d.hasOwnProperty("err")) {
        const title = document.createElement("p");
        title.style.color = "red";
        title.style.textAlign = "center";
        title.innerText = d["err"];
        dialog.appendChild(title);
        if (d.hasOwnProperty("message")) {
            const verbose = document.createElement("p");
            verbose.style.color = "blue";
            verbose.innerText = d["message"];
            if (d.hasOwnProperty("stacktrace")) {
                verbose.innerText += `\n${d["stacktrace"]}`;
            }
            dialog.appendChild(verbose);
        }
        const panel = document.createElement("div");
        panel.style.textAlign = "center";
        const cancel = document.createElement("button");
        cancel.type = "button";
        cancel.innerText = "Close";
        cancel.onclick = () => {
            dialog.clearChildren();
            dialog.close();
        };
        panel.appendChild(cancel);
        dialog.appendChild(panel);
        dialog.showModal();
    }
}

function parser(data) {
    for (const k in data) {
        switch (k) {
            case "title":
                const title = document.createElement("p");
                title.innerText = data[k];
                result.append(title);
                break;
            case "formats":
                for (const m in data[k]) {
                    const url = document.createElement("a");
                    const label = document.createElement("label");
                    const add = document.createElement("input");
                    add.value = url.href = data[k][m]["url"];
                    url.innerText = label.innerText = data[k][m]["format"];
                    add.type = "radio";
                    if (d["vcodec"] === "none") {
                        url.type = `audio/${data[k][m]["ext"]}`;
                        label.htmlFor = add.name = url.className = "audio";
                        select_audio.appendChild(label);
                        select_audio.appendChild(add);
                        select_audio.appendChild(document.createElement("br"));
                    } else if (d["acodec"] === "none") {
                        url.type = `video/${data[k][m]["ext"]}`;
                        label.htmlFor = add.name = url.className = "video";
                        select_video.appendChild(label);
                        select_video.appendChild(add);
                        select_video.appendChild(document.createElement("br"));
                    }
                    result.append(url);
                    result.appendChild(document.createElement("br"));
                }
                break;
        }
    }
    result.removeAttribute("hidden");
}


document.dialog.run.onclick = () => {
    const http = new XMLHttpRequest();
    http.onreadystatechange = () => {
        if (http.readyState === XMLHttpRequest.DONE) {
            try {
                const data = JSON.parse(http.responseText);
                if (http.status === 500) {
                    error_message(data)
                } else if (http.status === 200) {
                    parser(data)
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
                        dialog.clearChildren();
                        dialog.close();
                    };
                    panel.appendChild(cancel);
                    dialog.appendChild(panel);
                    dialog.showModal();
                }
            }
        }
    };
    result.clearChildren();
    select_video.clearChildren();
    select_audio.clearChildren();

    const found = regex.exec(document.dialog.data.value);

    if (found && found.length == 2) {
        http.open("POST", "/cgi-bin/youtube.py", true);
        http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        http.send(`id=${found[1]}`);
    } else {
        alert("This url is incorrect");
    }
};

document.dialog.onsubmit = () => {
    document.dialog.run.click();
    return false;
};

document.select.execute.onclick = () => {
    video.clearChildren();
    audio.clearChildren();
    const test1 = document.createNodeIterator(select_video, NodeFilter.SHOW_ELEMENT,
        code => (code instanceof HTMLInputElement && code.checked) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT);
    const test2 = document.createNodeIterator(select_audio, NodeFilter.SHOW_ELEMENT,
        code => (code instanceof HTMLInputElement && code.checked) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT);
    let test = test1.nextNode()
    if (test) {
        const soc = document.createElement("source");
        soc.src = test.value;
        video.appendChild(soc);
    }
    test = test2.nextNode();
    if (test) {
        const soc = document.createElement("source");
        soc.src = test.value;
        audio.appendChild(soc);
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
        if (!document.fullscreenElement) {
            preview.requestFullScreen();
        } else {
            document.exitFullscreen(document);
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
