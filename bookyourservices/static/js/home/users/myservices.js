import ListServices from '/static/js/modules/listServices.js';

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

listServices.loadList(true , 1 , true);
