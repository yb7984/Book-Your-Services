import ListServices from '../modules/listServices.js'
import ListProviders from '../modules/listProviders.js'

const $serviceList = $("#services-list");
const $serviceTemplate = $("#services-template").html();

const listServices = new ListServices($serviceList , $serviceTemplate , "/api/services?limit=6");
listServices.loadList();

const listProviders = new ListProviders($("#providers-list") , $("#providers-template").html() , "/api/providers?limit=6")
listProviders.loadList();

