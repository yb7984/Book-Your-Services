import * as formFunc from '/static/js/modules/form.js'

/************
 * Here is the part for addresses
 * 
 */
const $addressList = $("#addresses-list");
const $addressTemplate = $("#addresses-template");
const $addressForm = $("#form-address-container form");
const $addressFormTitle = $("#address-form-title");
/**
 * Address edit button event
 */
$addressList.on("click", ".address-edit", async function (e) {
    e.preventDefault();
    const $btn = $(e.target);

    const id = $btn.data("id");

    const address = await getAddress(id);

    if (address) {
        $addressFormTitle.text("Edit Address");
        const $btn = $(`<button class="btn btn-success">New Address</button>`);
        $btn.on("click" , resetAddressForm);
        $addressFormTitle.append($btn);

        $("#address-id").val(address.id);
        $("#address-name").val(address.name);
        $("#address-address1").val(address.address1);
        $("#address-address2").val(address.address2);
        $("#address-state").val(address.state);
        $("#address-city").val(address.city);
        $("#address-zipcode").val(address.zipcode);

        $("#address-is_default").prop("checked", address.is_default);
        $("#address-is_active").prop("checked", address.is_active);
    }
});

/**
 * Address delete button event
 */
$addressList.on("click", ".address-delete", async function (e) {
    e.preventDefault();
    const $btn = $(e.target);

    const id = $btn.data("id");

    try {
        const resp  = await axios.delete(ADDRESS_DELETE_URL.substring(0 , ADDRESS_DELETE_URL.length - 1) + id);
        
        await removeAddress(id);
    } catch (error) {
        formFunc.showFormError($addressForm , "Error when deleting!");
    }
});

/**
 * Address submit event
 */
$addressForm.on("submit", async function (e) {
    e.preventDefault();

    try {
        formFunc.showFormError($addressForm , "");

        const id = $("#address-id").val();
        let url = ADDRESS_NEW_URL;
        let method = "post";

        if (id){
            url = ADDRESS_UPDATE_URL.substring(0 , ADDRESS_UPDATE_URL.length - 1) + id;
            method = "patch";
        }

        const resp = await formFunc.postForm($addressForm, url , method , true);

        if (resp.data.item){
            
            if (resp.status === 201) {
                //create successfully
                await listAddresses(true);
    
                resetAddressForm();
            } else if (id && resp.status === 200){
                //update successfully
                await listAddresses(true);
    
                resetAddressForm();
            } 
        } else {
            if (resp.data.error){
                formFunc.showFormError($addressForm , resp.data.error);
            } else if (resp.data.errors){
                const errors = resp.data.errors;
                formFunc.showFormError($addressForm , "" , errors);
            }
        }

    } catch (error) {
        formFunc.showFormError($addressForm , "Error when updating data!");
    }
})

/**
 * List All Address of current user
 * @param {*} reload 
 */
async function listAddresses(reload=false) {

    const list = await getAddresses(reload);

    $addressList.html('');
    list.forEach(item => {
        $addressList.append(getAddressHtml(item));
    });
}

/**
 * Remove an address from the list
 * @param {*} id 
 */
async function removeAddress(id){
    const list = await getAddresses();

    //update the addresses value
    for (let i = 0 ; i < list.length ; i ++){
        if (list[i].id === id){
            list.splice(i , 1);
            break;
        }
    }

    //update the display
    $(`#address-list-${id}`).remove();
}

/**
 * Return the html of the address
 * @param {*} address 
 */
function getAddressHtml(address){

    return $addressTemplate.html()
        .replaceAll("%%id%%", address.id)
        .replaceAll("%%address%%", address.address.replaceAll("\n", "<br />"))
        .replaceAll("%%is_default%%", address.is_default ? "Default" : "")
        .replaceAll("%%is_active%%", address.is_active ? "" : "Inactive");
}

/**
 * Get address data by address id
 */
async function getAddress(id) {

    const list = await getAddresses();

    for (let i = 0; i < list.length; i++) {
        if (list[i].id === id) {
            return list[i];
        }
    }

    return null;
}


/**
 * Return the address list of the user
 * @param {*} reload 
 */
async function getAddresses(reload=false) {

    if (addresses == null || reload === true) {
        //Load the addresses if not loaded yet
        const resp = await axios.get(ADDRESS_LIST_URL);

        addresses = resp.data.items;
    }
    return addresses;
}


/**
 * Reset the form to original status
 */
function resetAddressForm(){
    $addressFormTitle.text("New Addresses");
    $("#address-id").val('');
    formFunc.resetForm($addressForm);
}



/************
 * Here is the part for services
 * 
 */
const $serviceList = $("#services-list");
const $serviceTemplate = $("#services-template");
const $serviceForm = $("#form-service-container form");
const $serviceFormTitle = $("#service-form-title");
/**
 * Service edit button event
 */
$serviceList.on("click", ".service-edit", async function (e) {
    e.preventDefault();
    const $btn = $(e.target);

    const id = $btn.data("id");

    const service = await getService(id);

    if (service) {
        $serviceFormTitle.text("Edit Service");
        const $btn = $(`<button class="btn btn-success">New Service</button>`);
        $btn.on("click" , resetServiceForm);
        $serviceFormTitle.append($btn);

        $("#service-id").val(service.id);
        $("#service-name").val(service.name);
        $("#service-location_type").val(service.location_type);
        $("#service-description").text(service.description);
        $("#service-is_active").prop("checked", service.is_active);

        $("#service-categories").val(service.category_ids);
    }
});

/**
 * Service delete button event
 */
$serviceList.on("click", ".service-delete", async function (e) {
    e.preventDefault();
    const $btn = $(e.target);

    const id = $btn.data("id");

    try {
        const resp  = await axios.delete(SERVICE_DELETE_URL.substring(0 , SERVICE_DELETE_URL.length - 1) + id);
        
        await removeService(id);
    } catch (error) {
        formFunc.showFormError($serviceForm , "Error when deleting!");
    }
});

/**
 * Service submit event
 */
$serviceForm.on("submit", async function (e) {
    e.preventDefault();

    try {
        formFunc.showFormError($serviceForm , "");

        const id = $("#service-id").val();
        let url = SERVICE_NEW_URL;
        let method = "post";

        if (id){
            url = SERVICE_UPDATE_URL.substring(0 , SERVICE_UPDATE_URL.length - 1) + id;
            method = "patch";
        }

        const resp = await formFunc.postForm($serviceForm, url , method);

        
        if (resp.data.item){
            
            if (resp.status === 201) {
                //create successfully
                await listServices(true);
    
                resetServiceForm();
            } else if (id && resp.status === 200){
                //update successfully
                await listServices(true);
    
                resetServiceForm();
            } 
        } else {
            if (resp.data.error){
                formFunc.showFormError($serviceForm , resp.data.error);
            } else if (resp.data.errors){
                const errors = resp.data.errors;
                formFunc.showFormError($serviceForm , "" , errors);
            }
        }

    } catch (error) {
        formFunc.showFormError($serviceForm , "Error when updating data!");
    }
})

/**
 * List All Service of current user
 * @param {*} reload 
 */
async function listServices(reload=false) {

    const list = await getServices(reload);

    $serviceList.html('');
    
    list.forEach(item => {
        $serviceList.append(getServiceHtml(item));
    });
}

/**
 * Remove an service from the list
 * @param {*} id 
 */
async function removeService(id){
    const list = await getServices();

    //update the services value
    for (let i = 0 ; i < list.length ; i ++){
        if (list[i].id === id){
            list.splice(i , 1);
            break;
        }
    }

    //update the display
    $(`#services-list-${id}`).remove();
}

/**
 * Return the html of the service
 * @param {*} service 
 */
function getServiceHtml(service){

    let categories = "";
    service.categories.forEach(item => {
        if (categories.length > 0){
            categories += ", ";
        }
        categories += item.name;
    })
    return $serviceTemplate.html()
        .replaceAll("%%id%%", service.id)
        .replaceAll("%%name%%", service.name)
        .replaceAll("%%categories%%", categories)
        .replaceAll("%%location_type%%", service.location_type_name)
        .replaceAll("%%description%%", service.description.replaceAll("\n", "<br />"))
        .replaceAll("%%image%%" , service.image_url)
        .replaceAll("%%is_active%%", service.is_active ? "" : "Inactive");
}

/**
 * Get service data by service id
 */
async function getService(id) {

    const list = await getServices();

    for (let i = 0; i < list.length; i++) {
        if (list[i].id === id) {
            return list[i];
        }
    }

    return null;
}


/**
 * Return the service list of the user
 * @param {*} reload 
 */
async function getServices(reload=false) {

    if (services == null || reload === true) {
        //Load the services if not loaded yet
        const resp = await axios.get(SERVICE_LIST_URL);

        services = resp.data.items;
    }
    return services;
}


/**
 * Reset the form to original status
 */
function resetServiceForm(){
    $serviceFormTitle.text("New Services");
    $("#service-id").val('');
    formFunc.resetForm($serviceForm);
}



/****************
Load data here.
 */
listAddresses();
listServices();

