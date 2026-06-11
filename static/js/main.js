document.getElementById("form").addEventListener("submit", async function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    let res = await fetch("/generate", {
        method: "POST",
        body: formData
    });

    let data = await res.json();

    console.log("FULL RESPONSE:", data); // DEBUG

    renderChart(data.ui_lagna, "lagnaChartUI");
    renderChart(data.ui_bhav, "bhavChartUI");

    renderKPGrid(data.kp_grid);
    renderSutraGrid(data.sutra_grid);
});


// ===============================
// CHART RENDER
// ===============================
function renderChart(chart, elementId) {
    let html = "<table border='1'>";

    for (let h in chart) {
        html += `<tr><td>House ${h}</td><td>${chart[h].join(", ")}</td></tr>`;
    }

    html += "</table>";
    document.getElementById(elementId).innerHTML = html;
}


// ===============================
// KP GRID
// ===============================
function renderKPGrid(kp) {
    let html = "<table border='1'>";
    html += "<tr><th>Planet</th><th>House</th><th>Sign</th><th>Star</th><th>Sub</th></tr>";

    for (let p in kp) {
        let d = kp[p];
        html += `<tr>
            <td>${p}</td>
            <td>${d.house}</td>
            <td>${d.sign}</td>
            <td>${d.star_lord}</td>
            <td>${d.sub_lord}</td>
        </tr>`;
    }

    html += "</table>";
    document.getElementById("kpGrid").innerHTML = html;
}


// ===============================
// SUTRA GRID
// ===============================
function renderSutraGrid(sutra) {
    let html = "<table border='1'>";
    html += "<tr><th>Planet</th><th>House</th><th>Sign Lord</th><th>Star Lord</th><th>Sub Lord</th></tr>";

    for (let p in sutra) {
        let d = sutra[p];
        html += `<tr>
            <td>${p}</td>
            <td>${d[0]}</td>
            <td>${d[1]}</td>
            <td>${d[2]}</td>
            <td>${d[3]}</td>
        </tr>`;
    }

    html += "</table>";
    document.getElementById("sutraGrid").innerHTML = html;
}