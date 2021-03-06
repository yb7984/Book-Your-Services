import ListBasic from '/static/js/modules/list.js';
import * as formFunc from '/static/js/modules/form.js';

class ListSchedules extends ListBasic {
    /**
     * Events
     */
    event() {
        this.$formModal = this.$form.parents(".modal");
        this.$formTitle = this.$formModal.find(".modal-title");
        this.$date_exp_weekly = this.$form.find(`[name='${this.prefix}date_exp_weekly']`);
        this.$date_exp_dates = $(`#${this.prefix}date_exp_dates`);
        this.$schedules = $(`#${this.prefix}schedules`);

        //change the display of the form
        this.initForm();

        //edit button event
        this.$listContainer.on("click", ".btn-edit", async (e) => {
            e.preventDefault();

            const $btn = findClickedButton(e, "btn-edit");

            await this.openUpdate($btn);
        });


        this.$listContainer.on("click", ".btn-delete", async (e) => {
            await this.deleteItem(e);
        });
    }



    /**
     * Return the name of the schedule
     * @param {*} date_exp 
     */
    getName(date_exp) {
        if (date_exp.length != 1 && (parseInt(date_exp) > 6 || parseInt(date_exp) < 0)) {
            return date_exp;
        }

        return WEEKDAYS[parseInt(date_exp)];
    }

    /**
     * Return the schedule list HTML
     * @param {*} item 
     */
    getSchedulesHtml(item) {
        let html = "";
        if (item.schedules.length > 0) {
            const list = JSON.parse(item.schedules);

            list.forEach(schedule => {
                html += ` <div class="text-info h6 border border-light rounded p-2">
                ${schedule.start} - ${schedule.end}
            </div>`;
            })
        }

        return html;
    }

    /**
     * Return the html of the schedule
     * @param {*} item 
     */
    getHtml(item) {
        const htmlSchedules = this.getSchedulesHtml(item);
        return this.template
            .replaceAll("%%name%%", this.getName(item.date_exp))
            .replaceAll("%%date_exp%%", item.date_exp)
            .replaceAll("%%schedules%%", htmlSchedules)
            .replaceAll("%%is_active%%", item.is_active ? "" : "Inactive");
    }


    /**
     * init the display for form
     */
    initForm() {

        if ($(`#${this.prefix}date_exp_date`).length === 0) {
            console.log("initForm")

            this.$date_exp_dates.addClass("d-none");
            this.$date_exp_dates.after(`
    <div class="row">
        <div class="col-8">
        <input type="date" class="form-control" id="${this.prefix}date_exp_date" />
        </div>
        <div class="col-4">
            <button class="btn btn-success btn-schedules-dates-add"><i class="fa fa-plus"></i></button>
        </div>
    </div>
    <div id="${this.prefix}dates-container" class="row container">
    </div>`);

            //hide the original schedules input box
            this.$schedules.addClass("d-none");

            this.$schedules.after(`
    <button class="btn btn-success btn-schedules-add"><i class="fa fa-plus"></i></button>
    <div id="${this.prefix}schedules-container">
    </div>`);

        }

        this.$datesContainer = $(`#${this.prefix}dates-container`);
        this.$schedulesContainer = $(`#${this.prefix}schedules-container`);


        //event for adding specific dates
        this.$form.off("click", ".btn-schedules-dates-add");
        this.$form.on("click", ".btn-schedules-dates-add", (e) => {
            e.preventDefault();

            const $date = $(`#${this.prefix}date_exp_date`);
            const newValue = $date.val();

            this.addScheduleDate(newValue);

            $date.val("");
        });


        //event for adding specific dates
        this.$form.off("click", ".btn-schedule-date-delete");
        this.$form.on("click", ".btn-schedule-date-delete", (e) => {
            this.deleteScheduleDate(e);
        });

        //schedules add button event
        this.$form.off("click", ".btn-schedules-add");
        this.$form.on("click", ".btn-schedules-add", (e) => {
            e.preventDefault();

            console.log("btn-schedules-add");

            const $btn = findClickedButton(e, "btn-schedules-add");

            this.addSchedule();
        });


        //schedules delete button event
        this.$form.off("click", ".btn-schedules-delete");
        this.$form.on("click", ".btn-schedules-delete", (e) => {
            e.preventDefault();

            const $btn = findClickedButton(e, "btn-schedules-delete");

            const $container = $btn.parents(".schedule-schedules-time");

            $container.remove();
        });

        this.$form.off("submit");
        this.$form.on("submit", async (e) => {
            await this.postForm(e);
        });
    }

    /**
     * Open the update modal
     * @param {*} $btn 
     */
    async openUpdate($btn) {

        this.$formTitle.text("Edit Schedule");

        const date_exp = $btn.data("date_exp");

        for (let i = 0; i < this.$date_exp_weekly.length; i++) {
            const $checkbox = $(this.$date_exp_weekly[i]);

            $checkbox.prop("checked", $checkbox.val() == date_exp);
        }
        this.$date_exp_dates.val('');
        this.$datesContainer.html('');

        if (date_exp.length > 1) {
            this.addScheduleDate(date_exp);
        }

        //clear schedules container
        this.$schedulesContainer.html("");

        this.schedulesCount = 0;

        const schedule = await this.getItem(this.idKey , date_exp);

        if (schedule != null){
            const schedules = JSON.parse(schedule.schedules);

            schedules.forEach(item =>{
                this.addSchedule(item.start , item.end);
            });
        }
    }


    /**
     * Add a schedule date
     * @param {*} date 
     */
    addScheduleDate(date) {
        let currentValue = this.$date_exp_dates.val();

        if (date.length > 0 && !currentValue.includes(date)) {
            currentValue = (currentValue.length > 0 ? currentValue + ',' : '') + date;
            this.$date_exp_dates.val(currentValue);

            this.$datesContainer.append(`
        <div class="col-3 border rounded p-2 schedule-date-container text-center" data-date_exp="${date}">
            ${date}
            <button class="btn btn-danger btn-schedule-date-delete"><i class="fa fa-trash-alt"></i></button>
        </div>`)
        }
    }

    /**
     * Delete Schedule Date Event
     * @param {*} e 
     */
    deleteScheduleDate(e){

        e.preventDefault();

        const $btn = findClickedButton(e, "btn-schedule-date-delete");
        const $container = $btn.parents(".schedule-date-container");

        const date_exp = $container.data("date_exp");
        let currentValue = this.$date_exp_dates.val();

        currentValue = currentValue.replaceAll(date_exp, "").replaceAll(",,", ",");

        if (currentValue.startsWith(",")) {
            currentValue = currentValue.substring(1);
        }

        if (currentValue.endsWith(",")) {
            currentValue = currentValue.substring(0, currentValue.length - 1);
        }

        this.$date_exp_dates.val(currentValue);

        $container.remove();
    }

    /**
     * add a schedule time frame
     * @param {*} start 
     * @param {*} end 
     */
    addSchedule(start = "", end = "") {

        this.$schedulesContainer.append(`<div class="p-2 schedule-schedules-time row">
    <div class="col-4">
    <input type="time" class="form-control schedule-schedules-start"  name="${this.prefix}schedules-start" id="${this.prefix}schedules-start-${this.schedulesCount}" required />
    </div>
    <div class="col-1"> - </div>
    <div class="col-4">
    <input type="time" class="form-control schedule-schedules-end" name="${this.prefix}schedules-end" id="${this.prefix}schedules-end-${this.schedulesCount}" required /> 
    </div>
    <div class="col-3">
    <button class="btn btn-danger btn-schedules-delete" data-id="${this.schedulesCount}"><i class="fa fa-trash-alt"></i></button>
    </div>
    </div>`);

        $(`#${this.prefix}schedules-start-${this.schedulesCount}`).val(start);
        $(`#${this.prefix}schedules-end-${this.schedulesCount}`).val(end);

        this.schedulesCount++;
    }


    /**
     * Post Form
     * @param {*} e 
     */
    async postForm(e){
        e.preventDefault();

        console.log(this.$form.serializeArray());

        formFunc.showFormError(this.$form, '');

        const resp = await formFunc.postForm(this.$form, this.updateUrl);

        if (resp.data.items) {
            if (resp.status === 200) {
                this.$formModal.modal("hide");

                //reload schedules
                this.reload();
            }
        } else {
            if (resp.data.error) {
                formFunc.showFormError(this.$form, resp.data.error);
            } else if (resp.data.errors) {
                const errors = resp.data.errors;
                formFunc.showFormError(this.$form, "", errors);
            }
        }
    }

    /**
     * set the reload list
     * @param {*} list 
     */
    setReloadList(list){
        this.reloadList = list;
    }
    /**
     * Reload List data
     */
    reload(){
        this.reloadList.forEach(list => {
            list.loadList(true);
        });
    }
}

export { ListSchedules as default };