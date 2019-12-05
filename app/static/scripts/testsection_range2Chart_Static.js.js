// var dataOld = [];
// var dataNew = [];
var T = 7
var array_static_new = new Array(T).fill(0);
var array_static_old = new Array(T).fill(0);
var array_linear_new = new Array(T).fill(0);
var array_linear_old = new Array(T).fill(0);
var array_exp_new = new Array(T).fill(0);
var array_exp_old = new Array(T).fill(0);

// console.log(array_static_new)
// console.log(array_static_old)

var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];


function update() {
    output_int_static.value = input_static.value;
    output_int_growth.value = input_growth.value;
    rangeToChart();
}


function rangeToChart() {

    var ctxStatic = document.getElementById('chartStatic').getContext('2d');
    var ctxLinear = document.getElementById('chartLinear').getContext('2d');
    var ctxExp = document.getElementById('chartExp').getContext('2d');

    array_static_old = array_static_new
    array_linear_old = array_linear_new
    array_exp_old = [1,2,3,4,5,6,7];

    array_static_new = new Array(T).fill(input_static.value);
    array_linear_new = array_static_new.map((value, index) => (Math.round((value * 1 + input_growth.value * index) * 100) / 100));
    array_exp_new = array_static_new.map((value, index) => (Math.round((value * input_growth.value ** index + Number.EPSILON) * 100) / 100));

    var chartStatic = new Chart(ctxStatic, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: false,
                borderColor: 'rgb(0, 99, 132)',
                data: array_static_new    
            }, {
                borderColor: 'rgb(44, 22, 11)',
                data: array_static_old
            }]
        },
        options: {
            legend: {
                position: "bottom",
            },
            scales: {
                yAxes: [{
                    ticks: {
                        callback: function (value, index, values) {
                            return '$' + value;
                        }
                    }
                }]
            }
        }
    });
    var chartLinear = new Chart(ctxLinear, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: false,
                borderColor: 'rgb(0, 99, 132)',
                data: array_linear_new
            }, {
                    borderColor: 'rgb(44, 22, 11)',
                    data: array_linear_old
                }]
        },
        options: {
            legend: {
                position: "bottom",
            },
            scales: {
                yAxes: [{
                    ticks: {
                        callback: function (value, index, values) {
                            return '$' + value;
                        }
                    }
                }]
            }
        }
    });
    var chartExp = new Chart(ctxExp, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: false,
                borderColor: 'rgb(0, 99, 132)',
                data: array_exp_new
            }, {
                    borderColor: 'rgb(44, 22, 11)',
                    data: array_exp_old
                }]
        },
        options: {
            legend: {
                position: "bottom",
            },
            scales: {
                yAxes: [{
                    ticks: {
                        callback: function (value, index, values) {
                            return '$' + value;
                        }
                    }
                }]
            }
        }
    });

    chartStatic.update();
    chartLinear.update();
    chartExp.update();
}

