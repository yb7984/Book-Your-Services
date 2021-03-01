import ListServices from '/static/js/modules/listServices.js';
// import * as formFunc from '/static/js/modules/form.js';

// const $title = $("#service-form-title");
const $listContainer = $("#services-list");
// const $formContainer = $("#form-service-container");
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

// $listContainer.on("click" , ".btn-edit" , async (e)=>{

//     const $btn = findClickedButton(e , "btn-edit");

//     const id = $btn.data("id");

//     let item = await listServices.getItem("id" , id);


//     $title.html(`Edit Service: ${item.name}`);
//     $("#service-id").val(item.id);
//     $("#service-name").val(item.name);
//     $("#service-categories").val(item.category_ids);
//     $("#service-description").val(item.description);
//     $("#service-location_type").val(item.location_type);
//     $("#service-is_active").prop("checked" , item.is_active);
// });


// /**
//  * Service submit event
//  */
// $form.on("submit", async function (e) {
//     e.preventDefault();

//     try {
//         formFunc.showFormError($form , "");

//         const id = $("#service-id").val();
//         let url = SERVICE_INSERT_URL;
//         let method = "post";

//         if (id){
//             url = SERVICE_UPDATE_URL.substring(0 , SERVICE_UPDATE_URL.length - 1) + id;
//             method = "patch";
//         }

//         const resp = await formFunc.postForm($form, url , method);

        
//         if (resp.data.item){
            
//             if (resp.status === 201) {
//                 //create successfully
//                 await listServices.loadList(true , 1 , true);
    
//                 resetServiceForm();
//                 $formContainer.modal("hide");

//             } else if (id && resp.status === 200){
//                 //update successfully
//                 await listServices.loadList(true , 1 , true);
    
//                 resetServiceForm();
//                 $formContainer.modal("hide");

//             } 
//         } else {
//             if (resp.data.error){
//                 formFunc.showFormError($form , resp.data.error);
//             } else if (resp.data.errors){
//                 const errors = resp.data.errors;
//                 formFunc.showFormError($form , "" , errors);
//             }
//         }

//     } catch (error) {
//         formFunc.showFormError($form , "Error when updating data!");
//     }
// });


// /**
//  * Service delete event
//  */
// $listContainer.on("click" , ".btn-delete" , async (e)=>{
//     e.preventDefault();
    
//     const $btn = findClickedButton(e , "btn-delete");

//     const id = $btn.data("id");

//     try {
//         const resp  = await axios.delete(SERVICE_DELETE_URL.substring(0 , SERVICE_DELETE_URL.length - 1) + id);
        
//         await listServices.loadList(true, listServices.page , true)
//     } catch (error) {
//         showAlert("Error when deleting!" , ALERT_ERROR);
//     }
// });


// /**
//  * Reset the form to original status
//  */
// function resetServiceForm(){
//     $title.text("New Services");
//     $("#service-id").val('');
//     formFunc.resetForm($form);

// }


listServices.loadList(true , 1 , true);
