
console.log("WORKSPACE JS LOADED");

document.addEventListener(
    "DOMContentLoaded",
    async function () {

        await loadWorkspace();
    }
);

async function loadWorkspace() {

    try {

        const response =
            await fetch("/workspace_data");

        const data =
            await response.json();

        console.log(
            "WORKSPACE DATA:",
            data
        );

        renderWorkspace(data);

    } catch(err) {

        console.error(err);

        alert(
            "Workspace load failed."
        );
    }
}

function renderWorkspace(data) {

    renderCharts(data);

    renderDasa(data);

    renderBirthDetails(data);

    renderRulingPlanets(data);

    renderSutraGrid(data);
}

function renderCharts(data) {

    drawWorkspaceChart(
        "lagnaChart",
        data.natal_chart || []
    );

    drawWorkspaceChart(
        "bhavChart",
        data.bhav_chart || {}
    );
}

function renderNorthChart(id, chartData) {

    const container =
        document.getElementById(id);

    if (!container) return;

    let html = `
        <div class="chart-container">
    `;

    // LAGNA STYLE ARRAY
    if (Array.isArray(chartData)) {

        chartData.forEach(row => {

            row.forEach(cell => {

                html += `
                    <div class="box">
                        ${String(cell).replace(/\n/g, "<br>")}
                    </div>
                `;
            });

        });
    }

    // BHAV STYLE OBJECT
    else {

        const order = [
            12,1,2,3,
            11,"","",4,
            10,"","",5,
            9,8,7,6
        ];

        order.forEach(h => {

            if (h === "") {

                html += `
                    <div class="box"></div>
                `;

            } else {

                const planets =
                    chartData[h] || [];

                html += `
                    <div class="box">
                        <b>${h}</b><br>
                        ${planets.join("<br>")}
                    </div>
                `;
            }
        });
    }

    html += `</div>`;

    container.innerHTML = html;
}

function renderDasa(data) {

    const box =
        document.getElementById(
            "dasaNavigator"
        );

    if (!box) return;

    box.innerHTML = `
        <div style="
            padding:10px;
            font-weight:bold;
            color:#000066;
            font-size:18px;
        ">
            ${data.running_dasa || ""}
        </div>
    `;
}

function renderBirthDetails(data) {

    document.getElementById(
        "dobValue"
    ).innerHTML =
        data.birth_datetime || "";

    document.getElementById(
        "latValue"
    ).innerHTML =
        data.latitude || "";

    document.getElementById(
        "lonValue"
    ).innerHTML =
        data.longitude || "";

    document.getElementById(
        "siderealValue"
    ).innerHTML =
        data.sidereal_time || "";

    window.birthDateTime =
        new Date(
            data.birth_datetime
        );
}

function renderRulingPlanets(data) {

    const container =
        document.getElementById(
            "rulingPlanets"
        );

    if (!container) return;

    container.innerHTML = `

        <div class="rp-grid">

            <div class="rp-label">
                Asc LRD/STL/SL
            </div>

            <div class="rp-value">
                ${data.asc_ruling || ""}
            </div>

            <div class="rp-label">
                Mon LRD/STL/SL
            </div>

            <div class="rp-value">
                ${data.moon_ruling || ""}
            </div>

            <div class="rp-label">
                Day Lord
            </div>

            <div class="rp-value">
                ${data.day_lord || ""}
            </div>

        </div>
    `;
}

function renderSutraGrid(data) {

    const tbody =
        document.getElementById(
            "sutraGridBody"
        );

    if (!tbody) return;

    tbody.innerHTML = "";

    const rows =
        data.kp_grid || [];

    rows.forEach(r => {

        tbody.innerHTML += `

        <tr>

            <td>${r.planet || ""}</td>

            <td>${r.planet_houses || ""}</td>

            <td>${r.star_lord || ""}</td>

            <td>${r.star_houses || ""}</td>

            <td>${r.sub_lord || ""}</td>

            <td>${r.sub_houses || ""}</td>

        </tr>
        `;
    });
}


function drawWorkspaceChart(id, chartData) {

    const container =
        document.getElementById(id);

    if (!container) return;

    container.style.position = "relative";

    container.innerHTML = `

    <div
        style="
            position:relative;
            width:520px;
            height:520px;
        "
    >

    <svg
        width="520"
        height="520"
        viewBox="0 0 520 520"
        style="
            position:absolute;
            left:0;
            top:0;
        "
    >

        <polygon
            points="
                260,20
                500,260
                260,500
                20,260
            "
            fill="none"
            stroke="blue"
            stroke-width="2"
        />

        <rect
            x="160"
            y="160"
            width="200"
            height="200"
            fill="none"
            stroke="blue"
            stroke-width="2"
        />

        <line x1="260" y1="20" x2="160" y2="160" stroke="blue"/>
        <line x1="260" y1="20" x2="360" y2="160" stroke="blue"/>
        <line x1="500" y1="260" x2="360" y2="160" stroke="blue"/>
        <line x1="500" y1="260" x2="360" y2="360" stroke="blue"/>
        <line x1="260" y1="500" x2="160" y2="360" stroke="blue"/>
        <line x1="260" y1="500" x2="360" y2="360" stroke="blue"/>
        <line x1="20" y1="260" x2="160" y2="160" stroke="blue"/>
        <line x1="20" y1="260" x2="160" y2="360" stroke="blue"/>

    </svg>

    </div>
    `;

    const layer = container.querySelector("div");

    const positions = {

         1: [245, 35],
         2: [375, 75],
         3: [445, 200],
         4: [400, 330],
         5: [320, 455],
         6: [245, 475],
         7: [110, 455],
         8: [35, 330],
         9: [25, 200],
        10:[95,75],
        11:[210,170],
        12:[210,330]
    };

    if (Array.isArray(chartData)) {

        let sign = 1;

        chartData.flat().forEach(cell => {

            const pos = positions[sign];

            if (!pos) return;

            const div = document.createElement("div");

            div.style.position = "absolute";
            div.style.left = pos[0] + "px";
            div.style.top = pos[1] + "px";
            div.style.fontSize = "14px";
            div.style.fontWeight = "bold";
            div.style.whiteSpace = "pre-line";

            div.innerHTML =
                String(cell).replace(/\n/g,"<br>");

            layer.appendChild(div);

            sign++;
        });

    } else {

        Object.entries(positions).forEach(([h,pos]) => {

            const div = document.createElement("div");

            div.style.position = "absolute";
            div.style.left = pos[0] + "px";
            div.style.top = pos[1] + "px";
            div.style.fontSize = "14px";
            div.style.fontWeight = "bold";
            div.style.whiteSpace = "pre-line";

            const planets =
                chartData[h] || [];

            div.innerHTML =
                "<b>" + h + "</b><br>" +
                planets.join("<br>");

            layer.appendChild(div);
        });
    }
}

window.adjustBirthTime = function(
    unit,
    direction
) {

    let seconds = 0;

    if (unit === "day") {
        seconds = 86400;
    }

    else if (unit === "hour") {
        seconds = 3600;
    }

    else if (unit === "minute10") {
        seconds = 600;
    }

    else if (unit === "minute1") {
        seconds = 60;
    }

    seconds =
        seconds * direction;

    if (!window.birthDateTime) {

        alert("Generate chart first.");

        return;
    }

    window.birthDateTime =
        new Date(

            window.birthDateTime.getTime()

            +

            (seconds * 1000)
        );

    alert(
        "Updated Birth Time: " +
        window.birthDateTime
    );
};
