import ServicesList from '/static/js/modules/listServices.js'

const listServices = new ServicesList(
    $("#services-list"),
    $("#services-template").html(),
    `/api/services?username=${PROVIDER_USER_NAME}`)

listServices.loadList();

