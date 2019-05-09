function prepopulate() {
    var query = document.querySelector('#q').value;
    document.getElementById("query").value = query;

    var values = []

    for (var i=0; i < document.getElementById('doc_type').selectedOptions.length; i++) {
        values.push(document.getElementById('doc_type').selectedOptions[i].value)
    }

    for (var i=0; i < document.getElementById('doctype').options.length; i++) {
        if (values.includes(document.getElementById("doctype").options[i].value)) {
        document.getElementById('doctype').options[i].selected = true;
        }
    }

    var items = []

    for (var i=0; i < document.getElementById('city').selectedOptions.length; i++) {
        items.push(document.getElementById('city').selectedOptions[i].value)
    }

    for (var i=0; i < document.getElementById('cities').options.length; i++) {
        if (items.includes(document.getElementById("cities").options[i].value)) {
        document.getElementById('cities').options[i].selected = true;
        }
    }
}