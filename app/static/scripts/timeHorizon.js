var start = 0;
var end = chart.data.labels.length;


function increaseTimeHorizon() {
    chart.data.labels.push(months[end]);
    chart.update();
    end++;
};

function reduceTimeHorizon() {
    chart.data.labels.pop(months[end]);
    chart.update();
    end--;
};

function shiftForwardTimeHorizon() {
    chart.data.labels.push(months[start + end]);
    chart.data.labels.shift();
    chart.data.datasets[0].data.shift();
    chart.data.datasets[1].data.shift();
    chart.update();
    start++;
    end++;
};

function shiftBackwardTimeHorizon() {
    var i = chart.data.labels.length;
    chart.data.labels.pop(months[start + end]);
    chart.data.labels.unshift();
    start--;
    end--;
    chart.data.datasets[0].data.unshift();
    chart.data.datasets[1].data.unshift();
    chart.update();
};