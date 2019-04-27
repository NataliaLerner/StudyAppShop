function sendJsonAndGetTextFromService(url, data, type) {
    return $.ajax({
        type: type,
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        dataType: 'json',
        async: false,
        success:function (data) {
            return data;
        }
    }).responseText;
}

function sendTextAndGetTextFromService(url, data, type) {
    return $.ajax({
        type: type,
        url: url,
        data: data,
        contentType: "text/plain",
        async: false,
        success:function (data) {
            return data;
        }
    }).responseText;
}