function handle_search(e, sender) {
    e.preventDefault();

    let formData = $(sender).closest('form').serialize();

    if (location.pathname == "/products/") { // if we are already on the /products/ page, we need to preserve the filters
        let search = location.search; // extract all additional parameters;

        let q_start = search.indexOf('q'); // this searches for where the q_query starts
        let q_end = search.indexOf("&", q_start); // this searches for the first "&" coming after the "q", which indicates the start of a new search parameter. Example: /?q=product&price=100

        let filters = ''; // this is where the filters will be stored

        if(q_start == -1) { // no prior search has been launched, so just accept filters as they are
            filters = search; // if no "q" has been found (indexOf('q')=-1), then no slicing needs to be done from the search parameter
        }
        else if(q_end == -1) { // if q_end = -1, it means that no "&" was found after the "q", meaning that "q" is the last search-parameter
            filters = search.slice(1, q_start); // under this condition, we can slice from the start of the string until the "q"
        }
        else {
            filters = search.slice(q_end+1); // if we can find a "q_end", that means that there is a "&" after the "q"-parameter, meaning that it is the first parameter.
        }

        if(filters.indexOf('?') == -1) {
            location.replace(`/products/?${filters}&${formData}`);
        }
        else {
            filters = filters.slice(1);
            location.replace(`/products/?${filters}&${formData}`);
        }
    }
    else {
        location.replace(`/products/?${formData}`);
    }
}