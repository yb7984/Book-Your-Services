import ListBasic from '/static/js/modules/list.js'

class ListProviders extends ListBasic {
    /**
     * Return the html of the provider
     * @param {*} item 
     */
    getHtml(item) {
        return this.template
            .replaceAll("%%first_name%%", item.first_name)
            .replaceAll("%%last_name%%", item.last_name)
            .replaceAll("%%full_name%%", item.full_name)
            .replaceAll("%%username%%", item.username)
            .replaceAll("%%description%%", item.description.replaceAll("\n", "<br />"))
            .replaceAll("%%email%%", item.email)
            .replaceAll("%%phone%%", item.phone)
            .replaceAll("%%image%%", item.image_url);
    }
}

export { ListProviders as default };