
/**
 * Return the values set from the server side
 * @param {*} key 
 */
function getGlobalValues(key) {
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

/**
 * get the url for pager
 */
function getPageUrl(page = 1) {

    let params = new URLSearchParams(window.location.search);
    let url = window.location.pathname;

    params.delete("page");
    params.append("page", page);

    return url + "?" + params.toString();
}

// pager event, go to the page in data-page
if ($(".html-pager")) {
    $(".html-pager").on("click", ".pager-link", (e) => {
        e.preventDefault();

        const $btn = $(e.target);
        location.href = getPageUrl($btn.data("page"));
    });
}

// side menu event
if ($('#side-menu-btn')) {
    //toggle the side menu when smaller screen
    $('#side-menu-btn').on('click', (e) => {
        $('#side-menu').toggleClass('d-none');
    });
}