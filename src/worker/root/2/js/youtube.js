window.onYouTubeIframeAPIReady = () => {
    window.player = new YT.Player("ytplayer", {
        width: document.documentElement.clientWidth,
        height: document.documentElement.clientHeight,
        videoId: "Stwkoa3QYNE",
        host: "https://www.youtube-nocookie.com",
        events: {
            onReady: event => {
                event.target.setVolume(100);
                event.target.setPlaybackQuality("highres");
                event.target.setPlaybackRate(1.2);
                setTimeout(() => event.target.playVideo(), 1000);
                document.body.onresize = () => {
                    let frame = player.getIframe();
                    frame.width = document.documentElement.clientWidth;
                    frame.height = document.documentElement.clientHeight;
                };
            }
        },
        playerVars: {
            autoplay: 0,
            cc_lang_pref: "en",
            cc_load_policy: 1,
            controls: 0,
            disablekb: 1,
            fs: 0,
            hl: "en",
            iv_load_policy: 3,
            listType: "playlist",
            list: "UUtHRR8yqk-4YFFWjtUH8n1g",
            loop: 1,
            modestbranding: 1,
            origin: location.origin,
            playsinline: 1,
            rel: 0,
            showinfo: 0,
            widget_referrer: location.href
        }
    });

    setTimeout(() => {
        const target = document.getElementById("ytplayer");
        target.requestFullScreen();
        target.contentWindow.postMessage(
            JSON.stringify({
                event: "command",
                func: "seekTo",
                args: [64]
            }),
            new URL(target.src).origin
        );
    }, 5000);
};
