


function reset_price_output_int_static(output_id_static, value_default_static, output_id_growth, value_default_growth) {
    var output_static = document.getElementById(output_id_static)
    output_static.innerHTML = value_default_static;
};


function reset_env_input(T, input_type, chart_id, 
                        static_input_id, static_output_id, static_input_default_value, 
                        growth_input_id, growth_output_id, growth_input_default_value) {

    var input_static = document.getElementById(static_input_id)
    input_static.value = static_input_default_value;
    if (growth_input_id !== undefined) {
        var input_growth = document.getElementById(growth_input_id)
        input_growth.value = growth_input_default_value;
    }
    update_env(T, input_type, chart_id, static_input_id, static_output_id, static_input_default_value, growth_input_id, growth_output_id, growth_input_default_value);

};

function display_env(input_static_id, output_static_id, input_growth_id, output_growth_id) {
    var input_static = document.getElementById(input_static_id);
    var output_static = document.getElementById(output_static_id); 
    output_static.value = input_static.value;
    if (input_growth_id !== undefined) {
        var input_growth = document.getElementById(input_growth_id); 
        var output_growth = document.getElementById(output_growth_id);    
        output_growth.value = input_growth.value;
    }
};


function update_env(T, input_type, chart_id, 
                    static_input_id, static_output_id, static_input_default_value, 
                    growth_input_id, growth_output_id, growth_input_default_value) {

    var input_static = document.getElementById(static_input_id);
    var output_static = document.getElementById(static_output_id);
    output_static.value = input_static.value;
    if (growth_input_id !== undefined) {
        var input_growth = document.getElementById(growth_input_id);
        var output_growth = document.getElementById(growth_output_id)
        output_growth.value = input_growth.value;
    };
    var ctx = document.getElementById(chart_id).getContext('2d');

    var array_env_initial = new Array(T).fill(input_static.value);
    if (input_type == 'static') {
        var array_env_default = array_env_initial;
        var array_env_default = new Array(T).fill(static_input_default_value);
        console.log(array_env_default)
    } else if (input_type == 'linear') {
        var array_env = array_env_initial.map((value, index) => (Math.round((value * 1 + input_growth.value * index) * 100) / 100));
        var array_env_default = array_env_initial.map((value, index) => (Math.round((value * 1 + growth_input_default_value * index) * 100) / 100));

    } else if (input_type == 'exp') {
        var array_env = array_env_initial.map((value, index) => (Math.round((value * ((1 + 1* input_growth.value) ** index) + Number.EPSILON) * 100) / 100));
        var array_env_default = array_env_initial.map((value, index) => (Math.round((value * ((1 + 1 * growth_input_default_value) ** index) + Number.EPSILON) * 100) / 100));
        console.log(array_env_default)
        console.log(array_env)

    };   

    var chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: 'current value',
                borderColor: '#367DD9',
                data: array_env,
                fill:+1,
                pointRadius: 0
            }, {
                label: 'default value',
                borderColor: '#B8B6B4',
                borderDash: [5, 5],
                data: array_env_default,
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


    chart.update();
};



