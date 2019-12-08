function reset() {
    var input = document.getElementById('env_input_static_{{ environment_input.id }}')
    input.value = {{ environment_input.static_values.value_default }};
    update_env_{{ environment_input.id }}()
};
