
/**
 * Return the values set from the server side
 * @param {*} key 
 */
function getGlobalValues(key){
    return $(document).data(key);
}

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