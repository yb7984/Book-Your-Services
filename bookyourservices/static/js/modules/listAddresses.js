import ListBasic from '/static/js/modules/list.js'
import * as formFunc from '/static/js/modules/form.js'

class ListAddresses extends ListBasic {
    /**
     * Return the html of the address
     * @param {*} item 
     */
    getHtml(item) {
        return this.template
            .replaceAll("%%id%%", item.id)
            .replaceAll("%%address%%", item.address.replaceAll("\n", "<br />"))
            .replaceAll("%%is_default%%", item.is_default ? "Default" : "")
            .replaceAll("%%is_active%%", item.is_active ? "" : "Inactive");
    }
}

export { ListAddresses as default };