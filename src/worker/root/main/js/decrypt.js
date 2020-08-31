document.query.search.onclick = () => {
/*
    http = new XMLHttpRequest();
    http.onreadystatechange = () => {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            res = JSON.parse(this.responseText);
        }
    };
    query.clearChildren();
    http.open("POST", "/cgi-bin/youtube.py", true);
    http.send(`keyword=${document.query.keyword.value}`);
*/
};

document.query.onsubmit = () => {
    document.query.search.click();
    return false;
};

function error_message(d){
    if (d.hasOwnProperty("err")) {
        title = document.createElement("p");
        title.style.color = "red";
        title.style.textAlign = "center";
        title.innerText = d["err"];
        error.appendChild(title);
    }
    if (d.hasOwnProperty("message")) {
        verbose = document.createElement("p");
        verbose.style.color = "blue";
        verbose.innerText = d["message"];
        if (d.hasOwnProperty("stacktrace")) {
            verbose.innerText += `\n${d["stacktrace"]}`;
        }
        error.appendChild(verbose);
    }
    panel = document.createElement("div");
    panel.style.textAlign = "center";
    cancel = document.createElement("button");
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
    for (k in data) {
        switch (k) {
            case "title":
                title = document.createElement("p");
                title.innerText = data[k];
                result.append(title);
                break;
            case "formats":
                for (m of data[k]) {
                    url = document.createElement("a");
                    label = document.createElement("label");
                    add = document.createElement("input");
                    add.value = url.href = m["url"];
                    url.innerText = label.innerText = m["format"];
                    add.type = "radio";
                    if (m["vcodec"] === "none") {
                        url.type = `audio/${m["ext"]}`;
                        label.htmlFor = add.name = url.className = "audio";
                        selad.appendChild(label);
                        selad.appendChild(add);
                        selad.appendChild(document.createElement("br"));
                    } else if (m["acodec"] === "none") {
                        url.type = `video/${m["ext"]}`;
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
    http = new XMLHttpRequest();
    http.onreadystatechange = () => {
        if (http.readyState === XMLHttpRequest.DONE) {
            try {
                data = JSON.parse(http.responseText);
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

    found = /(?:(?:https?:\/\/)?(?:(?:(?:www|m)\.)?youtube(?:-nocookie)?\.com\/(?:embed\/|watch\?v=)|youtu\.be\/))?((?:\w|-){11})/.exec(document.dialog.data.value);

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
    video.clearChildren();
    audio.clearChildren();
    test1 = document.createNodeIterator(selvd, NodeFilter.SHOW_ELEMENT,
        code => (code instanceof HTMLInputElement && code.checked) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT).nextNode();
    test2 = document.createNodeIterator(selad, NodeFilter.SHOW_ELEMENT,
        code => (code instanceof HTMLInputElement && code.checked) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT).nextNode();
    if (test1) {
        soc = document.createElement("source");
        soc.src = test1.value;
        video.appendChild(soc);
    }
    if (test2) {
        soc = document.createElement("source");
        soc.src = test2.value;
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

youtube.oncontextmenu = preview.oncontextmenu = e => e.preventDefault();

function test() {
    test = new DOMParser();
    for (w of img) {
        temp = /data:(.+?);?(?:base64)?,(.+)/.exec(w.src);
        data = test.parseFromString(base64.decode(temp[2]), temp[1])

        p = data.getElementsByTagName("svg");
        a = data.getElementsByTagName("polygon");
        b = data.getElementsByTagName("line");
        c = data.getElementsByTagName("rect");

        for (x of a) {
            x.style.fill = "red";
        }

        for (y of b) {
           y.style.stroke = "red";
        }

        for (z of c) {
           z.style.stroke = "red";
        }

        w.src = `data:${data[1]};base64,${base64.encode(p[0].outerHTML)}`
    }
}