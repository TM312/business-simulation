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


<script>

    $(document).ready(function () {

        $.get("{{ url_for('jsonmodel') }}", function (data) {
            var environment_input = data.environment_inputs
            console.log(environment_input)
            $.each(environment_input, function () {
                $('#v-pills-environmental_inputs').load("{{url_for('static', filename='_environment_input2.html') }}");

                var id = this.id
                var name = this.name
                var input_type = this.input_type
                var value_min = this.value_min;
                var value_max = this.value_max;
                var step = this.step;
                var value = this.value_default;
                var description = this.description;
                var sources = this.sources;
                console.log(name)

                $('#name').text(name);
                $('#input_type').val(input_type);
                $("#input").attr({
                    "max": value_max,
                    "min": value_min,
                    "step": step,
                    "value": value,
                });
                $('#description').text(description);
                $('#sources').attr({
                    "data-content": sources,

                });
            });
        });
});

                    </script>

