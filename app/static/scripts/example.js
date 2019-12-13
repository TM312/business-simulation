
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

function clear_viewchange(change_id) {
    var change = document.getElementById(change_id);
    change.innerHTML = ""
};



function reset_price_output_int_static(output_id_static, value_default_static, output_id_growth, value_default_growth) {
    var output_static = document.getElementById(output_id_static)
    output_static.innerHTML = value_default_static;
    if (output_id_growth !== undefined) {
        var output_growth = document.getElementById(output_id_growth)
        output_growth.value = value_default_growth;
    }
};


function reset_env_input(T, input_type, chart_id, env_array_id_global,
                        static_input_id, static_output_id, static_input_default_value, 
                        growth_input_id, growth_output_id, growth_input_default_value) {

    var input_static = document.getElementById(static_input_id)
    input_static.value = static_input_default_value;
    if (growth_input_id !== undefined) {
        var input_growth = document.getElementById(growth_input_id)
        input_growth.value = growth_input_default_value;
    }
    update_env(T, input_type, chart_id, env_array_id_global, static_input_id, static_output_id, static_input_default_value, growth_input_id, growth_output_id, growth_input_default_value);

};

function display_output_int(input_static_id, output_static_id, input_growth_id, output_growth_id) {
    var input_static = document.getElementById(input_static_id);
    var output_static = document.getElementById(output_static_id); 
    output_static.value = input_static.value;
    if (input_growth_id !== undefined) {
        var input_growth = document.getElementById(input_growth_id); 
        var output_growth = document.getElementById(output_growth_id);    
        output_growth.value = input_growth.value;
    }
};

function create_env_chart(ctx_id, T, env_array, env_array_default) {
    var ctx = document.getElementById(ctx_id).getContext('2d');
    var chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: T,
                datasets: [{
                    label: 'current value',
                    borderColor: '#367DD9',
                    data: env_array,
                    fill: +1,
                    pointRadius: 0
                }, {
                    label: 'default value',
                    borderColor: '#B8B6B4',
                    borderDash: [5, 5],
                    data: env_array_default;,
                    fill: false,
                    pointRadius: 0
                }]
            },
            options: {
                legend: {
                    position: "bottom",
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            maxTicksLimit: 10,
                        }
                    }]
                }
            }
        });

};
    


function update_env(T, input_type, chart, env_array_id,
                    static_input_id, static_output_id, static_input_default_value, 
                    growth_input_id, growth_output_id, growth_input_default_value) {

 

    return env_array_id
};


function create_arrays(max_T, input_type, static_input_id, static_output_id, growth_input_id, growth_output_id) {

    var input_static = document.getElementById(static_input_id);
    var output_static = document.getElementById(static_output_id);
    output_static.value = input_static.value;

    if (growth_input_id !== undefined) {
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
}




