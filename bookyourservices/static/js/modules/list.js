/**
 * Basic class for list items from ajax resource
 */
class BasicList {
    constructor($list, template, url) {
        this.$listContainer = $list;
        this.template = template;
        this.url = url;

        this.items = null;
    }


    
    /**
     * List All items
     * @param {*} reload 
     * @param {*} page
     */
    async loadList(reload = false, page=1) {

        const list = await this.getList(reload, page);

        this.$listContainer.html('');

        list.forEach(item => {
            this.$listContainer.append(this.getHtml(item));
        });
    }

    /**
     * Return the html
     * @param {*} item 
     */
    getHtml(item) {
        return this.template.replaceAll("item" , item);
    }

    /**
     * Return the list
     * @param {*} reload 
     * @param {*} page
     */
    async getList(reload = false, page=1) {

        if (this.items == null || reload === true) {

            console.log(this.getUrl())
            //Load the services if not loaded yet
            const resp = await axios.get(this.getUrl(page));

            this.items = resp.data.items;
        }
        return this.items;
    }


    /**
     * Method to get the request url
     */
    getUrl(page=1){
        let params = new URLSearchParams(window.location.search);

        let url = this.url;
        if (this.url.includes("?")){
            url += `&${params.toString()}`
        }

        url += `?${params.toString()}`;

        if (page > 1){
            url += `&page=${page}`;
        }

        return url;
    }
}

export {BasicList as default}