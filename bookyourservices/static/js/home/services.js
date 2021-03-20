import ListServices from '../modules/listServices.js'

const $serviceList = $("#services-list");
const $serviceTemplate = $("#services-template").html();

const listServices = new ListServices($serviceList , $serviceTemplate , "/api/services" , 12);

listServices.loadList(true , 0 , true);

