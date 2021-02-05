const select_customer_endpoint = "/orders/select_customer/";
const alter_cart_endpoint = "/orders/update_cart/";
const add_product_endpoint = "/orders/create/select_products/";
// ===========================================
// ===========================================
let cart = [];
// // // // // // //  
//  DUMMY - REMOVE / DUMMY - REMOVE / DUMMY - REMOVE / 
const dummy_products = [
    {
        "id": "3",
        "name": "Stan Locko's Coole Number 3",
        "quantity": 333,
        "categories": [
            {
                "id": 1,
                "name": "wheels"
            }
        ],
        "bottomPrice": 3.30,
        "price": 33.03
    },
    {
        "id": "2",
        "name": "Geile Scheisse 2",
        "quantity": 222,
        "categories": [
            {
                "id": 2,
                "name": "cars"
            }
        ],
        "bottomPrice": 2.02,
        "price": 22.20
    },
    {
        "id": "1",
        "name": "Krass 1",
        "quantity": 111,
        "categories": [
            {
                "id": 7,
                "name": "everything"
            }
        ],
        "bottomPrice": 1.10,
        "price": 11.00
    }
];

const dummy_template = '#product-template-el';
const dummy_parent = '#product-template-parent';

// // // // // // //  
//  DUMMY - REMOVE / DUMMY - REMOVE / DUMMY - REMOVE / 
//          /?redirect=


// context:
// userId = 
// ALLE productId = 

// userId = "2";
// productID = '3';
// action = 'add', 'remove', 'delete';

// const cart_dummy_data: {}

// ***********************************
// ***********************************
// customerId 
// EXISTING ORDER orderId 
// productId 
// action (increment, decrement, remove)


// SUCHE: EINES VON DIESEN 3:
// name = Kundenname (first / lastName)
// email = email Adresse
// mobile Number

// GIBT ZURUECK: ALLE 4:
// id = customerNo
// name = Kundenname (first / lastName)
// email = email Adresse
// mobile Number
// ***********************************
// ***********************************



{/* <td class='product-full-price'>
                <span class='for-calculation-item-quantity d-none'>
                    {{item.quantity}}
                </span>
                <span class='for-calculation-item-price d-none'></span> */}

// $(document).ready(function() {
//     let all_full_price_td = $('td.product-full-price');

//     for(i=0;i<all_full_price_td.length;i++) {
//         let quantity = $(all_full_price_td[i]).find(".for-calculation-item-quantity").html();
//         let price = $(all_full_price_td[i]).find(".for-calculation-item-price").html();
        

//         $(all_full_price_td[i]).html(price*quantity);
//     }
// });





// BACKOFFICE FUNCTIONS

/* #3 ADD ITEM TO MAIN LIST */
function loadAndUpdateMainList(newProduct, quantityAdded, productId=null, discountedPrice) {
    console.log('loadAndUpdateMainList');
    
    if (!newProduct) {
        let parent_el; 

        if(productId) {
            parent_el = $("#cart-main-list").find(`[data-product-id=${productId}]`); // this is the <tr> with the data-product-id attribute of the respective product
        }
        else {
            parent_el = $("#cart-main-list").find(`[data-product-id=${cart[0]['id']}]`); // this is the <tr> with the data-product-id attribute of the respective product
        }
        
        // const currentQuantity = $(parent_el).find(".product-quantity-field").val();
        // const newQuantity = parseInt(currentQuantity) + parseInt(quantityAdded); // calculate the new quantity after adding the one coming back from the server

        $(parent_el).find(".product-quantity-field").val(quantityAdded);

        cart.shift() // once the element has been added, remove it from the array so that it won't be double added the next time we run this loop
    }
    else { // if the added product is new, we should add a new row in the main list, if not, we should increase the existing row
        while(cart.length>0) {
            addItemsToMainList(cart[0], discountedPrice);
            cart.shift() // once the element has been added, remove it from the array so that it won't be double added the next time we run this loop
        }
    }
}

function addItemsToMainList(data, discountedPrice=null) {
    
    
    console.log('CART CART CART CART ');
    console.log(data);
    console.log('==================');

    let template = $('#template_main_product_list_el');
    let parent_element = $('#main_list_template_parent');

    console.log('#main_list_template_parent');

    // ***************************************

    $(template).find(".product-id").html(data["id"]);
    $(template).find(".product-name").html(data["name"]);
    $(template).find(".product-sku").html(data["sku"]);
    // $(template).find(".product-bottom-price").html(data["bottomPrice"]); // ##OLD
    $(template).find(".product-bottom-price").html(humanise(data["bottomPrice"]));
    // $(template).find(".product-price").html(data["price"]); // ##OLD
    
    if(discountedPrice) {
        $(template).find(".discount-price").html(humanise(discountedPrice));
    }

    $(template).find(".product-price").html(humanise(data["price"]));

    let temp_full_price = `${data["price"]*data["cart_quantity"]}`;
    $(template).find(".product-full-price").html(humanise(temp_full_price));

    // SETUP THE FIELD
    $(template).find(".product-quantity-field ").attr("id", `fieldFor${data["id"]}`);
    $(template).find(".product-quantity-field ").attr("data-quantity-field-for-id", data["id"]);
    ///////////////
    $(template).find(".product-quantity-field ").val(data["cart_quantity"]);
    //////////////
    $(template).find(".IMP-main-list-qt-btn").attr("data-target-field", `#fieldFor${data["id"]}`);
    $(template).find(".IMP-main-list-qt-btn").attr("data-id", data["id"]);
    
    if(data["cart_quantity"] == 1) { // if the quantity added is just 1, then the "-1"-Button should be "disabled", hence the class is added. If the quantity is >1, it should be enabled!
        $(template).find(".IMP-main-list-qt-btn.removeButton").addClass("disabled");
    }
    else {
        $(template).find(".IMP-main-list-qt-btn.removeButton").removeClass("disabled");
    }


    ////////////////////
    ////////////////////
    ////////////////////
    ////////////////////

    let new_el = $(template).clone();
    $(new_el).removeClass("d-none");
    $(new_el).attr("id", "");
    $(new_el).attr("data-product-id", data["id"]);

    $(parent_element).prepend($(new_el));
}

// ./BACKOFFICE FUNCTIONS





























//// // // // // // // // // 
var csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
//// // // // // // // // // 

function preventDefaultEvent(e,endpoint, sender) {
    e.preventDefault();
    processCustomerSearch(endpoint, sender);
}

function processCustomerSearch(endpoint, sender) { // this function is called once the user searches for a customer in the order/create URL
    // event.preventDefault();
    const targetFieldValue = $(sender.dataset.targetField).val();
    let data = {"name":"", "email":"","mobileNumber":""};

    var emailRegEx = new RegExp("[@]");
    var phoneRegEx = new RegExp("[0-9]");
    if (emailRegEx.test(targetFieldValue)) {
        data['email'] = targetFieldValue;
    }
    else if(phoneRegEx.test(targetFieldValue)) {
        data['mobileNumber'] = targetFieldValue;
    }
    else {
        data['name'] = targetFieldValue;
    }

    sendRequest(endpoint, data);
}

function processAddProductSearch(endpoint, sender, event) {
    event.preventDefault();

    let formData = $(sender).serializeArray();
    let data = {};
    for(i=0;i<formData.length;i++) {
        data[formData[i]['name']] = formData[i]['value'];
    }
    sendRequest(endpoint, data);
}


///////////////////////////////////////////////////////
// CALLBACKS


function searchCustomerCallback(res) {
    let customers = JSON.parse(res)["users"];
    
    $('#customer-table-body').empty(); // clear all child elements from the table

    if(customers.length>0) { // in case that no results came back, we want to keep the table empty
        $('#search-results-table').removeClass('d-none');
        $('#no-results-found').html(customers.length);
    }
    else {
        $('#search-results-table').addClass('d-none');
        $('#no-results-found').html('0');
    }

    for(i=0;i<customers.length;i++) {
        let template = $('#customer-item-TEMPLATE');
        $(template).children('.customer-name').html(`${customers[i]['first_name']} ${customers[i]['last_name']}`);
        $(template).children('.customer-email').html(customers[i]['email']);
        $(template).children('.customer-phone').html(customers[i]['mobileNumber']);
        $(template).attr('data-customer-id',customers[i]['id']);

        let newEl = $(template).clone();
        $(newEl).attr('id','');
        $(newEl).removeClass('d-none');
        $('#customer-table-body').prepend(newEl);
    }
}

function updateTotalPrice(product_id) {
    let el = $(`tr[data-product-id="${product_id}"]`);
    let new_quantity = $(el).find('input').val();
    let new_price = 0;


    let discount_price = $(el).find('.discount-price').html();
    discount_price = parseFloat(humanise(discount_price, 'to_machine'));

    if(!parseInt(discount_price)) { // means there is no discount price shown
        // new_price = parseFloat($(el).find('.product-price').html()); // ## OLD
        let temp = $(el).find('.product-price').html();
        new_price = parseFloat(humanise(temp, 'to_machine'));
    }
    else {
        new_price = parseFloat(discount_price);
    }

    new_price = parseFloat(new_price * new_quantity);

    // $(el).find('.product-full-price').html(new_price); // ##OLD
    $(el).find('.product-full-price').html(humanise(new_price));

    updateTotalCartPrice(); // after we have updated the product-full-price, we must also recalculate the entire cart price
}

function updateTotalCartPrice() {
    const all_full_price_elements = $('#cart-main-list .product-full-price'); // those are all the <span> elements containing the full price for each product (e.g. one product is $100, and you have 5 of that in your cart => product-total=$500) //// VERY IMPORTANT to keep #cart-main-list inside, because the empty template element has the same class name and would thus calculate the price wrongly

    let sum = 0.0;

    console.log('all_full_price_elements.length');
    console.log(all_full_price_elements.length);

    for(let i = 0; i<all_full_price_elements.length;i++) {
        let innerHtml = $(all_full_price_elements[i]).html();
        innerHtml = humanise(innerHtml.trim(), "to_machine"); // the innerHtml must be trim() to remove the space
        innerHtml = parseFloat(innerHtml); // it must still be parsed to float

        if(innerHtml) { // this check is required, because sometimes humanise() will return NaN, which will mess up the entire sum
            sum += innerHtml;
        }
    }

    $('.cart-total').html(humanise(sum)); // the sum must be humanise() again, to make it human readable
}

function alterCartCallback(res) {
    let resData = JSON.parse(res);

    console.log('DATA DATA DATA DATA ');
    console.log(resData);

    loadAndUpdateMainList(resData.newProduct, resData.numProducts, resData.productId, resData.discountedPrice); // the loadAndUpdateMainList() function will act differently depending on whether the product added is a new product or not. I fi IS a new product, a new Zeile will be added - if not, the existing Zeile will be increased
    
    if(resData['quantity']==0) {
        let rowToDelete = $(`#cart-main-list tr[data-product-id="${resData['productId']}"]`); // the BackOffice-table contains each product-list item in a <tr>
        rowToDelete.remove();
    }
    else {
        const targetField = `#fieldFor${resData['productId']}`; // in HTML, each field has an ID which is called "fieldFor<productID>" => therefore, we can find the same field like this
        // $(targetField).val(resData['quantity']); // ##
    }

    updateTotalPrice(resData['productId']); // this updates the UI to showcase the new price after updating the quantity
}

function updateTotalCartCountCF(userCartLength) {
    const cartCounterEl = $('#cartCounter');
    $(cartCounterEl).html(userCartLength);
}


function updateTotalProductPriceCF(product_id) { // this function updates the total price of that product, based on the new quantity that the user has entered
    let el = $(`.CART-LIST-ITEM[data-product-id="${product_id}"]`);
    let new_quantity = $(el).find('input').val();

    // let new_price = parseFloat($(el).find('.price-per-item').html()); //// this is how I used to do it before I tried the code in the next line
    let new_price = $(el).find('.price-per-item').html();
    new_price = parseFloat(new_price.replace(",","")); // this is required to parse the number from a human-readable format

    new_price = parseFloat(new_price * new_quantity);

    new_price = new_price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); // this is required to make the new price human readable again, e.g. 100000 => 100,000
    $(el).find('.product-total-price').html(new_price);
}

function updateCartTotalPriceCF() { // this function recalculates the price of all cart-items, so that the price is adjusted whenever the amount of items inside the cart is adjusted
    const total_product_prices = $(".product-total-price"); // the <span> with class='product-total-price' contains the total price for each product
    const cart_total_el = $('#cart_total_number');

    let new_cart_total_price = 0; // holds the new price of ALL items in the cart

    for(let i=0;i<total_product_prices.length;i++) {
        let current_el = $(total_product_prices[i]).html();
        
        current_el = current_el.replaceAll(/,/g, "");

        current_el = parseFloat(current_el.replace(",","")); // this is required to parse the number from a human-readable format

        new_cart_total_price += parseFloat(current_el);
    }

    new_cart_total_price = new_cart_total_price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    cart_total_el.html(new_cart_total_price);
}

function alterCartCallbackCF(res) { // this is the alterCartCallback which is called when the alterCart-API is called from the customer-facing side
    let resData = JSON.parse(res);

    if(!window.location.pathname.includes('/cart')) { // the modal should only be shown if users are NOT ALREADY on the cart page!
        $('#addedToCartModal').modal('show'); // this shows the "Go-To-Cart"-MODAL
    }


    updateTotalCartCountCF(resData["numProducts"]); // CHECK wehther this works

    if(resData['quantity']==0) {
        let rowToDelete = $(`.CART-LIST-ITEM[data-product-id="${resData['productId']}"]`);
        rowToDelete.remove();
    }
    else {
        const targetField = `#fieldFor${resData['productId']}`; // in HTML, each field has an ID which is called "fieldFor<productID>" => therefore, we can find the same field like this
        $(targetField).val(resData['numProducts']);
    }

    try {
        updateTotalProductPriceCF(resData['productId']);
    }
    catch(err) {
        console.log(err);
    }

    updateCartTotalPriceCF();
}

/* #1 PROCESS POPUP SEARCH */ 
function addProductCallback(res) { // 1. processes the products-popup search bar

    let data = JSON.parse(res);

    data = data['products'];

    addItemsToPopUpList(data);

    // all of those items here should be populated via the CART_ARRAY global variable, rather than via parameters

    // create the whole product list and shit
    
    // addMainListItem(); // this function has to be called from cart_new.js
}

/* #2 PROCESS POPUP SEARCH */
function addItemsToPopUpList(new_data) { // 2. this takes the response 

    let template = $('#product-template-el');
    let parent_element = $('#product-template-parent');

    // clean out the container element first, so that all existing elements inside are removed
    $(parent_element).empty();

    // ***************************************
    for(d=0;d<new_data.length;d++) {

        $(template).attr("data-all-info", JSON.stringify(new_data[d])); // this attribute stores all the info related to the product, so that it can be retrieved later when we add the elements

        let data = new_data[d];

        $(template).attr("data-product-id", data["id"]);
        $(template).find(".product-name").html(data["name"]);

        // ***************************************
        $(template).find(".product-available-quantity").html(data["quantity"]);

        // *******************************
        // ADJUST FIELD

        $(template).find('.popup-quantity-field').attr('id', `popupFieldFor${data["id"]}`);
        let popupAddQuantButton = $(template).find('.product-add-button');
        $(popupAddQuantButton).attr("data-target-field", `#popupFieldFor${data["id"]}`);
        $(popupAddQuantButton).attr("data-id", data["id"]);

        // ***************************************

        $(template).find(".product-bottom-price").html(humanise(data["bottomPrice"]));
        // $(template).find(".product-price").html(data["price"]); // ##OLD
        $(template).find(".product-price").html(humanise(data["price"]));

        // ***************************************

        $(template).find(".product-categories").html(''); // empty this field first because it is still filled from the previous template
        for(i=0;i<data["categories"].length;i++) { // for each category, one pill must be added

            let existing_data = $(template).find(".product-categories").html();

            if(i==0) { // if it's the first element, don't add the COMMA
                $(template).find(".product-categories").html(`${data["categories"][i]['name']}`);
            }
            else {
                $(template).find(".product-categories").html(`${existing_data}, ${data["categories"][i]['name']}`);
            }
        }

        let new_el = $(template).clone();
        $(new_el).removeClass("d-none");
        $(new_el).attr("id", "");

        $(parent_element).prepend($(new_el));
    }

}

/////////////////////////////////////
// SEND AJAX

function sendRequest(endpoint, data) {
    // code required for CSRF
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    // if request depending on the type of data we sent + endpoint
    if (endpoint == select_customer_endpoint) {
        executeAjax(endpoint, data, searchCustomerCallback);
    }
    else if (endpoint == alter_cart_endpoint) {

        let newData = {};
        newData["userId"] = parseInt(data.dataset.userId); // Django backend is expecting the ID to be an integer value
        newData["productId"] = parseInt(data.dataset.id); // Django backend is expecting the ID to be an integer value

        if(data.dataset.action == 'add' || data.dataset.action == 'addCF') {
            newData['quantity'] = 1;
            /////////////////////////////
            let field;
            let field_parent;
            let minus_button
            if(data.dataset.action == 'addCF') { // CF and BO have different names for the field
                field = $(data).closest('.quantity-field');
                minus_button = $(field).find('.disabled');
            }
            else {
                field = $(data).closest('.product-quantity-field');
                field_parent = $(data).closest('.product-quantity');
                minus_button = $(field_parent).find('.disabled');
            }
            $(minus_button).removeClass('disabled'); // once we add more than 1 products, the minus-button should work again. Whenever the  product-quantity reaches 1, the minus-button is disabled, so that users cannot go to zero products (they should use the delete button instead). But once we go above 1 product, we must also enable the button again
            /////////////////////////////
        }
        else if(data.dataset.action == 'remove' || data.dataset.action == 'removeCF') {
            const currentVal = parseInt($(data.dataset.targetField).val()); // the value the field currently holds
            
            if((currentVal-1) == 1) { // if the value is about to go to 1, the "minus-button" should no longer work, so that users can't go to 0 items
                $(data).addClass('disabled'); // for the button to no longer work, we must disable it
            }
            newData['quantity'] = -1;
        }
        else if(data.dataset.action == 'addToCart' || data.dataset.action == 'addToCartCF') { // CF = customer-facing, which needs a slightly different button
            newData['quantity'] = parseInt($(data.dataset.targetField).val()); // if we add it to the cart, then the targetField already contains the correct amount
        } 
        else if(data.dataset.action == 'delete' || data.dataset.action == 'deleteCF') {
            newData['quantity'] = parseInt(0);
        }

        // newData['quantity'] = parseInt(newData['quantity']); // Django-Backend braucht ein Integer

        if($(data).attr("data-action") == "addToCart") { // this should only be called if the quantity is updated from the popup list button - because we also need to add a list item in the background            
            let sender = $(data);
            let parent = $(sender).closest('tr');
            let all_product_info = JSON.parse($(parent).attr("data-all-info"));
            
            console.log('all_product_info');
            console.log(all_product_info);
            console.log('newData');
            console.log(newData);
            
            
            all_product_info['cart_quantity'] = newData['quantity'];

            cart.push(all_product_info);
        }

        if(data.dataset.action == 'addCF'  || data.dataset.action == 'removeCF' || data.dataset.action == 'addToCartCF' || data.dataset.action == 'deleteCF') { // if the actions contains the "CF", it comes from the customer-facing side, not the backoffice side, meaning that we should call the CF-callback which takes care of the customer-facing UI
            executeAjax(endpoint, newData, alterCartCallbackCF);
        }
        else {
            executeAjax(endpoint, newData, alterCartCallback);
        }
    }
    else if (endpoint == add_product_endpoint) {
        executeAjax(endpoint, data, addProductCallback);
    }
    else {
        console.log('no endpoint provided');
    }
}

function executeAjax(endpoint, data, callback) {
    $.ajax({
        url: endpoint,
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),
        dataType: 'text',
        success: function(res) {
            callback(res);
        },
        error: function(err) {
            console.log(err);
        }
    });
}






////// UI-Functions


function customerSelected(sender) {
    const customerId = sender.dataset.customerId;
    console.log(customerId);
    console.log('URL');
    const url = `${window.location.href}${customerId}`;
    window.location.assign(url);
}

function addElementFromAJAX(data, template, parent) {

    for(let i=0;i<data.length;i++) {
        for (const [key, value] of Object.entries(data[i])) {
            try {
                $(template).find(`span[data-${key}]`).html(value);
            } catch (err) {
                console.log('MY-Error, Non-Critical: No target element provided:');
                console.log(err);
            }
        }

        let newEl = $(template).clone();
        $(newEl).removeClass('d-none');
        $(newEl).attr("id","");
        $(newEl).attr("data-id",data[i]['id']); // this adds the id provided as a "data-id" attribute

        $(parent).prepend(newEl);
    }
}