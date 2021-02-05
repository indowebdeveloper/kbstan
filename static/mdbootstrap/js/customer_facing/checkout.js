// HANDLING THE MAIN FORM

function showNewAddressForm(show) {
    if(show) {
        $('#newAddressForm').show();
    }
    else {
        $('#newAddressForm').hide();
    }

    showRequiredAddressFields(show);
}

function showRequiredAddressFields(required) {
    const reqFields = $('#newAddressForm input, #newAddressForm select');
    for(let i=0;i<reqFields.length;i++) {
        $(reqFields[i]).prop('required',required);
    }
}

// =========================
// =========================
// =========================
// HANDLING THE INDODANA PAYMENT PERIOD FORM

// =========================
// =========================
// =========================
// HANDLING THE Shipping SELECTION radios

function selectShippingRadio(sender) {
    simulateClick(sender); // this is to "click" on the other tab which will reveal the specific form

    let make_required = $(sender).data('make-required');
    let make_not_required = $(sender).data('make-not-required');

    console.log('=== MAKE REQUIRED ===');
    console.log(make_required);
    console.log(make_required == '#store_pickup_form');
    if(make_required == '#store_pickup_form') {
        // showNewAddressForm(false); // #CHANGE
    }

    showHideRequiredFields(make_required);
    showHideRequiredFields(make_not_required, required=false);
}

function showIndodanaPeriodForm(show) {
    if(show) {
        $('#div_id_installment_period').show();
        $('#indodana_disclaimer').show(); // this element contains the disclaimer message for Indodana. It should also only be shown when the Indodana form is shown
    }
    else {
        $('#div_id_installment_period').hide();
        $('#indodana_disclaimer').hide(); // this element contains the disclaimer message for Indodana. It should also only be shown when the Indodana form is shown
    }
    requireIndodanaFields(show);
}

function requireIndodanaFields(required) {
    const reqFields = $('#id_installment_period input, #id_installment_period select');
    for(let i=0;i<reqFields.length;i++) {
        $(reqFields[i]).prop('required',required)
    }
}


// =========================
// =========================
// =========================
// HANDLING THE STORE SELECTION FORM

function showPaymentStoreForm(show) {
    if(show) {
        $('#div_id_payment_store').show();
    }
    else {
        $('#div_id_payment_store').hide();
    }
    requirePaymentStoreFields(show);
}

function requirePaymentStoreFields(required) {
    const reqFields = $('#id_payment_store input, #id_payment_store select');
    for(let i=0;i<reqFields.length;i++) {
        $(reqFields[i]).prop('required',required)
    }
}

// =========================
// =========================
// =========================
// HANDLING THE Bank SELECTION FORM

function showBankForm(show) {
    if(show) {
        $('#div_id_bank_name').show();
    }
    else {
        $('#div_id_bank_name').hide();
    }
    requireBankFields(show);
}

function requireBankFields(required) {
    const reqFields = $('#id_bank_name input, #id_bank_name select');
    for(let i=0;i<reqFields.length;i++) {
        $(reqFields[i]).prop('required',required)
    }
}

// =========================
// =========================
// =========================



// Attaches all the event-handlers on page_load

$(document).ready(function() {
    showHideRequiredFields('#store_pickup_form', false);
    showHideRequiredFields('#shipping_form', true); // the shipping_form field must be forced to be made required - else, a customer could submit an order without an address

    showIndodanaPeriodForm(false);
    showPaymentStoreForm(false);
    if($('#newAddressForm').attr('data-new-address-required') == "false") { // if there is no existing addresses, then this data-attr. will be set to FALSE, which means that the new address form shouldn't be shown (since the user has existing addresses to select from). However, if there is NO existing addresses, the customerAddressCreateForm should be SHOWN and it MUST BE MANDATORY fields. Thus, in the else{}-condition, it is forced to be shown.
        showNewAddressForm(false); 
    }
    else {
        showNewAddressForm(true);
    }

    $("[name=payment_method]").val('Bank Transfer');

    $("[name=payment_method]").change(function(event) {
        const val = $(event.target).val();

        // hide all sub-fields first
        showIndodanaPeriodForm(false);
        showPaymentStoreForm(false);
        showBankForm(false);
        // end-hide

        if(val == 'Indodana') {
            showIndodanaPeriodForm(true);
            
            showPaymentStoreForm(false); // hide all payment store fields, if they are there
            showBankForm(false); // hide all bank-related fields, if they are there
        }
        else if(val == 'Payment in the store') {
            showPaymentStoreForm(true);

            showIndodanaPeriodForm(false); // hide all indodana-related fields, if they are there
            showBankForm(false); // hide all bank-related fields, if they are there
        }
        else if(val == 'Bank Transfer') {
            showBankForm(true);
            
            showPaymentStoreForm(false); // hide all payment store fields, if they are there
            showIndodanaPeriodForm(false); // hide all indodana-related fields, if they are there
        }
    });
});