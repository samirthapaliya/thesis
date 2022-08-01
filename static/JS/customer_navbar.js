var dropdown_opener = document.getElementsByClassName("dropdown-opener")[0];
var dropdown_content = document.getElementsByClassName("dropdown-content")[0];
var dob = false;

dropdown_content.style.display = "none";
dropdown_opener.style.color = "black";

function open_dropdown() {
  if (dob == false) {
    dropdown_content.style.display = "block";

    dob = true;
  } else {
    dropdown_content.style.display = "none";
    dropdown_opener.style.color = "black";
    dob = false;
  }
}

function navbar_content(x) {
  if (x.matches) {
    dropdown_content.style.display = "flex";
    dropdown_opener.style.display = "none";
  } else {
    dropdown_content.style.display = "none";
    dropdown_opener.style.display = "block";
  }
}
var mediaQ = window.matchMedia("(max-width: 575px)");
navbar_content(mediaQ);
mediaQ.addListener(navbar_content);
