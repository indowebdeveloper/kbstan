function convertFormIntoObject(form) { // this function takes a form element and returns the data from all fields in object form
    const formFields = $(form).serializeArray();
    console.log('form fields');
    console.log(formFields);
    let data = {};
    for (let item in formFields) {
        data[formFields[item]['name']] = formFields[item]['value'];
    }

    return data;
}

function newItemCallback(result, sender) {
    let data = JSON.parse(result); // parses the stringified JSON for easier access of properties

    console.log(result);

    if(data.status != 'SUCCESS') {
        alert(`Item not created: ${data.status}`);
    }
    else {
        const template_item_name = $(sender).attr('data-item-template');
        const template_item = $(template_item_name);
        let new_item = template_item.clone();

        // customise the new element
        $(new_item).attr('id','');
        $(new_item).removeClass('d-none');
        
        for(let key in data) {
            $(new_item).find(`.${key}`).html(data[key]); //classname must match result-dict's key! then the html is replaced with the value
            $(new_item).find(`.${key}`).val(data[key]); // this is to fill the corresponding text field (same class name) with the value as well
        }

        const idName = $(sender).attr('data-item-id-name'); // this data-*-attr. denotes the name of the field where the new item's ID is stored, i.e. "attributeID", "brandID"
        $(new_item).attr('data-item-id',data[idName]); // now I can set the <tr>'s data-item-id to the value of the item's ID in the database

        const parent = $(template_item).closest(`.${template_item_name.slice(1) + '-parent'}`); // the parent element, into which the new el. should be added into, has the same name plus a '-parent'. slice(1) is required, because template_item_name is stored as "#tr-...", so we must remove the hash first
        $(parent).prepend(new_item);
        console.log('parent');
        console.log(parent);
    }
}

function addNewItem(e, sender) {
    e.preventDefault(); // if not, it will simulate a SUBMIT

    $(sender).prop('disabled', true); // because the button simultaneously acts as a submit button, it must stay disabled until something has been typed in the <input>

    const inputs = $(sender).closest('.input-group').children('input');

    if($(sender).hasClass('ready-to-submit')) { // if the button has this class, then the request should be sent out
        // TODO: IMPLEMENT SERVER REQUEST

        $(sender).prop('disabled', false); // the button will go back to its original form and must be enabled again
        
        let formFields = $(sender).closest('form').serializeArray();
        let data = {};
        for (let item in formFields) {
            data[formFields[item]['name']] = formFields[item]['value'];
        }
        $(inputs).val(''); // clear all text fields to be ready to take new values

        const url = $(sender).attr('data-api-endpoint');
        sendServerRequest(url, data, newItemCallback, additionalData=sender);
    }

    // if(readyToSubmit) { // this parameter defines whether the 'ready-to-submit' class should be added after this interaction
        $(sender).toggleClass('ready-to-submit');
    // }

    $(sender).toggleClass('show-details'); // this is to make the button say only "Add", rather than "Add Whatever"
    $(sender).parent().toggleClass('w-100');
    $(sender).parent().toggleClass('input-group-append');

    $(inputs).toggleClass('d-none');
    $(inputs).first().focus();
}

function removeItem(data,sender) {
    $(sender).closest('tr').remove();
}

function editItemCallback(result, sender) {
    let data = JSON.parse(result); // parses the stringified JSON for easier access of properties
    
    const el = $(sender).closest('tr'); // this is the row element that needs updating


    if(data.status != 'SUCCESS') {
        alert(`${data.status}: Edited item already exists`);
    }
    else {
        for(let key in data) {
            $(el).find(`.${key}`).html(data[key]); //classname must match result-dict's key! then the html is replaced with the value
        }
    }
}

function editItemUI(e, sender) {
    e.preventDefault();

    let el = $(sender).closest('div').siblings('.displayMode'); // the "Edit/Delete"-buttons are in a sibling div
    $(el).find('input').focusin();
    if (el.length == 0) {
        el = $(sender).closest('.editMode') // however, the "Cancel/Save"-buttons are within the parent div. So if el.length = 0, it means that no elements have been found (which means that the sender is not within the sibling-div, but within the parent div)
    }
    const item_id = $(sender).closest('tr').attr('data-item-id');
    
    $(el).toggleClass('displayMode');
    $(el).toggleClass('editMode');

    if($(sender).attr('type') == 'submit') {
        const url = $(sender).attr('data-api-endpoint');
        let data = convertFormIntoObject( $(sender).closest('form') );
        data[$(sender).attr('data-item-id-name')] = item_id; // the sender attribute contains the name of the ID that needs to be submitted
        sendServerRequest(url,data,editItemCallback,sender);
    }
}

function alterItem(sender, actionType) {
    const row_el = $(sender).closest('tr');
    const item_id = $(row_el).attr('data-item-id');
    const id_name = $(row_el).attr('data-item-id-name');
    console.log(id_name);
    let url = '';

    switch(actionType) {
        case 'edit':
            editItemUI(sender);
            break;
        case 'delete':
            if (confirm('Are you sure you want to DELETE this item? This will affect all associated products too')) {
                url = $(sender).attr('data-api-endpoint');
                let data = {}; // Step 1: This is a two-step process, because I can directly use JS-variables as dictinary keys
                data[id_name] = item_id; // Step 2
                console.log('DATA');
                console.log(data);
                sendServerRequest(url,data,removeItem,sender);
              } else {
                // Do nothing!
                console.log('Nothing was deleted');
              }
            break;
        default:
            alert('Action not supported');
    }
}

function typingAction(sender, action) { // this function enables/disables the button depending on whether the field is empty or not
    const typing_target = $(sender).attr('data-typing-action-target');
    const target_element = $(typing_target);

    if(action=='disableWhenEmpty') {
        if(sender.value == '') {
            $(target_element).prop('disabled', true);
        }
        else {
            $(target_element).prop('disabled', false);
        }
    }
}