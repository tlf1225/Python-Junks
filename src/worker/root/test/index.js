var time = document.getElementById("time");
var earth = document.getElementById("earth");
var date = new Date();

function paddingZero(n, digit) {
    "use strict";
    var zeros = new Array(digit + 1).join("0");
    return (zeros + n).slice(-digit);
}


var val = setInterval(() => {
    "use strict";
    date.setTime(Date.now());
    let tt = [date.getHours(),
        date.getMinutes(),
        date.getSeconds(),
        Math.floor(date.getMilliseconds() / 10)].map(src => paddingZero(src, 2));
    time.innerHTML = tt.join(":");
    let d = [tt[0] / 24 * 255, tt[1] / 60 * 255, tt[2] / 60 * 255];
    time.setAttribute("fill", `rgb(${d.join(", ")})`);
    let r = (tt[2] + tt[3]) / 6000 * 360;
    r = Math.floor(r * 100) / 100;
    earth.setAttribute("transform", `rotate(${r})`);
}, 20);
