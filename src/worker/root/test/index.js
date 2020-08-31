date = new Date();

function paddingZero(n, digit) {
    zeros = new Array(digit + 1).join("0");
    return (zeros + n).slice(-digit);
}


val = setInterval(() => {
    date.setTime(Date.now());
    tt = [date.getHours(),
        date.getMinutes(),
        date.getSeconds(),
        Math.floor(date.getMilliseconds() / 10)].map(src => paddingZero(src, 2));
    time.innerHTML = tt.join(":");
    d = [tt[0] / 24 * 255, tt[1] / 60 * 255, tt[2] / 60 * 255];
    time.style.fill = `rgb(${d.join(", ")})`;
    r = (tt[2] + tt[3]) / 6000 * 360;
    r = Math.floor(r * 100) / 100;
    earth.style.transform = `rotate(${r}deg)`;
}, 20);
