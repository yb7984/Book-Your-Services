import ListBasic from '../modules/list.js';

let list = null;

describe("form.js test (with setup and tear-down)", function () {
    beforeEach(function () {
        // initialization logic

        list = new ListBasic(
            $("#test-list"),
            `%%id%% , %%name%%`,
            "./list.test.json"
        );
    });

    it('test for getHtml()', function () {

        expect(list.getHtml({ "id": 1, "name": "test" })).toEqual("1 , test");
    });

    it('test for getPagerHtml()', async function () {
        await list.loadList(true, 1, true);

        const html = list.getPagerHtml();

        expect(html).not.toContain("page-first");
        expect(html).not.toContain("page-previous");
        expect(html).toContain("page-next");
        expect(html).toContain("page-last");
    });


    it('test for getList()', async function () {
        const data = await list.getList(true, 1);

        expect(list.total).toEqual(30);
        expect(list.per_page).toEqual(3);
        expect(list.items.length).toEqual(3);
        expect(list.page).toEqual(1);
    });



    it('test for getItem()', async function () {
        const item = await list.getItem(1);

        expect(item.id).toEqual(1);
        expect(item.name).toEqual('test-name-1');
    });


    it('test for getUpdateUrl()', function () {
        list.updateUrl = "/update/0";

        expect(list.getUpdateUrl(1)).toEqual("/update/1");
    });

    it('test for getDeleteUrl()', function () {
        list.deleteUrl = "/delete/0";

        expect(list.getDeleteUrl(1)).toEqual("/delete/1");
    });


    it('test for getUrl()', function () {
        if (location.search) {
            let params = new URLSearchParams(window.location.search);

            expect(list.getUrl(1)).toEqual("./list.test.json?" + params.toString());
            expect(list.getUrl(2)).toEqual("./list.test.json?" + params.toString() + "&page=2");
        } else {

            expect(list.getUrl(1)).toEqual("./list.test.json");
            expect(list.getUrl(2)).toEqual("./list.test.json?page=2");
        }
    });



    afterEach(function () {
        // teardown logic
    });
});
