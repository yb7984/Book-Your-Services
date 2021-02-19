import * as formFunc from '/static/js/modules/form.js'

/************
 * Here is the part for categories
 * 
 */
const $categoryList = $("#categories-list");
const $categoryForm = $("#form-category-container form");
const $categoryFormTitle = $("#category-form-title");

const categoryTemplate = `
<tr>
    <td>%%id%%</td>
    <td>%%name%%</td>
    <td>
        %%is_active%%
    </td>
    <td>
        <a class="btn btn-primary category-edit" href="javscript:void(0);" title="Edit" data-id="%%id%%"><i class="fas fa-edit"></i></a>
        <a class="btn btn-danger category-delete" href="javscript:void(0);" title="Delete" data-id="%%id%%"><i
                class="fas fa-trash-alt"></i></a>
    </td>
</tr>`;

/**
 * Category edit button event
 */
$categoryList.on("click", ".category-edit", async function (e) {
    e.preventDefault();
    let $btn = $(e.target);

    if (!$btn.data("id")){
        $btn = $($btn.parents(".category-edit"));
    }

    const id = $btn.data("id");

    const category = await getCategory(id);

    if (category) {
        $categoryFormTitle.text("Edit Category");
        const $btn = $(`<button class="btn btn-success">New Category</button>`);
        $btn.on("click" , resetCategoryForm);
        $categoryFormTitle.append($btn);

        $("#id").val(category.id);
        $("#name").val(category.name);
        $("#is_active").prop("checked", category.is_active);
    }
});

/**
 * Category delete button event
 */
$categoryList.on("click", ".category-delete", async function (e) {
    e.preventDefault();
    let $btn = $(e.target);

    if (!$btn.data("id")){
        $btn = $($btn.parents(".category-delete"));
    }

    const id = $btn.data("id");

    try {
        const resp  = await axios.delete(DELETE_URL.substring(0 , DELETE_URL.length - 1) + id);
        
        await listCategories(true);
    } catch (error) {
        formFunc.showFormError($categoryForm , "Error when deleting!");
    }
});

/**
 * Category submit event
 */
$categoryForm.on("submit", async function (e) {
    e.preventDefault();

    try {
        formFunc.showFormError($categoryForm , "");

        const id = $("#id").val();
        let url = NEW_URL;
        let method = "post";

        if (id){
            url = UPDATE_URL.substring(0 , UPDATE_URL.length - 1) + id;
            method = "patch";
        }


        const resp = await formFunc.postForm($categoryForm, url , method , true);

        if (resp.data.item){
            
            if (resp.status === 201) {
                //create successfully
                await listCategories(true);
    
                resetCategoryForm();
            } else if (id && resp.status === 200){
                //update successfully
                await listCategories(true);
    
                resetCategoryForm();
            } 
        } else {
            if (resp.data.error){
                formFunc.showFormError($categoryForm , resp.data.error);
            } else if (resp.data.errors){
                const errors = resp.data.errors;
                formFunc.showFormError($categoryForm , "" , errors);
            }
        }

    } catch (error) {
        formFunc.showFormError($categoryForm , "Error when updating data!");
    }
})

/**
 * List All Category of current user
 * @param {*} reload 
 */
async function listCategories(reload=false) {

    const list = await getCategories(reload);

    $categoryList.html('');
    list.forEach(item => {
        $categoryList.append(getCategoryHtml(item));
    });
}

/**
 * Return the html of the category
 * @param {*} category 
 */
function getCategoryHtml(category){

    return categoryTemplate
        .replaceAll("%%id%%", category.id)
        .replaceAll("%%name%%", category.name)
        .replaceAll("%%is_active%%", category.is_active ? `<i class="fas fa-check text-success"></i>` : `<i class="fas fa-times text-danger"></i>`);
}

/**
 * Get category data by category id
 */
async function getCategory(id) {

    const list = await getCategories();

    for (let i = 0; i < list.length; i++) {
        if (list[i].id === id) {
            return list[i];
        }
    }

    return null;
}


/**
 * Return the category list of the user
 * @param {*} reload 
 */
async function getCategories(reload=false) {

    if (categories == null || reload === true) {
        //Load the categories if not loaded yet
        const resp = await axios.get(LIST_URL);

        categories = resp.data.items;
    }
    return categories;
}


/**
 * Reset the form to original status
 */
function resetCategoryForm(){
    $categoryFormTitle.text("New Categories");
    $("#id").val('');
    formFunc.resetForm($categoryForm);
}


listCategories(true);
