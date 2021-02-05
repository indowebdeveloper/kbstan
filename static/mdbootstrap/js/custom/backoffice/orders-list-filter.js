function getFiltersFromUrl() { // this function returns the search string only, but entirely unsplit
    let search = window.location.search.substring(1); // this takes the search and removes the first character (which is a "?") => e.g. "/orders/?q=chris+await" becomes "?q=chris+await" which is cut to "q=chris+await"

    return search;
}


function updateUI(field_name, field_value) {
    $(`[name=${field_name}]`).val(field_value);
}


// ======================================================
// ======================================================
// ======================================================

function restoreFilterValues() {
    let search = getFiltersFromUrl();
    let split_by_terms = search.split('&'); // this splits the url into the invidual search terms, e.g "q=FullField&date=today&name=chris" turns into an ARRAY like this: ["q=FullField", "date=today", "name=chris"]

    for(let i = 0; i < split_by_terms.length; i++) {


        let split = split_by_terms[i].split('='); // the ARRAY has this format: ["q=FullField", "date=today", "name=chris"]. So by splitting it, we gain access to the field_name and the field_value
        let field_name = split[0];
        let field_value = split[1].replaceAll(/\+/g, " "); // this is to replace the "+" with a "space". E.g. "Stan+Kosy+Tires" becomes "Stan Kosy Tires", which is how people would type it in the search field;
        field_value = decodeURIComponent(field_value);

        console.log('field_name');
        console.log(field_name);
        console.log('field_value');
        console.log(field_value);

        updateUI(field_name, field_value);
    }
}






// ======================================================
// ======================================================
// ======================================================
// ======================================================
// ======================================================
// ======================================================






$(document).ready(function(){
    restoreFilterValues();
});