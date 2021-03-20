import ListBasic from './list.js'

/**
 * Class for list items from categories
 */
class ListCategories extends ListBasic {
    /**
     * Return the html of the provider
     * @param {*} item 
     */
    getHtml(item) {
        return this.template
        .replaceAll("%%id%%", item.id)
        .replaceAll("%%name%%", item.name)
        .replaceAll("%%is_active%%", item.is_active ? `<i class="fas fa-check text-success"></i>` : `<i class="fas fa-times text-danger"></i>`);
    }
}

export { ListCategories as default };