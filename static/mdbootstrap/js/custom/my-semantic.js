$(document).ready(function() {
    const url = window.location.href;
    const checkRegexEdit = url.match(/products\/.*\/edit/g); // this will match "/products/*ANYURL*/edit"
    const checkRegexAdjust = url.match(/products\/.*\/adjust-stock/g);
    if(
        url.includes("products/create/") ||
        checkRegexEdit != null ||
        checkRegexAdjust != null
        ) {
        $('select').dropdown();
    }
});