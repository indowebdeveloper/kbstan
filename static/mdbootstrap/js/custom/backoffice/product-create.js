let GLOBAL_no_of_new_fields = 0;

function addAttributeRow() {
    let sender; // this is the last attribute field that has been edited

    if ( $('.form-control-side-by-side').length == 0 ) { // if there is NO elements with the ".form-control-side-by-side"-class, it means that there is only one field, with an ID. So we should check this field. Else, we should check the last field with the "..form-control-side-by-side"-class
        sender = $('#div_id_values').find('input');
    }
    else {
        sender = $('.form-control-side-by-side').last().find('input');
    }

    if($(sender).val()) { // we should only execute this if the value of the input field is non-empty
        let new_attr_container = $(sender).closest('.form-group').prev('.form-group').clone();
        let new_value_container = $(sender).closest('.form-group').clone();

        GLOBAL_no_of_new_fields++; // increase the new_fields counter to assign a unique ID to each field
        
        $(new_attr_container).addClass('form-control-side-by-side'); // this class makes the field go side-by-side (50% width)
        $(new_value_container).addClass('form-control-side-by-side'); // this class makes the field go side-by-side (50% width)

        $('#add-attribute-btn').before(new_attr_container);
        $('#add-attribute-btn').before(new_value_container);

        // reset all values to have empty fields
        const val_field = $(new_value_container).find('input');
        const attr_field_div = $(new_attr_container).find('.ui.dropdown');

        $(val_field).val(''); // reset value
        $(val_field).prop('required',false); // remove required field, as those are all required fields

        // --------------------------------------------

        $(attr_field_div).dropdown(); // re-apply the Semantic UI effects & styling
        $(attr_field_div).dropdown("clear"); // reset value
        $(attr_field_div).find('select').prop('required',false); // remove required field, as those are all required fields
        // END reset
    }
}