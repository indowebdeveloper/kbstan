function to_human(value) {
    let temp_val = value;
    let new_val = '';
    let endless_count = 0;

    while(!((temp_val)<1000)) { // this is the ending condition - if the current_val can no longer be divided by 1,000, the function should stop and return the new value
        endless_count++;
        if(endless_count>50) { // to prevent endless loop, just in case
            break;
        }

        ////////////////////////

        let add_val = temp_val%1000;
        if(add_val < 10) {
            add_val = '00'+add_val; // if the number to be converted is e.g. 10003 then the %1000 would yield "3", which would be converted into 10,3 instead of 10,003. So we need to add either two '0' or one '0' depending on the modulo
        }
        else if(add_val < 100) {
            add_val = '0'+add_val;
        }

        ////////////////////////

        new_val = ","+ add_val + new_val;
        temp_val = parseInt(temp_val/1000);
    }
    new_val = String(temp_val + new_val); // adds the last remainder of the number to the string

    return new_val;
}

function to_machine(value) {
    let temp = String(value);
    return parseFloat(temp.replace(/,/g,'')); // this returns a parsedFloat of a 'value'-variable where all "," have been removed and thus can be parsed to float
}


function humanise(value, direction='to_human') {
    if(direction=='to_machine') {
        return to_machine(value);
    }
    else {
        return to_human(value);
    }
}