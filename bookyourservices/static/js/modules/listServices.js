import BasicList from '/static/js/modules/list.js'

class ServicesList extends BasicList {
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
        return this.template
            .replaceAll("%%id%%", item.id)
            .replaceAll("%%name%%", item.name)
            .replaceAll("%%username%%", item.username)
            .replaceAll("%%provider%%", item.provider)
            .replaceAll("%%categories%%", categories)
            .replaceAll("%%location_type%%", item.location_type_name)
            .replaceAll("%%description%%", item.description.replaceAll("\n", "<br />"))
            .replaceAll("%%image%%", item.image_url);
    }
}

export {ServicesList as default};