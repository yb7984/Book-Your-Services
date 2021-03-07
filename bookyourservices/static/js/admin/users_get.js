import ListServices from '/static/js/modules/listServices.js';


/************
 * Here is the part for services
 * 
 */

//Service urls
const SERVICE_LIST_URL = getGlobalValues("SERVICE_LIST_URL")
const SERVICE_INSERT_URL = getGlobalValues("SERVICE_INSERT_URL")
const SERVICE_UPDATE_URL = getGlobalValues("SERVICE_UPDATE_URL");
const SERVICE_DELETE_URL = getGlobalValues("SERVICE_DELETE_URL");


const $serviceList = $("#services-list");
const $serviceTemplate = $("#services-template");
const $serviceForm = $("#form-service-container form");

const listServices = new ListServices(
    $serviceList ,
    $serviceTemplate.html(),
    SERVICE_LIST_URL,
    0, 
    $serviceForm,
    "service-",
    SERVICE_INSERT_URL,
    SERVICE_UPDATE_URL,
    SERVICE_DELETE_URL,
    "New Service"
);

listServices.loadList(true);

$("#btn-service-new").on("click" , (e)=>{
    listServices.resetForm();
});
