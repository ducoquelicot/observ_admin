// function prepopulate(key) {
//     var query = window.location.search.substring(1);
//     var items = query.split("&");

//     for (var i=0; i<items.length; i++) {
//         var keys = items[i].split("=");
//         if (keys[0] == key) {
//             return keys[1];
//         }
//     }
// }

function prepopulate(key) {
    var data = {city: [], doc_type: []};
    var multi = ["city", "doc_type"];
    var items = window.location.search.substring(1).split("&");

    for (var i=0; i<items.length; i++) {
        var keys = items[i].split("=")

        if (multi.includes(keys[0])) {
            data[keys[0]].push(keys[1])
        } else {
            data[keys[0]] = keys[1]
        }
    }
    // items.forEach(function(param) {
    //     var prop, val = param.split("=");

    //     if (multi.includes(prop)) {
    //         data[prop].push(val);
    //     } else {
    //         data[prop] = val;
    //     }
    // })

    if (data.hasOwnProperty(key)) {
        return data[key];
    }
}

var q = prepopulate("q")
var query = q.replace(/\+/g, " ")
var doctype = prepopulate("doc_type")
var cities = prepopulate("city")

document.getElementById("query").value = query;
document.getElementById("doctype").value = doctype;
document.getElementById("cities").value = cities