import ListProviders from '../modules/listProviders.js'

const listProviders = new ListProviders(
    $("#providers-list") , 
    $("#providers-template").html() , 
    "/api/providers" , 
    12);

listProviders.loadList(true , 0 , true);

