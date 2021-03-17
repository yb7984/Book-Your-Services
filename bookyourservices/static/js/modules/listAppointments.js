import ListBasic from '/static/js/modules/list.js';
import * as config from '/static/js/config.js';

/**
 * Class for list items from appointments
 */
class ListAppointments extends ListBasic {

    /**
     * Load events
     */
    event(){
        super.event();

        this.$listContainer.on("click" , ".btn-note" , async (e)=>{

            e.preventDefault();
            const $btn = findClickedButton(e, "btn-note");

            const id = $btn.data(this.idKey);

            const item = await this.getItem(this.idKey, id);

            if (item.note != ""){
                showAlert(item.note);
            }
        });
    }

    /**
     * Return the html of the service
     * @param {*} item 
     */
    getHtml(item) {
        return this.template
            .replaceAll("%%id%%", item.id)
            .replaceAll("%%summary%%", item.summary)
            .replaceAll("%%service%%", item.service)
            .replaceAll("%%provider%%", item.provider_username)
            .replaceAll("%%customer%%", item.customer_username)
            .replaceAll("%%service_date%%", (new Date(item.start)).toLocaleString(config.DATE_FORMAT_LANG, config.DATE_FORMAT_OPTIONS))
            .replaceAll("%%start%%", (new Date(item.start)).toLocaleString(config.DATE_FORMAT_LANG, config.TIME_FORMAT_OPTIONS))
            .replaceAll("%%end%%", (new Date(item.end)).toLocaleString(config.DATE_FORMAT_LANG, config.TIME_FORMAT_OPTIONS))
            .replaceAll("%%no_note%%", item.note === "" ? "d-none": "")
            .replaceAll("%%description%%", item.description.replaceAll("\n", "<br />"))
            .replaceAll("%%is_active%%", item.is_active ? `<span class="text-success">Active</span>` : `<span class="text-danger">Inactive</span>`);
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

        const start = item.start;
        const end = item.end;

        for (const key in item) {
            // const $input = $(`#${prefix}${key}`);
            const $input = $(`[name='${prefix}${key}']`);

            if ($input.length === 0) {
                continue;
            } else if ($input.length === 1) {
                $input.val(item[key]);
            }
        }
        const $service_date = $(`[name='${prefix}service_date']`);
        const $times = $(`[name='${prefix}times']`);

        $service_date.val(start.substr(0, 10));
        $times.val(`${start.substr(11, 5)}-${end.substr(11, 5)}`);

        if (!$times.hasClass("d-none")) {
            $times.addClass("d-none");

            $times.after($(`
            <select class="custom-select" id="appointment-times-select">
            </select>`));

            const $timesSelector = $("#appointment-times-select");

            $timesSelector.on("change", (e) => {
                $times.val($timesSelector.val());
            });

            $service_date.on("change", async (e) => {
                await this.loadAvailableTimes(item.provider_username, $service_date.val(), item.id);
            });
        }

        //load times
        await this.loadAvailableTimes(item.provider_username, $service_date.val(), item.id);

        const $timesSelector = $("#appointment-times-select");
        $timesSelector.val($times.val());
    }


    /**
     * List All items
     * @param {*} reload 
     * @param {*} page
     * @param {*} loadPager
     */
    async loadList(reload = false, page = 1, loadPager = false) {

        await super.loadList(reload , page , loadPager);
        
        const $rows = this.$listContainer.find(".appointment-item");


        for (let i = 0 ; i < $rows.length ; i ++){
            if (i % 2 == 0){
                $($rows[i]).addClass("bg-light");
            }
        }
    }

    /**
     * Load available times of the date
     * @param {*} username 
     * @param {*} date 
     * @param {*} appointment_id
     */
    async loadAvailableTimes(username, date, appointment_id) {
        const resp = await axios.get(`/api/schedules/${username}/${date}/${appointment_id}`);

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
}

export { ListAppointments as default };