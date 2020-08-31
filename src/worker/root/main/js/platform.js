const Base64 = {
    encode: str => {
        return btoa(unescape(encodeURIComponent(str)));
    },
    decode: str => {
        return decodeURIComponent(escape(atob(str)));
    }
};

Object.defineProperty(Element.prototype, 'clearChildren', {
configurable: true, enumerable: false, value: () => { while(this.firstChild) this.removeChild(this.lastChild);}
});

const author = document.createElement("meta");
author.name = "author";
author.content = "honda";

const description = document.createElement("meta");
description.name = "description";
description.content = "This page is test by tlf";

const keywords = document.createElement("meta");
keywords.name = "keywords";
keywords.content = "minecraft server with development web";

const viewport = document.createElement("meta");
viewport.name = "viewport";
viewport.content = "width=device-width, height=device-height, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no";

document.head.appendChild(author);
document.head.appendChild(description);
document.head.appendChild(keywords);
document.head.appendChild(viewport);

try {
    const loader = location.pathname.split("/").pop().split(".")[0];
    if (loader) {
        const sc_elm = document.createElement("script");
        sc_elm.src = `js/${loader}.js`;
        sc_elm.defer = true;
        const cs_elm = document.createElement("link");
        cs_elm.href = `css/${loader}.css`;
        cs_elm.rel = "stylesheet";
        document.head.appendChild(sc_elm);
        document.head.appendChild(cs_elm);
    }
} catch (err) {
    console.log(err.message);
}

setTimeout(() => {
    const yt_js = document.createElement("script");
    yt_js.src = "https://www.youtube.com/iframe_api";
    document.head.appendChild(yt_js);
}, 500);