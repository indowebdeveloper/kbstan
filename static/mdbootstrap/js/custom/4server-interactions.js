// ===========================
// ===========================
// ===========================
// ===========================
// ===========================
// ===========================
// SERVER-INTERACTION FUNCTIONS

function loadModels(brand) {
    document.querySelector('body').dispatchEvent(updateModelList);
}

// CSRF code

var csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sendServerRequest(url, data, callback, additionalData=null) {
    // code required for CSRF
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    console.log("=== DATA ===");
    console.log(data);

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),
        dataType: 'text',
        success: function(result) {
            // this IF is needed because some callbacks need parameters such as the modelID, which are passed in the initial request - however, since not ALL callbacks need it, I cannot simply pass 'additionalData' to ALL the callbacks
            if(additionalData==null) {
                callback(result);
            }
            else {
                callback(result, additionalData);
            }
        },
        error: function(err) {
            console.log(err);
        }
    });
}

function CallbackSubmitNewBrand(result) {

    result = JSON.parse(result);

    console.log(result);

    if( result.status == 'Car brand already exists') {
        alert(result.status);
    }
    else { // this means a new brand could be successfully created
        addNewBrandListItem(result.brandID,result.brandName); // adds new <tr> element into the brands-table
    }
}

function CallbackSubmitNewModel(result) {
    result = JSON.parse(result);

    if( result.status == 'Car model already exists') {
        alert(result.status);
    }
    else { // this means a new brand could be successfully created
        addNewModelListItem(result.modelName,result.modelID,result.modelBuildYear,result.modelDetails,GLOBAL_SELECTED_BRAND['brandID']); // adds new <tr> element into the models-table
    }
}

function CallbackUpdateModel(result,tr_el) {
    result = JSON.parse(result);

    if( result.status == 'Car model already exists') {
        alert(result.status);
    }
    else { // this means a new brand could be successfully created
        editModelChangeUI(tr_el, true, result);

        // addNewModelListItem(result.modelName,result.modelID,result.modelBuildYear,result.modelDetails,GLOBAL_SELECTED_BRAND['brandID']); // adds new <tr> element into the models-table
    }
}

function CallbackUpdateBrand(result,tr_el) {
    result = JSON.parse(result);

    if( result.status == 'Car brand already exists') {
        alert(result.status);
    }
    else { // this means a new brand could be successfully created
        editBrandChangeUI(tr_el, true, result);

        // addNewModelListItem(result.modelName,result.modelID,result.modelBuildYear,result.modelDetails,GLOBAL_SELECTED_BRAND['brandID']); // adds new <tr> element into the models-table
    }
}

function CallbackDeleteModel(result,modelID) { // the callback's 'additionalData' variable will pass the modelID
    result = JSON.parse(result);
    console.log(modelID);

    if( result.status == 'Car model has been deleted') {
        console.log('MAKE THIS A CUSTOM ALERT', result.status);
        const selectedBrand = GLOBAL_SELECTED_BRAND['brandID'];

        // we select the #modelsTable, within that the <tbody> that has the selectedBrandID and within THAT the <tr> that has the modelID that was returned from the server as deleted

        $('#modelsTable tbody[data-id='+selectedBrand+'] tr[data-model-id='+modelID+']' ).remove();

        showSmallAlert('Deleted by accident?', false, "Undo", UndoDeleteModel);
    }
    else { // this means a new brand could be successfully created
        alert("Error while deleting car");
    }
}

function CallbackDeleteBrand(result,brandID) { // the callback's 'additionalData' variable will pass the modelID
    result = JSON.parse(result);

    if( result.status == 'Car brand has been deleted') {
        console.log('MAKE THIS A CUSTOM ALERT: ', result.status);

        // we select the #brandsTable, within that the <tr> that has the dataID (=brandID) that was returned from the server as deleted
        $('#brandsTable tr[data-id='+brandID+']' ).remove();

        // we also have to delete the models table that corresponds with the brandId that has just been deleted
        $(`#modelsTable tbody[data-id='${brandID}']` ).remove();

        // reset the SELECTED-BRAND, or else, the models table will still show the old selected Brand as its heading
        GLOBAL_SELECTED_BRAND = {brandName:'', brandID: ''};
        document.querySelector('body').dispatchEvent(carHasSelected); // this event must be dispatched, so that the models table knows that it must update itself

        // showSmallAlert('Deleted by accident?', false, "Undo", UndoDeleteModel);
    }
    else { // this means a new brand could be successfully created
        alert("Error while deleting car");
    }
}

function submitNewBrand(brandName) {
    // const url = 'http://165.22.58.179/cars/carbrand/create/';
    const url = '/cars/carbrand/create/';

    var data = {'brandName':brandName};

    sendServerRequest(url, data, CallbackSubmitNewBrand);
}

function submitNewModel(modelName,modelBuildYear,modelDetails,brandID) {
    // const url = 'http://165.22.58.179/cars/carmodel/create/';
    const url = '/cars/carmodel/create/';

    const parsedBuildYear = !modelBuildYear ? 0 : modelBuildYear; // If the buildYear field is empty, I must send it as 0, to prevent errors

    var data = {modelName:modelName,modelBuildYear:parseInt(parsedBuildYear),modelDetails:modelDetails,brandID:brandID};

    sendServerRequest(url, data, CallbackSubmitNewModel);
}

function updateModel(modelID, modelName,modelBuildYear,modelDetails,tr_el) {
    // const url = 'http://165.22.58.179/cars/carmodel/update/';
    const url = '/cars/carmodel/update/';

    const parsedBuildYear = !modelBuildYear ? 0 : modelBuildYear; // If the buildYear field is empty, I must send it as 0, to prevent errors

    console.log('Build Year:');
    console.log(parsedBuildYear);

    // brandID not needed, only modelID needed
    var data = {"modelID":modelID, modelName:modelName,modelBuildYear:parseInt(parsedBuildYear),modelDetails:modelDetails};

    sendServerRequest(url, data, CallbackUpdateModel, tr_el);
}

function updateBrand(brandID, brandName,tr_el) {
    // const url = 'http://165.22.58.179/cars/carbrand/update/';
    const url = '/cars/carbrand/update/';

    // brandID not needed, only modelID needed
    var data = {brandID:brandID, brandName:brandName};

    console.log('BRAND DATA');
    console.log(data);

    sendServerRequest(url, data, CallbackUpdateBrand, tr_el);
}

function deleteBrandFromServer(brandID) {
    // const url = 'http://165.22.58.179/cars/carbrand/delete/';
    const url = '/cars/carbrand/delete/';

    var data = {brandID:brandID};

    sendServerRequest(url, data, CallbackDeleteBrand, brandID);
}

function deleteModelFromServer(modelID) {
    // const url = 'http://165.22.58.179/cars/carmodel/delete/';
    const url = '/cars/carmodel/delete/';

    var data = {modelID:modelID};

    sendServerRequest(url, data, CallbackDeleteModel, modelID);
}