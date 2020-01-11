// while hovering over the output area this function displays the change in percentage to the default value next to it
function viewchange(input_id, change_id, default_value) {
    var output = parseFloat(document.getElementById(input_id).innerHTML);
    var change_display = document.getElementById(change_id);
    if (default_value == 0) {
        result = "default value: 0";
        if (output != default_value) {
            change_display.innerHTML = result
        };
    } else if (output != default_value ) {
            result = Math.round(((output - default_value) / default_value + Number.EPSILON / 100) * 100);
            if (result>0) {
            change_display.innerHTML = '+' + result + '%';
            } else {
                change_display.innerHTML = result + '%';
            };
    };
};

//this function clears the change display when hovering out of the output area
function clear_viewchange(change_id) {
    var change = document.getElementById(change_id);
    change.innerHTML = ""
};

// this function displays the inputs in the output field
function display_output_int(input_static_id, output_static_id, input_growth_id, output_growth_id) {
    var input_static = document.getElementById(input_static_id);
    var output_static = document.getElementById(output_static_id); 
    output_static.value = input_static.value;
    if (typeof input_growth_id !== 'undefined') {
        var input_growth = document.getElementById(input_growth_id); 
        var output_growth = document.getElementById(output_growth_id);    
        output_growth.value = input_growth.value;
    }
};

// this function creates arrays used for the simulation model and chart visualization based on the inputs
function create_arrays(max_T, input_type, static_input_id, static_output_id, growth_input_id, growth_output_id) {

    var input_static = document.getElementById(static_input_id);
    var output_static = document.getElementById(static_output_id);
    output_static.value = input_static.value;

    if (typeof growth_input_id !== 'undefined') {
        var input_growth = document.getElementById(growth_input_id);
        var output_growth = document.getElementById(growth_output_id)
        output_growth.value = input_growth.value;
    };

    var array_env_initial = new Array(max_T).fill(input_static.value);

    if (input_type == 'static') {
        var array_env = array_env_initial;
    } else if (input_type == 'linear') {
        var array_env = array_env_initial.map((value, index) => (Math.round((value * 1 + input_growth.value * index) * 100) / 100));

    } else if (input_type == 'exp') {
        var array_env = array_env_initial.map((value, index) => (Math.round((value * ((1 + 1 * input_growth.value) ** index) + Number.EPSILON) * 100) / 100));

    };
    return array_env;  
};





//price specific functions

//this function resets the price back to default by pressing the 'Reset' button
function reset_price_output_int_static(output_id_static, value_default_static, output_id_growth, value_default_growth) {
    var output_static = document.getElementById(output_id_static)
    output_static.innerHTML = value_default_static;
    if (typeof output_id_growth !== 'undefined') {
        var output_growth = document.getElementById(output_id_growth)
        output_growth.value = value_default_growth;
    }
};



// environment input specific functions

// this function updates the environment input chart visualization once a new array is created
function update_env_chart(chart, update_array_params_env) {
    var env_array = create_arrays.apply(this.id, update_array_params_env);
    console.log(env_array)
    if (chart.data.datasets.length > 1) {
        chart.data.datasets[0].data = env_array;
    }    
    chart.update();
};

// this function rests the environment input values back to default
function reset_input_values(max_T, input_type, chart,
    static_input_id, output_static_id, static_input_default_value,
    input_growth_id, output_growth_id, growth_input_default_value) {

    var input_static = document.getElementById(static_input_id);
    input_static.value = static_input_default_value;

    if (typeof input_growth_id !== 'undefined') {
        var input_growth = document.getElementById(input_growth_id);
        input_growth.value = growth_input_default_value;
    };

    display_output_int(static_input_id, output_static_id, input_growth_id, output_growth_id);

    var update_array_params = [max_T, input_type, static_input_id, output_static_id, input_growth_id, output_growth_id];

    update_env_chart(chart, update_array_params)
};


function reset_cost_input_values(max_T, array_id, input_type, chart,
    static_input_id, output_static_id, static_input_default_value,
    input_growth_id, output_growth_id, growth_input_default_value) {

    var input_static = document.getElementById(static_input_id);
    input_static.value = static_input_default_value;

    if (typeof input_growth_id !== 'undefined') {
        var input_growth = document.getElementById(input_growth_id);
        input_growth.value = growth_input_default_value;
    };

    display_output_int(static_input_id, output_static_id, input_growth_id, output_growth_id);

    var update_array_params = [max_T, input_type, static_input_id, output_static_id, input_growth_id, output_growth_id];

    update_cost_chart(chart, array_id, update_array_params)
};


// cost input specific functions

// this function updates the cost input chart visualization once a new array is created
function update_cost_chart(chart, array_id, update_array_params_cost) {
    var cost_array = create_arrays.apply(this.id, update_array_params_cost);
    
    chart.data.datasets[parseInt(array_id)].data = cost_array;
    chart.update();
};







