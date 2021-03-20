import ListServices from '../modules/listServices.js'

const PROVIDER_USERNAME = getGlobalValues("PROVIDER_USERNAME");

const listServices = new ListServices(
    $("#services-list"),
    $("#services-template").html(),
    `/api/services?username=${PROVIDER_USERNAME}`);

listServices.loadList(true , 0 , true);

