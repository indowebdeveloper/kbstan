// products/?price_max=400
// products/?price_max=400&categories=Wheels
// products/?categories=Wheels


// =====================
// =====================
// =====================
// Global State Variable keeps track of all the filters
let filters = {
    "categories": {
    },
    "brands": {
    },
    "price_min": 0,
    "price_max": 0,
    "sort_by": ""
}

// =====================
// =====================
// =====================


function change_product_per_page(sender) {
    const showPerPage = sender.value;
    alert(`Show ${showPerPage} per page!`);
}


// =====================
// =====================
// =====================


function handle_filters(e, sender) {
    e.preventDefault();

    let formData = $(sender).closest('form').serialize();

    let search = location.search; // extract all additional parameters;

    let q_start = search.indexOf('q'); // this searches for where the q-query starts
    let q_end = search.indexOf("&", q_start); // this searches for the first "&" coming after the "q", which indicates the start of a new search parameter. Example: /?q=product&price=100

    let new_search = '';


    if(q_start == -1) {
        console.log('no prior search');
    }
    else if(q_end == -1) { // means that "q" is the last parameter
        new_search = search.slice(q_start);
    }
    else { // this means that "q" is somewhere in the middle, and we must slice at the start and end
        new_search = search.slice(q_start, q_end);
    }
    
    location.replace(`/products/?${formData}&${new_search}`);
}


// =====================
// =====================
// =====================

function determineLastUrlFilterPosition(url) { 
    // this function takes the last filter in the url (price_max) and cuts off any string coming after that (as anything coming after the "&" will be related to the search, not the filters)
    // *** Example: ***
    // URL = /products/?categories=Wheels&price_max=123123235&&q=pro
    // In this case, we must find the position of the first "&" that comes after the "price_max" in the URL and cut off the string after that
    let new_url = "";
    let start_of_search = url.indexOf("price_max"); // this is our search start point
    let end_of_filters = url.indexOf("&", start_of_search); // this is the position of the "&" coming after "price_max"

    if(end_of_filters == -1) {
        new_url = url;
    }
    else {
        new_url = url.slice(0, end_of_filters); // now we cut the url from the very start until the point where the filters end (which is the location in the string of the first "&" after "price_max") 
    }

    return new_url;
}

function retrieveFiltersFromURL() { // this retrieves the filters from the URL and automatically updates the local state
    // sample URL: http://165.22.58.179/products/?categories=Wheels&categories=Glass&price_min=168000&price_max=651000&brands=Mercedes-Benz&brands=Toyota
    let url = window.location.search.split("?")[1];

    try {
        url = determineLastUrlFilterPosition(url);
    }
    catch(err) {
        console.log('no "&" found. filters function as expected');
    }

    let filter_pairs = url.split("&");


    for(pair in filter_pairs) {
        const p = filter_pairs[pair].split("=");
        const filter_category = p[0];
        let filter_name = p[1];

        if(filter_category=='price_min' || filter_category=='price_max' || filter_category=='sort_by') { // this is needed because the 'filter-categories' mentioned here are the only ones which are not tick-boxes
            filters[filter_category] = filter_name;
        }
        else {
            // first, check if the name contains any '+', and replace them with spaces ('+' is the replacement for 'space' in the url)
            while(filter_name.search(/\+/g) != -1) { // str.search() returns -1 if no more "+" is found. Need to run this loop until all + are replaced.
                // filter_name = filter_name.replace("+"," ");
                filter_name = filter_name.replaceAll(/\+/g, " ");
            }
            try {
                filter_name = filter_name.replaceAll(/%20/g, ' ');
                filters[filter_category][filter_name] = true;
            }
            catch(err) {
                console.log('Error: COMMENTED OUT - CHECK CODE TO PRINT ERROR');
                // console.log(err);
            }
        }
    }
}

// =====================
// =====================
// =====================

function updateFiltersUI() {
    const newMinPrice = filters['price_min'] == 0 ? 1000 : filters['price_min']; // this makes sure that the slider isn't messed up if the URL does NOT contain the min/max_price. E.g. when you are forwarded to products page from clicking on a promotion, the slider would be messed up, because no value is provided. This way, there is always a min/max value provided
    const newMaxPrice = filters['price_max'] == 0 ? 999999999 : filters['price_max'];
    
    /*******************/
    /******** I HAVE REMOVED THE RANGE SLIDER ***********/
    // let my_range = $(".js-range-slider").data("ionRangeSlider"); // setup the variable for IonRangeSlider to update the handlerSlides
    // 3. Update range slider content (this will change handles positions)
    // my_range.update({
    //     from: parseFloat(newMinPrice), /* divide by a thousand because the filterUI and actual price are off by 1000 to account for the large numbers in Indonesian Rupiah. */
    //     to: parseFloat(newMaxPrice)
    // });
    /*******************/
    /******** I HAVE REMOVED THE RANGE SLIDER ***********/


    /*******************/
    // setting the price filters first // 
    // this needs us to set two fields each for min and max price
    $('#filters_price_min').val(newMinPrice); // this is the hidden field that keeps track of the current price_min
    $('#filters_price_max').val(newMaxPrice); // this is the hidden field that keeps track of the current price_max
    
    
    $('#hidden_sort_by').val(filters['sort_by']); // this is the hidden sort_by field that allows the sort_by dropdown to be submitted with the form, even tho the dropdown that's visible to the user is in the top right corner
    updateHiddenForm($('#hidden_sort_by'), resubmitTargetForm=false);
    /* ********************************** */
    /* ********************************** */
    /* ********************************** */

    for(let value in filters['categories']) {
        $(`[name=categories][value="${value}"]`).prop("checked", true);
    }
    for(let value in filters['brands']) {
        $(`[name=brands][value="${value}"]`).prop("checked", true);
    }
}


// =====================
// =====================
// =====================
// call functions on document load

$(document).ready(function() {
    retrieveFiltersFromURL(); // retrieves the stored filters from the URL and stores them in a global variable
    updateFiltersUI(); // this function updates the UI
});


// ==============================
// Updating the hidden sorting field

function updateHiddenForm(sender, resubmitTargetForm=true) { 
    // this function is necessary because there is two "sort-by"-fields - one that is designed correctly, and one that is hidden within the filters-<form>-tag, so that it is submitted with the other filters
    // ABOUT THE resubmitTargetForm PARAMETER => this parameter is required, because sometimes when we update the field, we WANT the form to be resubmitted (e.g. when the user changes his/her selection) and sometimes we do not want it to reload the page (e.g. when the value is automatically changed). Since the default is that the form SHOULD be resubmitted, it is set to TRUE and only has to be changed in case you want to automatically change the value, but not resubmit the form.

    const target = $(sender).data('update-target');
    $(target).val($(sender).val());

    if(resubmitTargetForm) {
        $('#filters_form').trigger('submit'); // this form should be submitted each time, so that the products will automatically re-sort
    }
}