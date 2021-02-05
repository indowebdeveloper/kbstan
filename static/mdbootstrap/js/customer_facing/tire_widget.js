function showTireInfo(sender, show) {
    const target = $(sender).attr('data-hover-target');
    console.log(target);
    if(show) {
        $(target).show();
    }
    else{
        $(target).hide();
    }
}