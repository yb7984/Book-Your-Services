import ListCategories from '../modules/listCategories.js'

/************
 * Here is the part for categories
 * 
 */


const LIST_URL = getGlobalValues("LIST_URL");
const NEW_URL = getGlobalValues("NEW_URL");
const UPDATE_URL = getGlobalValues("UPDATE_URL");
const DELETE_URL = getGlobalValues("DELETE_URL");

let categories = null;
const $btnNew = $("#btn-new");
const $categoryList = $("#categories-list");
const $categoryForm = $("#form-");

const categoryTemplate = `
<tr>
    <td>%%id%%</td>
    <td>%%name%%</td>
    <td>
        %%is_active%%
    </td>
    <td>
        <a class="btn btn-primary btn-edit" href="javascript:void(0);" title="Edit" data-id="%%id%%" data-toggle="modal" data-target="#form-container"><i class="fas fa-edit"></i></a>
        <a class="btn btn-danger btn-delete" href="javascript:void(0);" title="Delete" data-id="%%id%%"><i
                class="fas fa-trash-alt"></i></a>
    </td>
</tr>`;

const listCategories = new ListCategories($categoryList , categoryTemplate , LIST_URL , 0 , $categoryForm);
listCategories.insertUrl = NEW_URL;
listCategories.updateUrl = UPDATE_URL;
listCategories.deleteUrl = DELETE_URL;
listCategories.newTitle = "New Category";

$btnNew.on("click" , (e) => {
    listCategories.resetForm();
});

listCategories.loadList(true);
