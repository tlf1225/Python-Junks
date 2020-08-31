const result = document.getElementById("result"),
      selvd = document.getElementById("selvd"),
      selad = document.getElementById("selad"),
      preview = document.getElementById("preview");

document.query.search.onclick = () => {
/*
    const http = new XMLHttpRequest();
    http.onreadystatechange = () => {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            const res = JSON.parse(this.responseText);
        }
    };
    document.getElementById("query").clearChildren();
    http.open("POST", "/cgi-bin/youtube.py", true);
    http.send(`keyword=${document.query.keyword.value}`);
*/
};

document.query.onsubmit = () => {
    document.query.search.click();
    return false;
};

function error_message(d){
    const error = document.getElementById("error");
    if (d.hasOwnProperty("err")) {
        const title = document.createElement("p");
        title.style.color = "red";
        title.style.textAlign = "center";
        title.innerText = d["err"];
        error.appendChild(title);
    }
    if (d.hasOwnProperty("message")) {
        const verbose = document.createElement("p");
        verbose.style.color = "blue";
        verbose.innerText = d["message"];
        if (d.hasOwnProperty("stacktrace")) {
            verbose.innerText += `\n${d["stacktrace"]}`;
        }
        error.appendChild(verbose);
    }
    const panel = document.createElement("div");
    panel.style.textAlign = "center";
    const cancel = document.createElement("button");
    cancel.type = "button";
    cancel.innerText = "Close";
    cancel.onclick = () => {
        error.clearChildren();
        error.close();
    };
    panel.appendChild(cancel);
    error.appendChild(panel);
    error.showModal();
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
                    if (data[k][m]["vcodec"] === "none") {
                        url.type = `audio/${data[k][m]["ext"]}`;
                        label.htmlFor = add.name = url.className = "audio";
                        selad.appendChild(label);
                        selad.appendChild(add);
                        selad.appendChild(document.createElement("br"));
                    } else if (data[k][m]["acodec"] === "none") {
                        url.type = `video/${data[k][m]["ext"]}`;
                        label.htmlFor = add.name = url.className = "video";
                        selvd.appendChild(label);
                        selvd.appendChild(add);
                        selvd.appendChild(document.createElement("br"));
                    }
                    result.append(url);
                    result.appendChild(document.createElement("br"));
                }
                break;
        }
    }
    result.hidden = false;
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
                    error_message({err: "Error: Try Again."});
                }
            }
        }
    };

    const found = /(?:(?:https?:\/\/)?(?:(?:(?:www|m)\.)?youtube(?:-nocookie)?\.com\/(?:embed\/|watch\?v=)|youtu\.be\/))?((?:\w|-){11})/.exec(document.dialog.data.value);

    if (found) {
        if (found.length == 2){
            http.open("POST", "/cgi-bin/youtube.py", true);
            http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            http.send(`id=${found[1]}`);

            result.clearChildren();
            result.hidden = true;
            selvd.clearChildren();
            selad.clearChildren();
        }
    } else {
        error_message({err: "This url is incorrect"})
    }
};

document.dialog.onsubmit = () => {
    document.dialog.run.click();
    return false;
};

document.sel.execute.onclick = () => {
    const video = document.getElementById("video"),
            audio = document.getElementById("audio"),
            time = document.getElementById("time"),
            info = document.getElementById("info"),
            play = document.getElementById("play"),
            pause = document.getElementById("pause"),
            head = document.getElementById("head"),
            volume = document.getElementById("volume"),
            mute = document.getElementById("mute"),
            full = document.getElementById("full");
    video.clearChildren();
    audio.clearChildren();
    const test1 = document.createNodeIterator(selvd, NodeFilter.SHOW_ELEMENT,
        code => (code instanceof HTMLInputElement && code.checked) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT).nextNode();
    const test2 = document.createNodeIterator(selad, NodeFilter.SHOW_ELEMENT,
        code => (code instanceof HTMLInputElement && code.checked) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT).nextNode();
    if (test1) {
        const soc = document.createElement("source");
        soc.src = test.value;
        video.appendChild(soc);
    }
    if (test2) {
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
        video.muted = audio.muted = !video.muted;
    };
    full.onclick = () => {
        if (!document.fullscreenElement) {
            preview.requestFullscreen();
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

document.sel.onsubmit = () => {
    preview.click();
    return false;
};

document.getElementById("youtube").oncontextmenu = preview.oncontextmenu = e => e.preventDefault();
