var service_number = document.getElementsByClassName("Numbering").length
for (i=0; i<service_number; i++) {
    document.getElementsByClassName("Numbering")[i].innerHTML = i + 1
}
