import ListServices from '../modules/listServices.js';

const SERVICE_LIST_URL = '/api/services/mine';
const SERVICE_INSERT_URL = '/api/services';
const SERVICE_UPDATE_URL = '/api/services/0';
const SERVICE_DELETE_URL = '/api/services/0';

const $listContainer = $("#services-list");
const $form = $("#form-service-");
const $newBtn = $("#btn-new");


const listServices = new ListServices(
    $listContainer,
    $("#services-template").html(),
    SERVICE_LIST_URL, 
    12, 
    $form ,
    "service-",
    SERVICE_INSERT_URL,
    SERVICE_UPDATE_URL,
    SERVICE_DELETE_URL,
    "New Service");

$newBtn.on("click" , (e)=>{
    listServices.resetForm();
});

listServices.loadList(true , 0 , true);
