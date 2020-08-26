const pictures = document.getElementById("pictures");

["http://qualia.clearrave.co.jp/images/gallery/06_b.jpg", "http://qualia.clearrave.co.jp/images/gallery/17_b.jpg", "http://palette.clearrave.co.jp/product/sakusaku/img/gallery/gal_b_14.jpg", "http://sweet.clearrave.co.jp/karehana/img/gallery/img_05.jpg", "http://recette.clearrave.co.jp/img/gallery/img_04.jpg", "http://qualia.clearrave.co.jp/images/gallery/11_b.jpg"].forEach(i => {
    const img = document.createElement("img");
    img.src = i;
    img.alt = "This image has been moved";
    pictures.appendChild(img);
});

window.onYouTubeIframeAPIReady = () => {
    window.player = new YT.Player("yt-pre", {
        height: window.innerHeight / 2,
        width: window.innerWidth / 2,
        videoId: "lSqnqSSXTUI",
        wmode: "transparent",
        host: "https://www.youtube-nocookie.com",
        events: {
            onReady: event => {
                event.target.setVolume(100);
                event.target.setPlaybackQuality("highres");
                event.target.setPlaybackRate(1.0);
            }
        },
        playerVars: {
            autoplay: 0,
            cc_lang_pref: "en",
            cc_load_policy: 1,
            controls: 1,
            disablekb: 0,
            fs: 1,
            hl: "en",
            iv_load_policy: 3,
            loop: 1,
            modestbranding: 1,
            origin: location.origin,
            playsinline: 1,
            rel: 0,
            showinfo: 0,
            widget_referrer: location.href
        }
    });
    window.ncs = new YT.Player("yt-ncs", {
        height: window.innerHeight / 2,
        width: window.innerWidth / 2,
        wmode: "transparent",
        host: "https://www.youtube-nocookie.com",
        playerVars: {
            autoplay: 1,
            list: "PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK",
            listType: "playlist",
            controls: 0,
            showinfo: 0
        }
    });
};
