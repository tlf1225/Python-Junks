function onYouTubeIframeAPIReady() {
    const base = {
        height: Math.trunc(innerHeight / 2),
        width: Math.trunc(innerWidth / 2),
        wmode: "transparent",
        host: "https://www.youtube-nocookie.com",
        playerVars: {
            // autoplay: 1,
            cc_lang_pref: "en",
            cc_load_policy: 1,
            controls: 1,
            disablekb: 1,
            fs: 1,
            hl: "en",
            iv_load_policy: 3,
            loop: 1,
            modestbranding: 1,
            playsinline: 1,
            rel: 0,
            widget_referrer: location.href
        }
    };
    let player1 = {
        ...base,
        videoId: "lSqnqSSXTUI",
        events: {
            ...base.events,
            onReady: event => {
                event.target.setVolume(100);
                event.target.setPlaybackQuality("highres");
                event.target.setPlaybackRate(1.0);
            }
        }
    };

    let player2 = {
        ...base,
        videoId: "videoseries",
        playerVars: {
            ...base.playerVars,
            list: "PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK",
            listType: "playlist",
        }
    };

    window.player = new YT.Player("yt-pre", player1);
    window.ncs = new YT.Player("yt-ncs", player2);
}

setTimeout(youtube_iframe, 500);

["http://qualia.clearrave.co.jp/images/gallery/06_b.jpg", "http://qualia.clearrave.co.jp/images/gallery/17_b.jpg", "http://palette.clearrave.co.jp/product/sakusaku/img/gallery/gal_b_14.jpg", "http://sweet.clearrave.co.jp/karehana/img/gallery/img_05.jpg", "http://recette.clearrave.co.jp/img/gallery/img_04.jpg", "http://qualia.clearrave.co.jp/images/gallery/11_b.jpg"].forEach(i => {
    const img = document.createElement("img");
    img.src = i;
    img.alt = "This image has been moved";
    pictures.appendChild(img);
});