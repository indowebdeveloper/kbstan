function simulateClick(sender) { // this function simulates a click on an element. The target element is passed by the clicker-element's "data-click-target"-attribute
    console.log('clicked this');


    const target = $(sender).data('click-target');
    $(target).trigger("click");
}






///////////////////////////////////////////////////
///////////////////////////////////////////////////
///////////////////////////////////////////////////

function showHideRequiredFields(target, required='true') { //
    console.log('showHideRequiredFields');
    console.log(target);
    console.log('required');
    console.log(required);
    let reqFields = $(target).find('input');
    reqFields.push(   $(target).find('select')   );
    reqFields.push(   $(target).find('textarea')   );
    for(let i=0;i<reqFields.length;i++) {
        $(reqFields[i]).prop('required',required);
    }
}






///////////////////////////////////////////////////
///////////////////////////////////////////////////
///////////////////////////////////////////////////

function resetAndSubmitForm(sender) { // this function can be called by any element. It will reset and resubmit an empty form. To select the form that should be reset, the element calling this function should have a data-attr. in this format => data-target-form='#customer_search_form'
    const target_form = $(sender).data('target-form');

    $(target_form).trigger("reset");
    $(target_form).submit();

    console.log(`reset of form ${target_form} successful.`);
}








///////////////////////////////////////////////////
///////////////////////////////////////////////////
///////////////////////////////////////////////////
// FILTERS FUNCTIONS


function getFiltersFromUrl() { // this function returns the search string only, but entirely unsplit
    let search = window.location.search.substring(1); // this takes the search and removes the first character (which is a "?") => e.g. "/orders/?q=chris+await" becomes "?q=chris+await" which is cut to "q=chris+await"

    return search;
}

function updateUI(field_name, field_value) {
    const currentField = $(`[name=${field_name}]`);

    if( $(currentField).attr('type') == 'checkbox' ) {
        $(currentField).prop('checked', 'checked');
    }
    else {
        $(`[name=${field_name}]`).val(field_value);
    }
}

function restoreFilterValues() { // THIS IS THE <<MAIN FUNCTION>> ===>>> call this function when onDocumentReady occurs to restore filter values
    let search = getFiltersFromUrl();
    let split_by_terms = search.split('&'); // this splits the url into the invidual search terms, e.g "q=FullField&date=today&name=chris" turns into an ARRAY like this: ["q=FullField", "date=today", "name=chris"]

    for(let i = 0; i < split_by_terms.length; i++) { // for each searchTerm, it will fill out the fields there are
        let split = split_by_terms[i].split('='); // the ARRAY has this format: ["q=FullField", "date=today", "name=chris"]. So by splitting it, we gain access to the field_name and the field_value
        let field_name = split[0];
        let field_value = split[1].replaceAll(/\+/g, " "); // this is to replace the "+" with a "space". E.g. "Stan+Kosy+Tires" becomes "Stan Kosy Tires", which is how people would type it in the search field;
        field_value = decodeURIComponent(field_value);

        updateUI(field_name, field_value);
    }
}





///////////////////////////////////////////////////
///////////////////////////////////////////////////
///////////////////////////////////////////////////



function makeAllFormFieldsRequired(target, required=true) { // this function takes a target-form and makes all <input>, <select> and <textarea> required
    console.log("FUNCTION: makeAllFormFieldsRequired() executed");
    
    let reqFields;
    reqFields = $(`${target}`).find('input, select, textarea');


    for(let i=0;i<reqFields.length;i++) {
        console.log(!$(reqFields[i]).hasClass('search'));
        if(!$(reqFields[i]).hasClass('search')) {
            $(reqFields[i]).prop('required',required);
        }
    }
}




///////////////////////////////////////////////////
///////////////////////////////////////////////////
///////////////////////////////////////////////////


function checkboxChangesSearchParams(sender) {
    const linkIfChecked = $(sender).data('link-if-checked');
    const linkIfUnchecked = $(sender).data('link-if-unchecked');
    console.log(linkIfUnchecked);
    const checked = $(sender).prop('checked');

    if(checked) {
        window.location.search = linkIfChecked;
    }
    else {
        window.location.search = linkIfUnchecked;
    }
}