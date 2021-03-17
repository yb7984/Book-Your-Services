import ListBasic from '/static/js/modules/list.js';
import * as formFunc from '/static/js/modules/form.js';

/**
 * Class for list items from service
 */
class ListServices extends ListBasic {
    /**
     * Return the html of the service
     * @param {*} item 
     */
    getHtml(item) {

        let categories = "";
        item.categories.forEach(item => {
            if (categories.length > 0) {
                categories += ", ";
            }
            categories += item.name;
        })
        let html = this.template
            .replaceAll("%%id%%", item.id)
            .replaceAll("%%name%%", item.name)
            .replaceAll("%%username%%", item.username)
            .replaceAll("%%provider%%", item.provider)
            .replaceAll("%%categories%%", categories)
            .replaceAll("%%description%%", item.description.replaceAll("\n", "<br />"))
            .replaceAll("%%image%%", item.image_url)
            .replaceAll("%%is_active%%", item.is_active ? `<span class="text-success">Active</span>` : `<span class="text-danger">Inactive</span>`);

        const current_username = getGlobalValues("CURRENT_USERNAME");
        
        if (!current_username || current_username === item.username) {
            //this service is belong to current login user, hide the appointment button

            html = html.replaceAll("btn-appointment", "btn-appointment d-none");
        }
        if (current_username) {
            html = html.replaceAll("btn-login", "btn-login d-none");
        }
        return html;
    }


    /**
     * event handlers
     */
    event() {
        //parent class's event handlers
        super.event();

        //appointment event
        this.$listContainer.on("click", ".btn-appointment", async (e) => {
            await this.openAppointment(e);
        });

        if ($("#form-appointment-").length > 0) {
            //appointment submit event
            $("#form-appointment-").on("submit", async (e) => {
                await this.submitAppointment(e)
            });
        }

    }

    /**
     * Open the appointment modal
     * @param {*} e 
     */
    async openAppointment(e) {
        const $btn = findClickedButton(e, "btn-appointment");

        const $form = $("#form-appointment-");
        formFunc.showFormError($form, "");

        const id = $btn.data("id");

        this.current_service = await this.getItem("id", id);

        this.initAppointmentForm();

        $("#form-appointment-title").html(`Make appointment with <label class="text-primary">${this.current_service.name}</label>`);
        $("#appointment-service_id").val(this.current_service.id);
        $("#appointment-provider_username").val(this.current_service.username);
    }

    /**
     * initial the appointment form
     */
    async initAppointmentForm() {
        const $times = $("#appointment-times");
        const $date = $("#appointment-service_date");

        if (!$times.hasClass("d-none")) {
            $times.addClass("d-none");

            $times.after($(`
            <select class="custom-select" id="appointment-times-select">
            </select>`));

            const $timesSelector = $("#appointment-times-select");

            $timesSelector.on("change", (e) => {
                $times.val($timesSelector.val());
            });

            $date.on("change", async (e) => {
                await this.loadAvailableTimes(this.current_service.username, $date.val());
            });
        }

        //load times
        const today = (new Date(Date.now())).toISOString().substr(0, 10);

        $date.val(today);

        await this.loadAvailableTimes(this.current_service.username, $date.val());

        const $timesSelector = $("#appointment-times-select");
        $times.val($timesSelector.val());
    }

    /**
     * Load available times of the date
     * @param {*} username 
     * @param {*} date 
     */
    async loadAvailableTimes(username, date) {
        const resp = await axios.get(`/api/schedules/${username}/${date}/0`);

        const items = resp.data.items;

        const $timesSelector = $("#appointment-times-select");
        $timesSelector.html("");
        items.forEach(item => {
            $timesSelector.append(`
            <option value="${item["start"]}-${item["end"]}">
                ${item["start"]}-${item["end"]}
            </option>`)
        });
    }

    /**
     * Submit the appointment
     * @param {*} e 
     */
    async submitAppointment(e) {

        e.preventDefault();

        const $form = $("#form-appointment-");
        const $formContainer = $("#form-appointment-container");
        const $formLoading = $formContainer.find(".modal-loading");

        $form.addClass("d-none");
        $formLoading.removeClass("d-none");

        try {
            formFunc.showFormError($form, "");

            let url = "/api/appointments";
            let method = "post";

            const resp = await formFunc.postForm($form, url, method);

            if (resp.data.item) {
                if (resp.status === 201) {
                    this.resetAppointmentForm();
                    $formContainer.modal("hide");

                    formFunc.showFormError($form, "");

                    showAlert("Successfully make appointment!")
                }
            } else {
                if (resp.data.error) {
                    formFunc.showFormError($form, resp.data.error);
                } else if (resp.data.errors) {
                    const errors = resp.data.errors;
                    formFunc.showFormError($form, "", errors);
                }
            }

        } catch (error) {
            formFunc.showFormError($form, "Error when updating data!");
        }


        $form.removeClass("d-none");
        $formLoading.addClass("d-none");
    }

    /**
    * Reset the form to original status
    */
    resetAppointmentForm() {
        $("#form-appointment-title").text("New Appointment");
        $("#appointment-service_id").val('');
        $("#appointment-provider_username").val('');
        formFunc.resetForm($("#form-appointment-"));
    }
}

export { ListServices as default };