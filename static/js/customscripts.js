    i = true;
function myFunction() {
    title_elem = document.getElementById("title_elem");
    if (i == true) {
        title_elem.innerHTML = "Le";
        i = false;
    } else {
        title_elem.innerHTML = "Meme";
        i = true;
    }
}
setInterval(myFunction, 2000);