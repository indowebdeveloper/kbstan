$( document ).ready(function() {
    let url = window.location.search;
    url = url.slice(1);

    let filters = url.split('&');
    for(let x=0;x<filters.length;x++) {
        let filter = filters[x].split('=');
        let filter_name = filter[0];
        let filter_value = filter[1];

        console.log("filter_name");
        console.log(filter_name);
        console.log("filter_value");
        console.log(filter_value);

        if(filter_name=='q') {
            console.log('SEARCH!!!');
            $('#search').val(filter_value);
            $('#hidden_search').val(filter_value); // the #hidden_search field must be updated too - it is a invisible field in the filters list - so that when you submit filters, the search will also be resubmitted
        }
        else if(filter_name != 'price_min' && filter_name != 'price_max') {
            filter_value = filter_value.replaceAll(/\+/g, " "); // this is to take out any "+" which occur if the name has a space, e.g. "Geiles Auto" => "Geiles+Auto"
            $(`[value="${filter_value}"]`).prop('checked', true);
        }
        else {
            $(`#${filter_name}`).val(filter_value);
        }
    }
});

function resetFiltersForm(sender) {
    const reset_target = $(sender).attr('data-reset-target');
    $(reset_target).trigger("reset");
    // location.reload();
}