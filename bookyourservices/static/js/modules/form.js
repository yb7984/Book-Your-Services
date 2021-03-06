/**
 * Reset a jQuery form
 * @param {*} $form 
 */
export function resetForm($form) {
    $form.trigger("reset");
    showFormError($form, "");
}


/**
 * Show form error messages
 * @param {*} $form 
 * @param {*} message 
 * @param {*} messageList 
 */
export function showFormError($form, message, messageList = {}) {
    const $msgLabel = $form.find(".form-error-message");
    $msgLabel.text(message);
    if (message.length > 0) {
        $msgLabel.removeClass("d-none");
    } else {
        $msgLabel.addClass("d-none");
    }
    //clear field error messages
    $form.find(".form-error").text('');
    const formId = $form.attr("id");

    for (const key in messageList) {
        $(`#${formId}-error-${key}`).html(messageList[key].join("<br />"));
    }
}

/**
 * Post form data to target url and return a response
 * @param {*} $form 
 * @param {*} url 
 * @param {*} method
 */
export async function postForm($form, url, method = "POST", withFiles = false) {
    //post the infomation
    method = method.toLowerCase();
    let config = {};

    if (withFiles === true) {
        config["headers"] = { 'Content-Type': 'multipart/form-data' };
    } else {
        config["headers"] = { 'Content-Type': 'application/json' };
    }

    console.log(config);

    if (method === "patch") {
        return await axios.patch(url, getFormData($form), config);
    } else if (method === "put") {
        return await axios.put(url, getFormData($form), config);
    } else if (method === "delete") {
        return await axios.delete(url, getFormData($form));
    }
    return await axios.post(url, getFormData($form), config);
}


/**
 * Input a jQuery form item and return a FormData object of the data of the form
 * @param {*} $form 
 */
export function getFormData($form) {
    const data = $form.serializeArray();

    const formData = new FormData();

    data.forEach(({ name: key, value: val }) => {
        
        formData.append(key, val);
    });


    const files = $form.find("input[type='file']");

    if (files.length > 0) {
        for (let i = 0; i < files.length; i++) {
            
            if (files[i].files.length > 0) {
                formData.append(files[i].name, files[i].files[0]);
            }
        }
    }

    return formData;
}