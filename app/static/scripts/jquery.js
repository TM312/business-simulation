$(document).ready(function () {
    $.get("{{ url_for('jsonmodel') }}", function (data) {
        var name = data.environment_inputs[0].name
        $('#name').text(name);
        var input_type = data.environment_inputs[0].input_type
        $('#input_type').val(input_type);

        var value_min = data.environment_inputs[1].value_min;
        var value_max = data.environment_inputs[1].value_max;
        var step = data.environment_inputs[1].step;
        var value = data.environment_inputs[1].value_default;

        $("#input").attr({
            "max": value_max,
            "min": value_min,
            "step": step,
            "value": value,
        });
        var description = data.environment_inputs[1].description;
        $('#description').text(description);
        var sources = data.environment_inputs[0].sources;
        $('#sources').attr({
            "data-content": sources,
        });
    });
});



