import ListBasic from '/static/js/modules/list.js';
import * as formFunc from '/static/js/modules/form.js';

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
            .replaceAll("%%location_type%%", item.location_type_name)
            .replaceAll("%%description%%", item.description.replaceAll("\n", "<br />"))
            .replaceAll("%%image%%", item.image_url)
            .replaceAll("%%is_active%%", item.is_active ? `<span class="text-success">Active</span>` : `<span class="text-danger">Inactive</span>`);

        if (CURRENT_USERNAME === item.username) {
            //this service is belong to current login user, hide the appointment button

            html = html.replaceAll("btn-appointment", "btn-appointment d-none");
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
            const $btn = findClickedButton(e, "btn-appointment");

            const id = $btn.data("id");

            this.current_service = await this.getItem("id", id);

            $("#form-appointment-title").html(`Make appointment with <label class="text-primary">${this.current_service.name}</label>`);
            $("#appointment-service_id").val(this.current_service.id);
            $("#appointment-provider_username").val(this.current_service.username);
        });

        if ($("#form-appointment-").length > 0) {
            //appointment submit event
            $("#form-appointment-").on("submit", async (e) => {
                e.preventDefault();

                const $form = $("#form-appointment-");
                const $formContainer = $("#form-appointment-container");
                try {
                    formFunc.showFormError($form, "");

                    let url = "/api/appointments";
                    let method = "post";

                    const resp = await formFunc.postForm($form, url, method);

                    if (resp.data.item) {
                        if (resp.status === 201) {
                            this.resetAppointmentForm();
                            $formContainer.modal("hide");

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
            });
        }

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