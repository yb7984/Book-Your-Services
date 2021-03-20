import * as formFunc from '../modules/form.js';

describe("form.js test (with setup and tear-down)", function () {
    beforeEach(function () {
        // initialization logic

        $("#name").val("name_test");
        $("#select").val("2");
    });

    it('test for resetForm()', function () {
        formFunc.resetForm($("#form-"));

        expect($("#name").val()).toEqual("");
        expect($("#select").val()).toEqual("1");
        expect($("#form--error").is(":visible")).toEqual(false);

        const $errors = $("#form-").find(".form-error");

        for (const error of $errors){
            expect($(error).text()).toEqual("");
        }
    });


    it('test for showFormError()', function () {
        formFunc.showFormError($("#form-"),
            "test-error-message",
            {
                "name": ["name error 1", "name error 2"],
                "select": ["select error 1"]
            });

        expect($("#form--error").is(":visible")).toEqual(true);
        expect($("#form--error").text()).toEqual("test-error-message");

        expect($("#form--error-name").text()).toContain("name error 1");
        expect($("#form--error-name").text()).toContain("name error 2");
        expect($("#form--error-select").text()).toContain("select error 1");
    });



    it('test for getFormData()', function () {
        
        const formData = formFunc.getFormData($("#form-"));


        expect(formData.has("name")).toEqual(true);
        expect(formData.has("select")).toEqual(true);


        expect(formData.get("name")).toEqual("name_test");
        expect(formData.get("select")).toEqual("2");
    });


    afterEach(function () {
        // teardown logic
    });
});
