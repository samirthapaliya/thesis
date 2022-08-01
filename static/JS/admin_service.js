function table_width(x) {
    if (x.matches) { 
        document.getElementsByClassName("table-responsive")[0].style.width="100%"
    } 
    else {
        document.getElementsByClassName("table-responsive")[0].style.width="900px"
    }
}
var mediaQ = window.matchMedia("(max-width: 1725px)")
table_width(mediaQ) 
mediaQ.addListener(table_width) 