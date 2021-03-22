import * as formFunc from '../modules/form.js';
import * as config from '../config.js';
/**
 * Basic class for list items from ajax resource
 * Author: Sunbao Wu
 * Email: bobowu@outlook.com
 */
class ListBasic {

    /**
     * Constructor for ListBasic
     * @param {*} $list jQuery object of the list container
     * @param {*} template html template of how to display the list
     * @param {*} url the url to get the list
     * @param {*} per_page how many items per page. if set to 0 getting the default amount of the server setting.
     * @param {*} $form jQuery object of the form for submiting updates. 
     * @param {*} prefix prefix for the form items
     * @param {*} insertUrl url for insert new item.
     * @param {*} updateUrl url for update existed item.
     * @param {*} deleteUrl url for delete existed item
     * @param {*} newTitle title of the form for inserting new Item
     */
    constructor(
        $list,
        template,
        url,
        per_page = 0,
        $form = null,
        prefix = "",
        insertUrl = "",
        updateUrl = "",
        deleteUrl = "",
        newTitle = "") {
        this.$listContainer = $list;
        this.template = template;
        this.url = url;
        this.per_page = per_page;

        this.items = null;

        // the id key default to "id"
        this.idKey = "id";
        this.nameKey = "name";

        this.$form = $form;
        this.prefix = prefix;
        this.insertUrl = insertUrl;
        this.updateUrl = updateUrl;
        this.deleteUrl = deleteUrl;

        this.newTitle = newTitle;

        this.event();

    }

    /**
     * event handlers
     */
    event() {

        //load pager click event
        this.$listContainer.on("click", ".pager a", async (e) => {
            e.preventDefault();

            const $link = $(e.target);


            if ($link.hasClass("page-first")) {
                await this.loadList(true, 1, true);
                location.href = "#page=1";
            } else if ($link.hasClass("page-prev")) {
                const hash = "#page=" + (this.page - 1);
                await this.loadList(true, this.page - 1, true);
                location.href = hash;
            } else if ($link.hasClass("page-next")) {
                const hash = "#page=" + (this.page + 1);
                await this.loadList(true, this.page + 1, true);
                location.href = hash;
            } else if ($link.hasClass("page-last")) {
                await this.loadList(true, this.pages, true);
                location.href = "#page=" + this.pages;
            }
        });

        //edit button event
        this.$listContainer.on("click", ".btn-edit", async (e) => {
            e.preventDefault();

            const $btn = findClickedButton(e, "btn-edit");

            const id = $btn.data(this.idKey);

            const item = await this.getItem(this.idKey, id);

            if (item) {
                await this.setEditValues(item);
            }
        });


        this.$listContainer.on("click", ".btn-delete", async (e) => {
            await this.deleteItem(e);
        });

        this.$listContainer.on("click", ".btn-login", (e) => {
            e.preventDefault();

            location.href = '/login?path=' + location.href;
        })

        //form submit event
        if (this.$form) {
            this.setFormSubmit();
        }
    }

    /**
     * set the values to the edit form
     * @param {*} item 
     * @param {*} prefix 
     */
    async setEditValues(item, prefix = "") {
        if (prefix == "") {
            prefix = this.prefix;
        }

        $(`#form-${this.prefix}title`).text(`Edit:${item[this.nameKey]}`);

        for (const key in item) {
            // const $input = $(`#${prefix}${key}`);
            const $input = $(`[name='${prefix}${key}']`);

            if ($input.length === 0) {
                continue;
            } else if ($input.length === 1) {
                if ($input.is(":checkbox")) {
                    //for checkbox
                    $input.prop("checked", item[key]);
                } else if ($input.is(":file")) {
                    $input.val('');
                } else {
                    $input.val(item[key]);
                }
            } else {
                //multiple input element
                if ($($input[0]).is(":checkbox")) {
                    const value = item[key];
                    //checkbox list
                    for (let i = 0; i < $input.length; i++) {
                        const $checkbox = $($input[i]);
                        $checkbox.prop("checked", false);
                        for (let j = 0; j < value.length; j++) {
                            if (value[j] == $checkbox.val()) {
                                $checkbox.prop("checked", true);
                                break;
                            }
                        }
                    }
                }
            }
        }
    }

    /**
     * Delete item
     * @param {*} e 
     */
    async deleteItem(e) {
        e.preventDefault();
        const $btn = findClickedButton(e, "btn-delete");

        const id = $btn.data(this.idKey);
        try {
            const resp = await axios.delete(this.getDeleteUrl(id));

            await this.loadList(true, 0, true);
        } catch (error) {
            showAlert("Error when deleting!", config.ALERT_ERROR);
        }
    }

    /**
     * setup the form submit event
     */
    setFormSubmit() {
        this.$form.off("submit");
        this.$form.on("submit", async (e) => {
            e.preventDefault();

            const $modal = this.$form.parents(".modal");
            const $modalLoading = $modal.find(".modal-loading");

            this.$form.addClass("d-none");
            $modalLoading.removeClass("d-none");

            try {
                formFunc.showFormError(this.$form, "");

                const id = $(`#${this.prefix}${this.idKey}`).val();
                let url = this.insertUrl;
                let method = "post";

                if (id) {
                    url = this.getUpdateUrl(id)
                    method = "patch";
                }


                const resp = await formFunc.postForm(this.$form, url, method, true);

                if (resp.data.item) {
                    if (resp.status === 201) {
                        $modal.modal("hide");

                        //create successfully
                        await this.loadList(true, 0, true);

                        this.resetForm();
                    } else if (id && resp.status === 200) {
                        $modal.modal("hide");

                        //update successfully
                        await this.loadList(true, 0, true);

                        this.resetForm();
                    }
                } else {
                    if (resp.data.error) {
                        formFunc.showFormError(this.$form, resp.data.error);
                    } else if (resp.data.errors) {
                        const errors = resp.data.errors;
                        formFunc.showFormError(this.$form, "", errors);
                    }
                }

            } catch (error) {
                formFunc.showFormError(this.$form, "Error when updating data!");
            }

            this.$form.removeClass("d-none");
            $modalLoading.addClass("d-none");
        });
    }

    /**
     * Reset form
     */
    resetForm() {
        $(`#form-${this.prefix}title`).text(this.newTitle);
        $(`#${this.prefix}${this.idKey}`).val('');
        formFunc.showFormError(this.$form, "");
        formFunc.resetForm(this.$form);
    }

    /**
     * List All items
     * @param {*} reload 
     * @param {*} page
     * @param {*} loadPager
     */
    async loadList(reload = false, page = 0, loadPager = false) {

        if (page == 0) {
            const hash = location.hash;

            if (hash.startsWith("#page=")) {
                page = parseInt(hash.substr(6));
            } else {
                page = 1;
            }

            this.page = page;
        }

        const list = await this.getList(reload, page);

        this.$listContainer.html('');

        for (let i = 0; i < list.length; i++) {
            this.$listContainer.append(this.getHtml(list[i]));
        }

        if (loadPager && this.pages > 1) {
            this.$listContainer.append(this.getPagerHtml());
        }
    }

    /**
     * Return the html
     * @param {*} item 
     */
    getHtml(item) {
        // return this.template.replaceAll("%%item%%", item);
        let html = this.template;
        for (const prop in item) {
            html = html.replaceAll(`%%${prop}%%`, item[prop]);
        }

        return html;
    }


    /**
     * Return the pager html
     */
    getPagerHtml() {
        let html = `
        <div class="col-12 h4 p-3 pager">
            <div class="mx-auto container">
        `;
        if (this.page > 1) {
            html += `
            <a href="javascript:void(0);" class="text-primary page-first">First</a>
            <a href="javascript:void(0);" class="text-primary page-prev">Previous</a>
            `;
        }

        if (this.page < this.pages) {
            html += `
            <a href="javascript:void(0);" class="text-primary page-next">Next</a>
            <a href="javascript:void(0);" class="text-primary page-last">Last</a>
            `;
        }

        html += `
        Current page <span class="text-primary">${this.page}</span> of <span class="text-primary">${this.pages}</span>
        `;
        html += `
            </div>
        </div>
        `;

        return html;
    }

    /**
     * Return the list
     * @param {*} reload 
     * @param {*} page
     */
    async getList(reload = false, page = 1) {

        if (this.items == null || reload === true) {
            //Load the services if not loaded yet
            const resp = await axios.get(this.getUrl(page));

            this.items = resp.data.items;
            this.page = resp.data.page;
            this.pages = resp.data.pages;
            this.per_page = resp.data.per_page;
            this.total = resp.data.total;
        }
        return this.items;
    }

    /**
     * Return the item with the key
     * @param {*} key 
     * @param {*} value 
     */
    async getItem(key, value) {

        const items = await this.getList();

        for (let i = 0; i < items.length; i++) {
            if (items[i][key] == value) {
                return items[i];
            }
        }

        return null;
    }

    /**
     * Return the update url
     * @param {*} id 
     */
    getUpdateUrl(id) {

        if (this.updateUrl.includes("?")) {
            let strs = this.updateUrl.split("?", 2)
            return strs[0].substring(0, strs[0].length - 1) + id + "?" + strs[1];

        }
        else {
            return this.updateUrl.substring(0, this.updateUrl.length - 1) + id;
        }
    }


    /**
     * Return the update url
     * @param {*} id 
     */
    getDeleteUrl(id) {

        if (this.deleteUrl.includes("?")) {
            let strs = this.deleteUrl.split("?", 2)
            return strs[0].substring(0, strs[0].length - 1) + id + "?" + strs[1];

        }
        else {
            return this.deleteUrl.substring(0, this.deleteUrl.length - 1) + id;
        }
    }

    /**
     * Method to get the request url from querystring
     */
    getUrl(page = 1) {
        let params = new URLSearchParams(window.location.search);

        let url = this.url;

        if (this.per_page > 0) {
            params.delete("per_page");
            params.append("per_page", this.per_page);

        }
        if (page > 1) {
            params.delete("page");
            params.append("page", page);
        }

        const queryString = params.toString();
        if (queryString.length > 0) {
            if (url.includes('?')) {
                url += '&' + queryString;
            } else {
                url += '?' + queryString;
            }
        }

        return url;
    }
}

export { ListBasic as default }