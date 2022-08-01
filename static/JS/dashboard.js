//ProgressBars
 options = {
    startAngle: -1.5,
    size: 150,
    value: .75,
    fill: {gradient: ["#fc1f3c", "#652efc", "#2dfa7c"]}
}

function setC1(x) {
    if (x.matches) { 
        options = {
            startAngle: -1.5,
            size: 70,
            value: .75,
            fill: {gradient: ["#fc1f3c", "#652efc", "#2dfa7c"]}
        }
        $(".circle .bar").circleProgress(options).on('circle-animation-progress',
        function(event, progress, stepValue) {
        });
    } else {
        options = {
            startAngle: -1.5,
            size: 150,
            value: .75,
            fill: {gradient: ["#fc1f3c", "#652efc", "#2dfa7c"]}
        }
        $(".circle .bar").circleProgress(options).on('circle-animation-progress',
        function(event, progress, stepValue) {
        });
    }
}
var mediaQ1 = window.matchMedia("(max-width: 590px)")
setC1(mediaQ1) 
mediaQ1.addListener(setC1) 


/*====================RNR Functions====================*/
function animateValue(id, start, end, duration) {
    // assumes integer values for start and end

    var obj = document.getElementById(id);
    var range = end - start;
    // no timer shorter than 50ms (not really visible any way)
    var minTimer = 50;
    // calc step time to show all interediate values
    var stepTime = Math.abs(Math.floor(duration / range));

    // never go below minTimer
    stepTime = Math.max(stepTime, minTimer);

    // get current time and calculate desired end time
    var startTime = new Date().getTime();
    var endTime = startTime + duration;
    var timer;

    function run() {
        var now = new Date().getTime();
        var remaining = Math.max((endTime - now) / duration, 0);
        var value = Math.round(end - (remaining * range));
        obj.innerHTML = value;
        if (value == end) {
            clearInterval(timer);
            }
        }
    timer = setInterval(run, stepTime);
    run();
}

var bs = parseInt(document.getElementById("bs").innerHTML);
animateValue("bs", 0, bs, 1000);

var bu = parseInt(document.getElementById("bu").innerHTML);
animateValue("bu", 0, bu, 1000);

var bc = parseInt(document.getElementById("bc").innerHTML);
animateValue("bc", 0, bc, 1000);

var bb = parseInt(document.getElementById("bb").innerHTML);
animateValue("bb", 0, bb, 1000);

var bw = parseInt(document.getElementById("bw").innerHTML);
animateValue("bw", 0, bw, 1000);

var bg = parseInt(document.getElementById("bg").innerHTML);
animateValue("bg", 0, bg, 1000);

var bh = parseInt(document.getElementById("bh").innerHTML);
animateValue("bh", 0, bh, 1000);

var br = parseInt(document.getElementById("br").innerHTML);
animateValue("br", 0, br, 1000);

var bn = parseInt(document.getElementById("bn").innerHTML);
animateValue("bn", 0, bn, 1000);