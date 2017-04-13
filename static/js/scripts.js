$(document).ready(function () {
    $("#delete").click(function () {
        var id = $('#english')[0].name;
        $.ajax({
            url: window.location.origin + "/manage",
            type: "DELETE", // Use DELETE
            data: {id: id},
            success: function (result) {
                window.location.replace(window.location.origin);
                alert(result);

            }
        })
    });
});

$(document).ready(function () {
    $("#update").click(function () {
        var id = $('#english')[0].name;
        var eng = $('#english').val();
        inputs=$('#words input');
        dict={id:id,eng:eng};
        for (i = 1; i < inputs.length; i+=2) {
            dict["lt"+i] = inputs[i-1].value;
            dict["link"+i] = inputs[i].value;
        }
        $.ajax({
            url: window.location.origin + "/manage",
            type: "PUT",
            data: dict,
            success: function (result) {
                window.location.replace(window.location.origin+"/manage/"+eng);
                alert(result);

            }
        })
    });
});