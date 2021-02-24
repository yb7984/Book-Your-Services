import ServicesList from '/static/js/modules/listServices.js'
import ProvidersList from '/static/js/modules/listProviders.js'

const listServices = new ServicesList($("#services-list") , $("#services-template").html() , "/api/services?limit=6")

listServices.loadList();

const listProviders = new ProvidersList($("#providers-list") , $("#providers-template").html() , "/api/providers?limit=6")

listProviders.loadList();

