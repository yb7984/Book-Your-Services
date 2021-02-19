

if ($('#side-menu-btn')){
    //toggle the side menu when smaller screen
    $('#side-menu-btn').on('click' , (e) => {
        $('#side-menu').toggleClass('d-none');
    });
}