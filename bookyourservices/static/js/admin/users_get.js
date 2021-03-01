import * as formFunc from '/static/js/modules/form.js';
import ListAddresses from '/static/js/modules/listAddresses.js';
import ListServices from '/static/js/modules/listServices.js';

/************
 * Here is the part for addresses
 * 
 */
const $addressList = $("#addresses-list");
const $addressTemplate = $("#addresses-template");
const $addressForm = $("#form-address-container form");

const listAddresses = new ListAddresses(
    $addressList ,
    $addressTemplate.html(),
    ADDRESS_LIST_URL,
    0, 
    $addressForm,
    "address-",
    ADDRESS_INSERT_URL,
    ADDRESS_UPDATE_URL,
    ADDRESS_DELETE_URL,
    "New Address"
);

listAddresses.loadList(true);

$("#btn-address-new").on("click" , (e)=>{
    listAddresses.resetForm();
});


/************
 * Here is the part for services
 * 
 */
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
