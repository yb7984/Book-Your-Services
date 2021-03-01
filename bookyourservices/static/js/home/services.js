import ListServices from '/static/js/modules/listServices.js'

const $serviceList = $("#services-list");
const $serviceTemplate = $("#services-template").html();

const listServices = new ListServices($serviceList , $serviceTemplate , "/api/services");

listServices.loadList();

