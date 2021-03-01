import ListProviders from '/static/js/modules/listProviders.js'

const listProviders = new ListProviders(
    $("#providers-list") , 
    $("#providers-template").html() , 
    "/api/providers" , 
    3);

listProviders.loadList(true , 1 , true);

