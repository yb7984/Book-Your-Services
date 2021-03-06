import ListBasic from '/static/js/modules/list.js'

class ListAppointments extends ListBasic {
    /**
     * Return the html of the service
     * @param {*} item 
     */
    getHtml(item) {
        console.log(item);
        return this.template
            .replaceAll("%%id%%", item.id)
            .replaceAll("%%summary%%", item.summary)
            .replaceAll("%%provider%%", item.provider_username)
            .replaceAll("%%customer%%", item.customer_username)
            .replaceAll("%%start%%", (new Date(item.start)).toLocaleString(DATE_FORMAT_LANG, DATE_FORMAT_OPTIONS))
            .replaceAll("%%end%%", (new Date(item.end)).toLocaleString(DATE_FORMAT_LANG, DATE_FORMAT_OPTIONS))
            // .replaceAll("%%location_type%%", item.location_type)
            .replaceAll("%%note%%", item.note.replaceAll("\n", "<br />"))
            .replaceAll("%%description%%", item.description.replaceAll("\n", "<br />"))
            .replaceAll("%%is_active%%" , item.is_active ? `<span class="text-success">Active</span>` : `<span class="text-danger">Inactive</span>`);
    }
}

export {ListAppointments as default};