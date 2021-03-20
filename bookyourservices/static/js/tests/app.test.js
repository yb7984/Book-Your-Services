describe("app.js test (with setup and tear-down)", function () {
    beforeEach(function () {
        // initialization logic
    });

    it('test for getGlobalValues()', function () {
        $(document).data("test", "test-data");

        expect(getGlobalValues("test")).toEqual("test-data");
    });


    it('test for findClickedButton()', function () {

        $("#btn-edit").on("click", function (e) {
            expect(findClickedButton(e, "btn-edit")[0]).toEqual($("#btn-edit")[0]);
        });
        $("#btn-edit").trigger("click");
        $("#icon").trigger("click");
    });


    it('test for showAlert()', function (done) {
        showAlert("test-alert", "success");

        setTimeout(function () {
            expect($("#alert-modal").is(":visible")).toEqual(true);
            expect($("#alert-content").text()).toContain("test-alert");
            expect($("#alert-content").find("label").hasClass("text-success")).toEqual(true);


            $("#alert-modal").modal("hide");

            done();
        }, 2000);
    });



    it('test for getPageUrl()', function () {
        if (location.search) {
            expect(getPageUrl(1)).toEqual(location.pathname + location.search + "&page=1");
        } else {
            expect(getPageUrl(1)).toEqual(location.pathname + "?page=1");
        }
    });

    afterEach(function () {
        // teardown logic
    });
});
