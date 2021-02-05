
// ===========================
// ===========================
// ===========================
// ===========================
// ===========================
// ===========================
// UI-INTERACTION FUNCTIONS

function newCarSelected(e) {
    GLOBAL_SELECTED_BRAND["brandName"] = $(e).attr('data-brand');
    GLOBAL_SELECTED_BRAND["brandID"] = $(e).attr('data-id');
    document.querySelector('body').dispatchEvent(carHasSelected);
}
// ===========================
// ===========================
// ===========================

function toggleTargetHideSelf(sender, focusTarget=null) {
    $(sender).addClass('d-none');
    const toggleTarget = $(sender).attr('data-toggle-target');

    $(toggleTarget).removeClass('d-none');

    if(focusTarget) {
        $(focusTarget).focus();
    }
}

function fieldReset(hideTarget, showTarget) {
    // $(hideTarget).addClass('d-none');
    // $(showTarget).removeClass('d-none');
    setTimeout(
        function(){ 
            $(hideTarget).addClass('d-none');
            $(showTarget).removeClass('d-none');
        }, 
    300);
}

function newBrandFieldToggler(e, sender) {
    e.preventDefault();

    console.log('CLICKED');

    const hidingForm = $(sender).closest('form'); // make the whole form for inputing new brands invisible again
    const toggleTarget = $(sender).attr('data-toggle-target'); // this attribute contains the name of the element that should be made visible again
    fieldReset(hidingForm, toggleTarget);

    submitNewBrand($('input#newBrand').val());

    $('input#newBrand').val('');
    $('#showNewBrandButton').prop('disabled',false); // we have just emptied the val() of input#newBrand => this will disable the 'Add'-Button, therefore, we must manually re-enable it
}

function newModelFieldToggler(e) {
    e.preventDefault();

    $('#newModel input').toggleClass('d-none');
    $('#newModel input').first().focus();

    $('#showNewModelButton').prop('disabled',true); // because the modelName-field will be empty at first, so we must manually disable the button

    // this IF is only called after the second time the button is clicked, because the 'ready-to-submit' class is only toggled later
    if($('#showNewModelButton').hasClass('ready-to-submit')) {
        const modelName = $('#newModel input[name="modelName"]').val();
        const modelYear = $('#newModel input[name="modelYear"]').val();
        const modelDetails = $('#newModel input[name="modelDetails"]').val();

        submitNewModel(modelName, modelYear, modelDetails, GLOBAL_SELECTED_BRAND['brandID']);

        $('#newModel input').val('');
        $('#showNewModelButton').prop('disabled',false); // we have just emptied the val() of input#newModel => this will disable the 'Add'-Button, therefore, we must manually re-enable it
    }

    $('#showNewModelButton').toggleClass('ready-to-submit');
}

function addNewBrandListItem(brandID,brandName) {

        // fill out the template data-* attributes and HTML content
        let brandListItemTemplate = $('#TEMPLATE_brand_table_ELEMENT');
        $(brandListItemTemplate).attr({'data-brand':brandName,'data-id':brandID});
        $(brandListItemTemplate).find('.brandName').html(brandName);

        // clone the template element and make it VISIBLE
        let newListItem = $(brandListItemTemplate).clone();
        $(newListItem).removeClass('d-none');
        $(newListItem).attr('id',''); // IMPORTANT! REMOVE ID!

        // prepend the newly cloned element
        $('#brandsTable').children('tbody').prepend(newListItem);

        // ==============
        // ==============
        // CREATE NEW MODELS TABLE In addition to creating a new list element, we must also create a new models table for the new brand
        let newModelTable = $('#TEMPLATE_models_table').clone();
        newModelTable.attr({'id':'', 'data-brand':brandName, 'data-id':brandID}); // IMPORTANT!!! REMOVE ID!

        newModelTable.empty(); // REQUIRED! Removes all child elements; this is because the table I just duplicated ALSO contains the model-table-listElement-TEMPLATE, which has a unique ID => therefore, we can't duplicate it
        $('#modelsTable').append(newModelTable);
        // ./CREATE NEW MODELS TABLE 
}

function addNewModelListItem(modelName,modelID,modelBuildYear,modelDetails,brandID) {

    let newListEl = $('#TEMPLATE_model_table_ELEMENT').clone();
    $(newListEl).attr({"id":"",'data-model':modelName,'data-model-id':modelID});
    console.log(modelName);
    $(newListEl).find('.modelName').html(modelName);
    $(newListEl).find('.modelBuildYear').html(modelBuildYear);
    $(newListEl).find('.modelDetailsText').html(modelDetails);

    // $('.receiveModelListUpdates[data-id='+GLOBAL_SELECTED_BRAND["brandID"]+']').append(newListEl);
    $('.receiveModelListUpdates[data-id='+brandID+']').append(newListEl);
}

function displayModelDetailModal(sender) {

    let listEl = $(sender).closest("tr"); // access the sender element
    const detailText = $(listEl).find('.modelDetailsText').html();
    const modelBuildYear = $(listEl).find('.modelBuildYear').html();
    const modalTitle = GLOBAL_SELECTED_BRAND['brandName'] + " " + listEl.attr('data-model') + " (" + modelBuildYear + ")";

    $('#modelDetailsModal h5').html(modalTitle);
    $('#modelDetailsModal .modal-body').html(detailText);

    $('#modelDetailsModal').modal('toggle');
}

function editModelChangeUI(tr_el, reverse=false, result=null) { // 'reverse' muss TRUE sein wenn wir fertig sind mit editieren
    const allButtons = $(tr_el).find('.allButtons');
    const editDoneButton = $(tr_el).find('.editDoneButton');
    
    let modelName = $(tr_el).find('.modelName');
    let modelBuildYear = $(tr_el).find('.modelBuildYear');
    let modelDetails = $(tr_el).find('.modelDetailsText');

    let modelNameInput = $(tr_el).find('.modelName-input');
    let modelBuildYearInput = $(tr_el).find('.modelBuildYear-input');
    let modelDetailsInput = $(tr_el).find('.modelDetailsText-input');

    if(reverse) {
        if(result) {
            $(modelName).html(result.modelName);
            $(modelBuildYear).html(result.modelBuildYear);
            $(modelDetails).html(result.modelDetails);
        }
        $(allButtons).removeClass('d-none');
        $(editDoneButton).addClass('d-none');

        $(modelName).removeClass('d-none');
        $(modelBuildYear).removeClass('d-none');

        $(modelNameInput).addClass('d-none');
        $(modelBuildYearInput).addClass('d-none');
        $(modelDetailsInput).addClass('d-none');
    }
    else {
        $(allButtons).addClass('d-none');
        $(editDoneButton).removeClass('d-none');

        /////////////////////////////////

        $(modelName).addClass('d-none');
        $(modelBuildYear).addClass('d-none');

        $(modelNameInput).removeClass('d-none');
        $(modelBuildYearInput).removeClass('d-none');
        $(modelDetailsInput).removeClass('d-none');
        $(modelNameInput).val(modelName.html());
        $(modelBuildYearInput).val(modelBuildYear.html());
        $(modelDetailsInput).val(modelDetails.html());
    }
}

function editModelButton(sender) {
    const tr_el = $(sender).closest('tr'); // this is the row element containing all relevant elements
    
    const fn = $(sender).attr('data-fn'); // since three different buttons can call this function, we can distinguish among them using the data-fn attribute

    if(fn=='cancelEditModel') {
        editModelChangeUI(tr_el, true); // pass the tr_el and reverse the UI changes (reverse=true)
    }
    else if (fn=='saveChangesModel') {
        // we will not reverse the UI in this function - we will do it in the callback instead, so that the UI is only reversed IF the server returns SUCCESS
        
        const modelID = $(tr_el).attr('data-model-id'); // this accesses the ID of the model
        const modelName = $(tr_el).find('.modelName-input').val();
        const modelBuildYear = $(tr_el).find('.modelBuildYear-input').val();
        const modelDetails = $(tr_el).find('.modelDetailsText-input').val();

        updateModel(modelID, modelName,modelBuildYear, modelDetails, tr_el);
    }
    else {
        editModelChangeUI(tr_el); // 'reverse' = false, weil wir die UI changes nicht umkehren
    }
}

function editBrandChangeUI(tr_el, reverse=false, result=null) { // 'reverse' muss TRUE sein wenn wir fertig sind mit editieren
    const allButtons = $(tr_el).find('.allButtons');
    const editDoneButton = $(tr_el).find('.editDoneButton');
    
    let brandName = $(tr_el).find('.brandName');

    let brandNameInput = $(tr_el).find('.brandName-input');

    if(reverse) {
        if(result) {
            $(brandName).html(result.brandName);
        }
        $(allButtons).removeClass('d-none');
        $(editDoneButton).addClass('d-none');

        $(brandName).removeClass('d-none');

        $(brandNameInput).addClass('d-none');
    }
    else {
        $(allButtons).addClass('d-none');
        $(editDoneButton).removeClass('d-none');

        /////////////////////////////////

        $(brandName).addClass('d-none');

        $(brandNameInput).removeClass('d-none');
        $(brandNameInput).val(brandName.html());
    }
}

function editBrandButton(sender) {
    const tr_el = $(sender).closest('tr'); // this is the row element containing all relevant elements
    
    const fn = $(sender).attr('data-fn'); // since three different buttons can call this function, we can distinguish among them using the data-fn attribute

    if(fn=='cancelEditBrand') {
        editBrandChangeUI(tr_el, true); // pass the tr_el and reverse the UI changes (reverse=true)
    }
    else if (fn=='saveChangesBrand') {
        // we will not reverse the UI in this function - we will do it in the callback instead, so that the UI is only reversed IF the server returns SUCCESS
        
        const brandID = $(tr_el).attr('data-id'); // this accesses the ID of the model
        const brandName = $(tr_el).find('.brandName-input').val();

        updateBrand(brandID, brandName, tr_el);
    }
    else {
        editBrandChangeUI(tr_el); // 'reverse' = false, weil wir die UI changes nicht umkehren
    }
}

function deleteBrandButton(sender) {
    const tr_el = $(sender).closest('tr'); // this is the row element containing all relevant elements

    const brandID = $(tr_el).attr('data-id'); // the data-id contains the brandID

    if (confirm('Are you sure you want to DELETE this brand? All customer cars will be deleted too!')) {
        // Delete the carBrand!
        deleteBrandFromServer(brandID);
      } else {
        // Do nothing!
        console.log('Nothing was deleted');
      }
}

function deleteModelButton(sender) {
    const tr_el = $(sender).closest('tr'); // this is the row element containing all relevant elements

    const modelName = $(tr_el).find('.modelName').html();
    const modelBuildYear = $(tr_el).find('.modelBuildYear').html();
    const modelDetails = $(tr_el).find('.modelDetailsText').html();

    preserveDeletedModel(GLOBAL_SELECTED_BRAND['brandID'], modelName, modelBuildYear,modelDetails); // this stores the data from the model that is about to be deleted in a global variable

    const modelID = $(tr_el).attr('data-model-id'); // this accesses the ID of the model


    if (confirm('Are you sure you want to DELETE this model? All customer cars will be deleted too!')) {
        // Delete the carBrand!
        deleteModelFromServer(modelID); // this function will delete the relevant model with ID from the server 
      } else {
        // Do nothing!
        console.log('Nothing was deleted');
      }
}

// this function stores the information of a carmodel that is about to be deleted in a global variable that can be accessed and restored if necessary
function preserveDeletedModel(brandID, modelName, modelBuildYear,modelDetails) {
    GLOBAL_RECENTLY_DELETED_MODEL['brandID'] = brandID;
    GLOBAL_RECENTLY_DELETED_MODEL['modelName'] = modelName;
    GLOBAL_RECENTLY_DELETED_MODEL['modelBuildYear'] = modelBuildYear;
    GLOBAL_RECENTLY_DELETED_MODEL['modelDetails'] = modelDetails;
}

function UndoDeleteModel() {
    console.log('I just called UNDODELETE');
    submitNewModel(
        GLOBAL_RECENTLY_DELETED_MODEL['modelName'],
        GLOBAL_RECENTLY_DELETED_MODEL['modelBuildYear'],
        GLOBAL_RECENTLY_DELETED_MODEL['modelDetails'],
        GLOBAL_RECENTLY_DELETED_MODEL['brandID']
    );
}

// message: The message to be displayed in the alert
// twoButtons: should the alert have TWO boxes or just one?
// firstButton: text to be displayed by first button
// secondButton: text to be displayed by second button
function showSmallAlert(msg, twoButtons=false, firstButtonMsg, firstButtonFn, secondButtonMsg='') {
    try {
        clearTimeout(timer); // this is necessary, so that we will not endlessly add on new timers
    }
    catch(err) {
        console.log('Warning: ', err);
    }

    var alertSmall = $('.custom-ui-alert-small');

    $(alertSmall).removeClass('hidden'); // make alert-small visible


    let timer = setTimeout(function(){ // hide alert-small AFTER 10 seconds
        $(alertSmall).addClass('hidden');
    }, 15000);

    $(alertSmall).find('.first-button').html(firstButtonMsg);

    $(alertSmall).find('.first-button').off('click'); // this removes ALL existing eventHandlers - otherwise, javascript will endlessly be adding on eventHandlers
    $(alertSmall).find('.first-button').on('click', function() {
        firstButtonFn();
        clearTimeout(timer); // this is necessary, so that the window will disappear immediately
        $(alertSmall).addClass('hidden');
    });

    $(alertSmall).removeClass('two-buttons'); // always remove the class first, because if not, it will endlessly be added
    if(twoButtons) {
        $(alertSmall).addClass('two-buttons');
        $(alertSmall).find('second-button').html(secondButtonMsg);
    }

    $(alertSmall).find('.message').html(msg);
}
