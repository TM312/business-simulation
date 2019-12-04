var T = 7
let rangeStaticArray = new Array(T);
var dataOld = [];
var dataNew = [];
var value = environment_input    { environment_input.id } }_disp.value

function rangeToArrayStatic() {
    dataOld = dataNew;
    environment_input{ { environment_input.id } }_disp.value = environment_input{{ environment_input.id }}.value;
    rangeStaticArray.fill(environment_input{{ environment_input.id }}.value);
    rangeArrayStaticOutput.value = rangeStaticArray;
    dataNew = rangeStaticArray;
    updateChart();
};

function rangeToArrayLinear() {
    dataOld = dataNew;
    rangeOutput.value = rangeInput.value;
    rangeStaticArray.fill(rangeInput.value);
    let rangeLinearArray = rangeStaticArray.map((value, index) => (Math.round((value * (1 + index * rangeGrowthFactorLinear.value) + Number.EPSILON) * 100) / 100));
    rangeArrayLinearOutput.value = rangeLinearArray;
    dataNew = rangeLinearArray;
    updateChart();
};

function rangeToArrayDynamic() {
    dataOld = dataNew;
    rangeOutput.value = rangeInput.value;
    rangeStaticArray.fill(rangeInput.value);
    let rangeDynamicArray = rangeStaticArray.map((value, index) => (Math.round((value * (1 + index ** rangeGrowthFactorDynamic.value) + Number.EPSILON) * 100) / 100));
    rangeArrayDynamicOutput.value = rangeDynamicArray;
    dataNew = rangeDynamicArray;
    updateChart();
};


var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];

var ctx = document.getElementById('environment_input{ { environment_input.id } }').getContext('2d');

var chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['January', 'February', 'March'],
        datasets: [{
            label: false,
            borderColor: 'rgb(0, 99, 132)',
            data: dataNew
        }, {
            borderColor: 'rgb(12, 44, 240)',
            data: dataOld,
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




