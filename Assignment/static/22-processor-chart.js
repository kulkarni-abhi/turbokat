function loadCpuChart() {
var chart = new CanvasJS.Chart("cpuChartContainer", {"animationEnabled": true, "exportEnabled": true, "axisY": {"title": "Percentage"}, "toolTip": {"shared": true}, "data": [], "legend": {"cursor": "pointer", "itemclick": "toggleDataSeries"}});

chart.render();

function toggleDataSeries(e) {
        if(typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
                e.dataSeries.visible = false;
        }
        else {
                e.dataSeries.visible = true;
        }
        chart.render();
}

}
