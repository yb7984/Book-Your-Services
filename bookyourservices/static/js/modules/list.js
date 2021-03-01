import * as formFunc from '/static/js/modules/form.js';
/**
 * Basic class for list items from ajax resource
 */
class ListBasic {
    constructor(
        $list,
        template,
        url,
        per_page = 0,
        form = null,
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

        this.$form = form;
        this.prefix = prefix;
        this.insertUrl = insertUrl;
        this.updateUrl = updateUrl;
        this.deleteUrl = deleteUrl;

        this.newTitle = newTitle;

        //indicating is the form is posting, avoid resubmiting
        this.formPosting = false;

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
            } else if ($link.hasClass("page-prev")) {
                await this.loadList(true, this.page - 1, true);
            } else if ($link.hasClass("page-next")) {
                await this.loadList(true, this.page + 1, true);
            } else if ($link.hasClass("page-last")) {
                await this.loadList(true, this.pages, true);
            }
        });

        //edit button event
        this.$listContainer.on("click", ".btn-edit", async (e) => {
            e.preventDefault();

            const $btn = findClickedButton(e, "btn-edit");

            const id = $btn.data(this.idKey);

            const item = await this.getItem(this.idKey, id);

            if (item) {
                this.setEditValues(item);
            }
        });


        this.$listContainer.on("click", ".btn-delete", async (e) => {
            e.preventDefault();
            const $btn = findClickedButton(e, "btn-delete");

            const id = $btn.data(this.idKey);

            // try {
            const resp = await axios.delete(this.deleteUrl.substring(0, this.deleteUrl.length - 1) + id);

            await this.loadList(true);
            // } catch (error) {
            //     showAlert("Error when deleting!", ALERT_ERROR);
            // }
        });

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
    setEditValues(item, prefix = "") {
        if (prefix == "") {
            prefix = this.prefix;
        }

        console.log(`#form-${this.prefix}title`);
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
     * setup the form submit event
     */
    setFormSubmit() {
        this.$form.on("submit", async (e) => {
            e.preventDefault();

            if (this.formPosting === true) {
                //avoid resubmitting
                alert("Form posting, please wait!");
                return false;
            }

            this.formPosting = true;

            // try {
            formFunc.showFormError(this.$form, "");

            const id = $(`#${this.prefix}${this.idKey}`).val();
            let url = this.insertUrl;
            let method = "post";

            if (id) {
                url = this.updateUrl.substring(0, this.updateUrl.length - 1) + id;
                method = "patch";
            }


            const resp = await formFunc.postForm(this.$form, url, method, true);

            if (resp.data.item) {
                const $modal = this.$form.parents(".modal");
                if (resp.status === 201) {
                    $modal.modal("hide");

                    //create successfully
                    await this.loadList(true);

                    this.resetForm();
                } else if (id && resp.status === 200) {
                    $modal.modal("hide");

                    //update successfully
                    await this.loadList(true);

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

            // } catch (error) {
            //     formFunc.showFormError(this.$form , "Error when updating data!");
            // }

            this.formPosting = false;
        });
    }

    /**
     * Reset form
     */
    resetForm() {
        console.log(`#form-${this.prefix}title`);
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
    async loadList(reload = false, page = 1, loadPager = false) {

        const list = await this.getList(reload, page);

        this.$listContainer.html('');

        console.log(list);

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
        return this.template.replaceAll("item", item);
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

            console.log(resp);
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
     * Method to get the request url from querystring
     */
    getUrl(page = 1) {
        let params = new URLSearchParams(window.location.search);

        let url = this.url;

        if (params.toString().length > 0) {
            if (this.url.includes("?")) {
                url += `&${params.toString()}`
            }
            else {
                url += `?${params.toString()}`;
            }
        }

        if (this.per_page > 0) {
            if (url.includes('?')) {
                url += `&per_page=${this.per_page}`;
            } else {
                url += `?per_page=${this.per_page}`;
            }
        }
        if (page > 1) {
            if (url.includes('?')) {
                url += `&page=${page}`;
            } else {
                url += `?page=${page}`;
            }
        }

        return url;
    }
}

export { ListBasic as default }