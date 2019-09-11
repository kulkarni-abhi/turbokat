function loadCpuChart() {
var chart = new CanvasJS.Chart("cpuChartContainer", JSON_DATA);

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
