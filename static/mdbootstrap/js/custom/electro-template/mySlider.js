function nextSlide(elem) {
    $(elem).addClass('next');
}

function previousSlide(elem) {
    $(elem).addClass('previous');
}

function goToSlide(elem, slideNumber) {
    $(elem).addClass(slideNumber);
}


// UI-functions
function callNextSlide(sender) {
    const targetElName = $(sender).attr('data-target');
    const targetEl = $(targetElName);
    nextSlide(targetEl);
}

function callPreviousSlide(sender) {
    const targetElName = $(sender).attr('data-target');
    const targetEl = $(targetElName);
    previousSlide(targetEl);
}

function callGoToSlide(sender) {
    const targetElName = $(sender).attr('data-target');
    const slideNumber = $(sender).attr('data-el-index');
    const targetEl = $(targetElName);
    goToSlide(targetEl, slideNumber);
}