function adjustQuantityField(sender) {
    let target_field = $(sender).attr('data-target-field');
    let target_field_value = $(target_field).val();
    let action = $(sender).attr('data-action');

    if(action == "INCREASE") {
        $(target_field).val(++target_field_value);
    }
    if(action == "DECREASE") {
        if(target_field_value==1) {
            console.log('cannot go below 1');
        }
        else {
            $(target_field).val(--target_field_value);
        }
    }
    else {
        console.log(`no button action specified for ${sender}`);
    }
}