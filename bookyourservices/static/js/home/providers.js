import ProvidersList from '/static/js/modules/listProviders.js'

const listProviders = new ProvidersList($("#providers-list") , $("#providers-template").html() , "/api/providers")

listProviders.loadList();

