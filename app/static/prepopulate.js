function prepopulate(key) {
    var query = window.location.search.substring(1);
    var items = query.split("&");

    for (var i=0; i<items.length; i++) {
        var keys = items[i].split("=");
        if (keys[0] == key) {
            return keys[1];
        }
    }
}

var q = prepopulate("q")
var query = q.replace(/\+/g, " ")
var doctype = prepopulate("doc_type")
var cities = prepopulate("city")

document.getElementById("query").value = query;
document.getElementById("doctype").value = doctype;
document.getElementById("cities").value = cities