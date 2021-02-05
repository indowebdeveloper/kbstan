function stepperButtonClicked(sender) {
    let productId = sender.dataset.product;
    let targetField = sender.dataset.target;
    let action = sender.dataset.action;

    if($(targetField).val() == 1 && action == 'remove') {
        alert('Quantity must be 1 or greater!');
        return; // returns immediately, so that user cannot change value below 1
    }

    if(user === 'AnonymousUser'){
        console.log('User is not logged in')
    } else{
        updateUserOrder(productId, action, targetField, sender)
    }
}
 
function updateUserOrder(productId, action, targetField, sender){
    var url = '/orders/update_cart/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        if(data=='cart updated') {
            let pricePerProduct = sender.dataset.pricePerProduct;
            let productTotalTarget = sender.dataset.productTotalTarget;
            let cartTotalTarget = sender.dataset.cartTotalTarget;

            let currentVal = $(targetField).val(); // this field stores the current quantity of a given product in the cart

            let cartTotal = parseFloat( $(cartTotalTarget).html() ); // parseFloat to ensure that it's not a string by accident

            console.log('BEGINNING cartTotal');
            console.log(cartTotal);


            if(action=='add') {
                $(targetField).val(++currentVal); // increment the value of the quantity field

                cartTotal += parseFloat(pricePerProduct); // increase the cart total by the price/product
            }
            else if(action=='remove') {
                $(targetField).val(--currentVal); // decrement the value of the quantity field

                cartTotal -= parseFloat(pricePerProduct); // decrease the cart total by the price/product
            }

            else if(action='delete') {

                cartTotal -= $(targetField).val() * pricePerProduct; // subtracts the product total from cart total

                $(targetField).closest('.CART-LIST-ITEM').remove();
            }

            if(action=='add' || action=='remove') {
                //////////// update the product total - this must come at the end, so that the new, updated field value is reflected
                const newProductTotal = $(targetField).val() * pricePerProduct; // use the quantity and price per product to calc new product total
                $(productTotalTarget).html(newProductTotal); // change HTML to reflect new product total
                ////////////
            }

            $(cartTotalTarget).html(cartTotal);
        }
    });
} 




//==============================================================================
//==============================================================================
//==============================================================================

// New implementation of cart functionality

// ***** CONSTANTS *****

const alter_cart_endpoint = "/orders/update_cart/";

//// // // // // // // // // 
var csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
//// // // // // // // // // 


// ***** CALLBACKS *****

// *********************


/////////////////////////////////////
// ***** SEND AJAX *****

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

        if(data.dataset.action == 'add') {
            newData['quantity'] = parseInt($(data.dataset.targetField).val()) + 1; // "+1" is needed, because the field contains the current value, which we want to increment by one
        }
        else if(data.dataset.action == 'remove') {
            newData['quantity'] = parseInt($(data.dataset.targetField).val()) - 1; // "-1" is needed, because the field contains the current value, which we want to increment by one
        }
        else if(data.dataset.action == 'addToCart') {
            newData['quantity'] = parseInt($(data.dataset.targetField).val()); // if we add it to the cart, then the targetField already contains the correct amount
        }
        else if(data.dataset.action == 'delete') {
            newData['quantity'] = parseInt(0);
        }
        else if(data.dataset.action == 'addQuantityOne') {
            newData['quantity'] = parseInt(1);
        }

        newData['quantity'] = parseInt(newData['quantity']); // Django-Backend braucht ein Integer

        console.log('CART DATA');
        console.log(newData);

        executeAjax(endpoint, newData, alterCartCallback);
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