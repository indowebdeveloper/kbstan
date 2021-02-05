let GLOBAL_no_of_new_fields = 0;

$(document).ready(function(){
    $("#div_id_values input").attr('onblur','addAttributeRow(this)');
});

function addAttributeRow(sender) {
    if($(sender).val()) { // we should only execute this if the value of the input field is non-empty
        let new_attr_container = $(sender).closest('.form-group').prev('.form-group').clone();
        let new_value_container = $(sender).closest('.form-group').clone();
        
        $(sender).attr('onblur',''); // this way, the onblur-function is removed from all "old" elements, and only the lowest item can add new items - else, even if a higher up item is edited, we would infinitely keep adding input fields below

        GLOBAL_no_of_new_fields++; // increase the new_fields counter to assign a unique ID to each field
        
        $(new_attr_container).addClass('form-control-side-by-side'); // this class makes the field go side-by-side (50% width)
        $(new_value_container).addClass('form-control-side-by-side'); // this class makes the field go side-by-side (50% width)
        // TEMP $(new_attr_container).attr('id', `div_id_attribute${GLOBAL_no_of_new_fields}`); // this class makes the field go side-by-side (50% width)
        // TEMP $(new_value_container).attr('id', `div_id_values${GLOBAL_no_of_new_fields}`); // this class makes the field go side-by-side (50% width)
        
        // $(new_attr_container).insertBefore("input[type=submit]");
        // $(new_value_container).insertBefore("input[type=submit]");
        $('#add-attribute-btn').before(new_attr_container);
        $('#add-attribute-btn').before(new_value_container);

        $(new_value_container).find('input').blur(() => {
            if($(new_value_container).find('input').val()) { // the rows should only be copied if the user has written anything into the existing attribute field
                addAttributeRow(); 
            }
        });

        // reset all values to have empty fields
        const val_field = $(new_value_container).find('input');
        const attr_field_div = $(new_attr_container).find('.ui.dropdown');

        $(val_field).val(''); // reset value
        $(val_field).prop('required',false); // remove required field, as those are all required fields
        // TEMP $(val_field).attr('id',''); // removes existing ID
        // TEMP $(val_field).attr('id',`id_values${GLOBAL_no_of_new_fields}`); // assigns new, unqiue ID
        // TEMP $(val_field).attr('name',''); // removes existing NAME
        // TEMP $(val_field).attr('name',`values${GLOBAL_no_of_new_fields}`); // assigns new, unqiue NAME
        // --------------------------------------------
        $(attr_field_div).dropdown(); // re-apply the Semantic UI effects & styling
        $(attr_field_div).dropdown("clear"); // reset value
        $(attr_field_div).find('select').prop('required',false); // remove required field, as those are all required fields
        // TEMP $(attr_field_div).find('select').attr('id',''); // removes existing ID
        // TEMP $(attr_field_div).find('select').attr('id',`id_attribute${GLOBAL_no_of_new_fields}`); // assigns new, unqiue ID
        // TEMP $(attr_field_div).find('select').attr('name',''); // removes existing NAME
        // TEMP $(attr_field_div).find('select').attr('name',`attribute${GLOBAL_no_of_new_fields}`); // assigns new, unqiue NAME
        // END reset
    }
}