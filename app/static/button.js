function subscribe() {
    var x = document.getElementById("subscribe");
        if (x.style.display === "none") {
            x.style.display = "block";
        } else if (x.style.display === "block") {
            x.style.display = "none";
        } else {
            x.style.display = "block";
        }
    }