const base64 = {
    encode: str => btoa(unescape(encodeURIComponent(str))),
    decode: str => decodeURIComponent(escape(atob(str)))
};

Object.defineProperty(Element.prototype, 'clearChildren', {
configurable: true, enumerable: false, value: () => { while(this.firstChild) this.removeChild(this.lastChild);}
});

const description = document.createElement("meta");
description.name = "description";
description.content = "This page is test by tlf";

const viewport = document.createElement("meta");
viewport.name = "viewport";
viewport.content = "width=device-width, height=device-height, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no";

document.head.appendChild(description);
document.head.appendChild(viewport);

try {
    const loader = location.pathname.split("/").pop().split(".")[0];
    if (loader) {
        const sc_elm = document.createElement("script");
        sc_elm.src = `js/${loader}.js`;
        const cs_elm = document.createElement("link");
        cs_elm.href = `css/${loader}.css`;
        cs_elm.rel = "stylesheet";
        document.head.appendChild(sc_elm);
        document.head.appendChild(cs_elm);
    }
} catch (err) {
    console.log(err.message);
}
