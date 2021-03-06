const DATE_FORMAT_LANG = "en-US";
const DATE_FORMAT_OPTIONS = {
    weekday: 'short',
    year: '2-digit',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric'
};

const WEEKDAYS = ["SUNDAY" , "MONDAY" , "TUESDAY" , "WEDNESDAY" , "THURDAY" , "FRIDAY" , "SATURDAY"];

const ALERT_SUCCESS = "success";
const ALERT_ERROR = "danger";


/**
 * Return the click event clicked button
 * @param {*} event 
 * @param {*} className 
 */
function findClickedButton(event, className) {
    let $btn = $(event.target);

    if (!$btn.hasClass(className)) {
        $btn = $btn.parents("." + className);
    }

    return $btn;
}


/**
 * Show alert message
 * @param {*} message 
 * @param {*} className 
 */
function showAlert(message, className = "success") {
    $("#alert-modal").find("#alert-content").html(`
    <label class="text-${className}">${message}</label>
    `);
    $("#alert-modal").modal("show");
}



if ($('#side-menu-btn')) {
    //toggle the side menu when smaller screen
    $('#side-menu-btn').on('click', (e) => {
        $('#side-menu').toggleClass('d-none');
    });
}