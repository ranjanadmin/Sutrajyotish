console.log("TRANSIT JS LOADED");
window.birthDateTime = null;
let transitTimer = null;
let transitStep = "day";
let transitDate = new Date();

function setTransitMode(mode) {
    transitStep = mode;
}

function startTransit() {

    if (transitTimer) return;

    transitTimer = setInterval(() => {
        stepForward();
    }, 1000);
}

function pauseTransit() {

    clearInterval(transitTimer);

    transitTimer = null;
}

function stepForward() {

    if (transitStep === "hour") {
        transitDate.setHours(transitDate.getHours() + 1);
    }

    else if (transitStep === "day") {
        transitDate.setDate(transitDate.getDate() + 1);
    }

    else if (transitStep === "week") {
        transitDate.setDate(transitDate.getDate() + 7);
    }

    else if (transitStep === "month") {
        transitDate.setMonth(transitDate.getMonth() + 1);
    }

    else if (transitStep === "year") {
        transitDate.setFullYear(transitDate.getFullYear() + 1);
    }

    loadTransitData();
}

function stepBackward() {

    if (transitStep === "hour") {
        transitDate.setHours(transitDate.getHours() - 1);
    }

    else if (transitStep === "day") {
        transitDate.setDate(transitDate.getDate() - 1);
    }

    else if (transitStep === "week") {
        transitDate.setDate(transitDate.getDate() - 7);
    }

    else if (transitStep === "month") {
        transitDate.setMonth(transitDate.getMonth() - 1);
    }

    else if (transitStep === "year") {
        transitDate.setFullYear(transitDate.getFullYear() - 1);
    }

    loadTransitData();
}

async function loadTransitData() {

    try {

        const lat =
            window.natalLat || 26.1482548;

        const lon =
            window.natalLon || 85.3316097;

        const timezone =
            document.getElementById("timezone")?.value
            || "Asia/Kolkata";

        const dt = transitDate
            .toISOString()
            .slice(0, 19)
            .replace("T", " ");

        const response = await fetch("/transit_api", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                datetime: dt,

                lat: parseFloat(lat),

                lon: parseFloat(lon),

                timezone: timezone
            })
        });

        let data = {};

        try {

            data = await response.json();

        } catch(e) {

            console.error(e);

            alert("Transit API invalid response.");

            return;
        }

        console.log("TRANSIT RESPONSE:", data);

        if (data.error) {

            alert(data.error);

            return;
        }

        renderTransitTable(data);

        updateTransitFooter(data);

        if (data.transit_chart) {

            drawTransitChart(
                data.transit_chart,
                data.natal_chart
            );
        }

    } catch(err) {

        console.error(err);

        alert("Transit engine error.");
    }
}

function renderTransitTable(data) {

    const transitBody =
        document.querySelector(
            "#transitTable tbody"
        );

    if (
        transitBody &&
        data.planets
    ) {

        transitBody.innerHTML = "";

        data.planets.forEach(p => {

            const row =
                document.createElement("tr");

            row.innerHTML = `
                <td>${p.planet}</td>
                <td>${p.sign}</td>
                <td>${p.sign_degree}</td>
                <td>-</td>
                <td>-</td>
                <td>${p.nak}</td>
                <td>${p.sub}</td>
            `;

            transitBody.appendChild(row);
        });
    }

    const natalBody =
        document.querySelector(
            "#natalTable tbody"
        );

    if (
        natalBody &&
        data.natal_table
    ) {

        natalBody.innerHTML = "";

        data.natal_table.forEach(p => {

            const row =
                document.createElement("tr");

            row.innerHTML = `
                <td>${p.planet}</td>
                <td>${p.sign}</td>
                <td>${p.sign_degree}</td>
                <td>-</td>
                <td>-</td>
                <td>${p.nak}</td>
                <td>${p.sub}</td>
            `;

            natalBody.appendChild(row);
        });
    }
}

function drawTransitChart(
    transitChart,
    natalChart
) {

    const shortNames = {

        "Sun": "Su",
        "Moon": "Mo",
        "Mars": "Ma",
        "Mercury": "Me",
        "Jupiter": "Ju",
        "Venus": "Ve",
        "Saturn": "Sa",
        "Rahu": "Ra",
        "Ketu": "Ke",

        "Uranus": "Ur",
        "Neptune": "Ne",
        "Pluto": "Pl"
    };

    const container =
        document.getElementById(
            "transitChart"
        );

    if (!container) return;

    container.style.position = "relative";

    container.innerHTML = `

    <div
        style="
            position:relative;
            width:920px;
            height:720px;
        "
    >

    <svg
        width="920"
        height="720"
        viewBox="0 0 920 720"
        style="
            position:absolute;
            left:0;
            top:0;
        "
    >

        <polygon
            points="
                460,20
                900,360
                460,700
                20,360
            "
            fill="none"
            stroke="blue"
            stroke-width="2"
        />

        <rect
            x="280"
            y="180"
            width="360"
            height="360"
            fill="none"
            stroke="blue"
            stroke-width="2"
        />

        <line x1="460" y1="20" x2="280" y2="180" stroke="blue"/>
        <line x1="460" y1="20" x2="640" y2="180" stroke="blue"/>
        <line x1="900" y1="360" x2="640" y2="180" stroke="blue"/>
        <line x1="900" y1="360" x2="640" y2="540" stroke="blue"/>
        <line x1="460" y1="700" x2="280" y2="540" stroke="blue"/>
        <line x1="460" y1="700" x2="640" y2="540" stroke="blue"/>
        <line x1="20" y1="360" x2="280" y2="180" stroke="blue"/>
        <line x1="20" y1="360" x2="280" y2="540" stroke="blue"/>

    </svg>

    </div>
    `;

    const chartLayer =
        container.querySelector("div");

    const positions = {

         1: [455, 65],
         2: [680, 120],
         3: [800, 285],
         4: [760, 470],
         5: [610, 630],
         6: [445, 680],
         7: [220, 630],
         8: [85, 470],
         9: [60, 285],
        10:[190,120],
        11:[390,250],
        12:[390,470]
    };

    Object.entries(positions).forEach(
        ([sign, pos]) => {

            const div =
                document.createElement("div");

            div.style.position = "absolute";

            div.style.left =
                pos[0] + "px";

            div.style.top =
                pos[1] + "px";

            div.style.fontSize = "14px";

            div.style.fontWeight = "bold";

            div.style.whiteSpace =
                "pre-line";

            div.style.textAlign =
                "center";

            let html =
                `<div style="
                    color:navy;
                    font-size:18px;
                ">
                    ${sign}
                </div>`;

            if (
                natalChart &&
                natalChart[sign]
            ) {

                natalChart[sign].forEach(p => {

                    if (
                        p.includes("Uranus") ||
                        p.includes("Neptune") ||
                        p.includes("Pluto")
                    ) {
                        return;
                    }

                    html += `
                    <div style="
                        color:#003cff;
                        font-size:14px;
                        font-weight:bold;
                        line-height:1.2;
                    ">
                        ${shortNames[p] || p}
                    </div>
                    `;
                });
            }

            if (
                transitChart &&
                transitChart[sign]
            ) {

                transitChart[sign].forEach(p => {

                    if (
                        p.includes("Uranus") ||
                        p.includes("Neptune") ||
                        p.includes("Pluto")
                    ) {
                        return;
                    }

                    html += `
                    <div style="
                        color:#d10000;
                        font-size:16px;
                        font-weight:bold;
                        margin-top:4px;
                        line-height:1.2;
                    ">
                        ${shortNames[p] || p}
                    </div>
                    `;
                });
            }

            div.innerHTML = html;

            chartLayer.appendChild(div);
        }
    );
}

function updateTransitFooter(data) {

    const dt =
        document.getElementById(
            "transitDateTime"
        );

    if (
        dt &&
        data.datetime
    ) {

        dt.innerHTML =
            data.datetime;
    }

    const dasa =
        document.getElementById(
            "runningDasa"
        );

    if (
        dasa &&
        data.running_dasa
    ) {

        dasa.innerHTML =
            "Vimsottari Dasa - " +
            data.running_dasa;
    }
}
function setTransitDate() {

    const day =
        prompt("Enter Day (DD)");

    if (!day) return;

    const month =
        prompt("Enter Month (MM)");

    if (!month) return;

    const year =
        prompt("Enter Year (YYYY)");

    if (!year) return;

    const hour =
        prompt("Enter Hour (0-23)", "0");

    const minute =
        prompt("Enter Minute", "0");

    const second =
        prompt("Enter Second", "0");

    transitDate = new Date(

        parseInt(year),

        parseInt(month) - 1,

        parseInt(day),

        parseInt(hour || 0),

        parseInt(minute || 0),

        parseInt(second || 0)
    );

    loadTransitData();
}
window.setTransitDate = function () {

    const day =
        prompt("Enter Day (DD)");

    if (!day) return;

    const month =
        prompt("Enter Month (MM)");

    if (!month) return;

    const year =
        prompt("Enter Year (YYYY)");

    if (!year) return;

    const hour =
        prompt("Enter Hour", "0");

    const minute =
        prompt("Enter Minute", "0");

    const second =
        prompt("Enter Second", "0");

    transitDate = new Date(

        parseInt(year),

        parseInt(month) - 1,

        parseInt(day),

        parseInt(hour || 0),

        parseInt(minute || 0),

        parseInt(second || 0)
    );

    console.log(
        "NEW TRANSIT DATE:",
        transitDate
    );

    loadTransitData();
};

// RECTIFICATION ENGINE (Workspace only)

window.adjustBirthTime = function(seconds) {

    if (!window.birthDateTime) {

        alert(
            "Generate natal chart first."
        );

        return;
    }

    window.birthDateTime = new Date(

        window.birthDateTime.getTime() +

        (seconds * 1000)
    );

    console.log(
        "RECTIFIED TIME:",
        window.birthDateTime
    );

    reloadRectifiedChart();
};

async function reloadRectifiedChart() {

    try {

        const lat =
            window.natalLat || 26.1482548;

        const lon =
            window.natalLon || 85.3316097;

        const dt =
            window.birthDateTime
            .toISOString()
            .slice(0, 19)
            .replace("T", " ");

        const response = await fetch(
            "/rectification_api",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    datetime: dt,

                    lat: lat,

                    lon: lon
                })
            }
        );

        const data =
            await response.json();

        console.log(
            "RECTIFICATION RESPONSE:",
            data
        );

        if (data.error) {

            alert(data.error);

            return;
        }

        renderTransitTable(data);

        updateTransitFooter(data);

        if (data.transit_chart) {

            drawTransitChart(
                data.transit_chart,
                data.natal_chart
            );
        }

    } catch(err) {

        console.error(err);

        alert(
            "Rectification update failed."
        );
    }
};
