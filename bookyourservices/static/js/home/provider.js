import ListServices from '/static/js/modules/listServices.js'

const listServices = new ListServices(
    $("#services-list"),
    $("#services-template").html(),
    `/api/services?username=${PROVIDER_USER_NAME}`);

listServices.loadList(true , 1 , true);

