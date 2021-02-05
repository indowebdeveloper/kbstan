// ===========================
// ===========================
// ===========================
// ===========================
// ===========================
// ===========================
// EVENT DISPATCHER

var carHasSelected = new Event('carHasSelected'); // called when we change our selection of car brand
var updateModelList = new Event('updateModelList'); // called when we change our model list - triggered by BODY to call on all subscribing list elements
var reloadModelLists = new Event('reloadModelLists'); // called when we change our model list - it gets triggered by ALL SUBSCRIBING LIST ELEMENTS to reload themselves

//handle new car being selected
$('body').on('carHasSelected', () => {
    loadModels(GLOBAL_SELECTED_BRAND);

    $('#showNewModelButton').prop('disabled',false);

    var allBrandElements = $('.receiveSelectedBrandUpdates'); // all elements that want updates when a new car is selected must have this CSS-class
                                                              // all elements' contents will automatically be updated when this event is dispatched
    for(var i=0;i<allBrandElements.length;i++) {
        $(allBrandElements[i]).html(GLOBAL_SELECTED_BRAND["brandName"]);
    }
});

//handle new model list being loaded
$('body').on('updateModelList', () => {
    var allModelLists = $('.receiveModelListUpdates'); // all elements that want updates from the modelList must have this CSS-class
    for(var i=0;i<allModelLists.length;i++) {
        
        const el = allModelLists[i];
        
        if($(el).attr('data-id') == GLOBAL_SELECTED_BRAND["brandID"]) { // this selects the table whose data-id attribute matches the global variables of our currently selected brand (which is updated whenever we click on the table on the left)
            $('.receiveModelListUpdates').addClass('d-none'); // first, we must make ALL lists invisible
            $(el).removeClass('d-none'); // then we make only the target-table visible
        }
    }
});

// FORM VALIDATION FUNCTIONS

// Car fields editing functions:
// These functions are concerned with (de)activating buttons and doing simple frontend validation of submitted data

// BRAND INPUTS
function fieldUpdated(field) {
    const buttonToBeDisabled = $(field).attr('data-disable-target'); // the 'data-disable-target' attribute contains the ID of the button that needs to be (dis)abled when the value changes
    if(field.value) {
        $(buttonToBeDisabled).prop('disabled',false);
    }
    else {
        $(buttonToBeDisabled).prop('disabled',true);
    }
}
// ./BRAND INPUTS

// MODEL INPUTS

// ./MODEL INPUTS
