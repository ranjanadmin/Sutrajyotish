function updateTransitDateDisplay(dtObj){

    const el =
        document.getElementById(
            "transitDateTime"
        );

    if(!el) return;

    const d =
        String(dtObj.getDate())
        .padStart(2,"0");

    const m =
        String(dtObj.getMonth()+1)
        .padStart(2,"0");

    const y =
        dtObj.getFullYear();

    const hh =
        String(dtObj.getHours())
        .padStart(2,"0");

    const mm =
        String(dtObj.getMinutes())
        .padStart(2,"0");

    const ss =
        String(dtObj.getSeconds())
        .padStart(2,"0");

    el.innerHTML =
        `${d}/${m}/${y} ${hh}:${mm}:${ss}`;
}

function drawTransitNorthChart(
    id,
    chartData
) {

    const container =
        document.getElementById(id);

    if (!container) return;

    container.innerHTML = `
    <div style="
        position:relative;
        width:760px;
        height:760px;
        margin:auto;
        background:#ffffff;
    ">

    <svg
        width="760"
        height="760"
        viewBox="0 0 760 760"
        style="position:absolute;left:0;top:0;z-index:1;"
    >

        <polygon
            points="380,30 700,380 380,730 60,380"
            fill="none"
            stroke="#0a46ff"
            stroke-width="4"
        />

        <rect
            x="245"
            y="245"
            width="270"
            height="270"
            fill="none"
            stroke="#0a46ff"
            stroke-width="4"
        />

        <line x1="380" y1="30" x2="245" y2="245" stroke="#0a46ff" stroke-width="3"/>
        <line x1="380" y1="30" x2="515" y2="245" stroke="#0a46ff" stroke-width="3"/>
        <line x1="700" y1="380" x2="515" y2="245" stroke="#0a46ff" stroke-width="3"/>
        <line x1="700" y1="380" x2="515" y2="515" stroke="#0a46ff" stroke-width="3"/>
        <line x1="380" y1="730" x2="245" y2="515" stroke="#0a46ff" stroke-width="3"/>
        <line x1="380" y1="730" x2="515" y2="515" stroke="#0a46ff" stroke-width="3"/>
        <line x1="60" y1="380" x2="245" y2="245" stroke="#0a46ff" stroke-width="3"/>
        <line x1="60" y1="380" x2="245" y2="515" stroke="#0a46ff" stroke-width="3"/>

    </svg>
    </div>
    `;

    const layer =
        container.firstElementChild;

    const positions = {
          1:[320,60],
          2:[500,140],
          3:[590,300],
          4:[540,500],
          5:[430,650],
          6:[300,700],
          7:[120,650],
          8:[20,500],
          9:[40,300],
         10:[120,140],
         11:[300,210],
         12:[300,470]
    };

    Object.entries(positions)
    .forEach(([sign,pos]) => {

        const planets =
            chartData[sign]
            || chartData[Number(sign)]
            || [];

        const div =
            document.createElement("div");

        div.style.position = "absolute";
        div.style.left = pos[0] + "px";
        div.style.top = pos[1] + "px";
        div.style.width = "120px";
        div.style.textAlign = "center";
        div.style.zIndex = "9999";

        div.innerHTML = `
            <div style="
                font-size:22px;
                font-weight:bold;
                color:#0a46ff;
                margin-bottom:6px;
            ">
                ${sign}
            </div>

            <div style="
                font-size:18px;
                font-weight:bold;
                color:#000000;
                line-height:1.3;
            ">
                ${planets.join("<br>")}
            </div>
        `;

        layer.appendChild(div);
    });
}



function drawTransitChart(
    transitChart,
    natalChart
) {

    const shortNames = {
        "Sun":"Su",
        "Moon":"Mo",
        "Mars":"Ma",
        "Mercury":"Me",
        "Jupiter":"Ju",
        "Venus":"Ve",
        "Saturn":"Sa",
        "Rahu":"Ra",
        "Ketu":"Ke"
    };

    const container =
        document.getElementById("transitChart");

    if (!container) return;

    container.innerHTML = "";

    const chartDiv = document.createElement("div");

    chartDiv.id = "transitChartInner";

    chartDiv.style.margin = "auto";

    chartDiv.style.width = "700px";

    chartDiv.style.height = "700px";

    container.appendChild(chartDiv);

    console.log(
        "TRANSIT CHART DATA:",
        transitChart
    );

    drawTransitNorthChart(
        "transitChartInner",
        transitChart || {}
    );

    window.NATAL_CHART_DATA =
        natalChart || {};
}
async function loadTransitData() {

    try {

        const wsResponse =
            await fetch("/workspace_data");

        const wsData =
            await wsResponse.json();

        console.log(
            "WORKSPACE:",
            wsData
        );

        const birthHeader =
            document.getElementById(
                "birthDetailsHeader"
            );

        if(birthHeader){

            const dob =
                wsData.birth_date
                || wsData.dob
                || "";

            const tob =
                wsData.birth_time
                || wsData.tob
                || "";

           
        }

        const lat =
            wsData.latitude;

        const lon =
            wsData.longitude;

        if (!lat || !lon) {

            alert(
                "No latitude/longitude found"
            );

            return;
        }

        const now = new Date();

        const dt =
            now.getFullYear()
            + "-"
            + String(
                now.getMonth() + 1
            ).padStart(2,"0")
            + "-"
            + String(
                now.getDate()
            ).padStart(2,"0")
            + " "
            + String(
                now.getHours()
            ).padStart(2,"0")
            + ":"
            + String(
                now.getMinutes()
            ).padStart(2,"0")
            + ":"
            + String(
                now.getSeconds()
            ).padStart(2,"0");

        const response =
            await fetch(
                "/transit_api",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        lat: lat,

                        lon: lon,

                        timezone:
                            "Asia/Kolkata",

                        datetime: dt
                    })
                }
            );

        const result =
            await response.json();

        console.log(
            "TRANSIT RESULT:",
            result
        );

        drawTransitChart(

            result.transit_chart || {},

            result.natal_chart || {}
        );

        renderTransitTable(
            result.transit_table || []
        );

        renderNatalTable(
            result.natal_table || []
        );
   
        setTimeout(() => {

            renderTransitDasa(
                result.running_dasa
                || result.current_dasa
                || result.dasa
                || ""
            );

        }, 50);


    } catch(err) {

        console.error(
            "TRANSIT ERROR:",
            err
        );
    }
}


window.loadTransitData = loadTransitData;



function renderTransitTable(rows) {

    const table =
        document.getElementById(
            "transitTable"
        );

    if (!table) return;

    let html = `
    <table class="table table-bordered">
        <thead>
            <tr>
                <th>Planet</th>
                <th>Sign</th>
                <th>Degree</th>
                <th>Lord</th>
                <th>STL</th>
                <th>SL</th>
                <th>SSL</th>
            </tr>
        </thead>
        <tbody>
    `;

    rows.forEach(row => {

        html += `
        <tr>
            <td>${row.planet || ""}</td>
            <td>${row.sign || ""}</td>
            <td>${row.sign_degree || row.degree || ""}</td>
            <td>${row.lord || ""}</td>
            <td>${row.stl || ""}</td>
            <td>${row.sl || ""}</td>
            <td>${row.ssl || ""}</td>
        </tr>
        `;
    });

    html += `
        </tbody>
    </table>
    `;

    table.innerHTML = html;
}



function renderNatalTable(rows) {

    const table =
        document.getElementById(
            "natalTable"
        );

    if (!table) return;

    let html = `
    <table class="table table-bordered">
        <thead>
            <tr>
                <th>Planet</th>
                <th>Sign</th>
                <th>Degree</th>
                <th>Nak</th>
                <th>Sub</th>
            </tr>
        </thead>
        <tbody>
    `;

    rows.forEach(row => {

        html += `
        <tr>
            <td>${row.planet || ""}</td>
            <td>${row.sign || ""}</td>
            <td>${row.sign_degree || row.degree || ""}</td>
            <td>${row.nak || ""}</td>
            <td>${row.sub || ""}</td>
        </tr>
        `;
    });

    html += `
        </tbody>
    </table>
    `;

    table.innerHTML = html;
}




/* =========================
   TRANSIT PLAYBACK ENGINE
========================= */

let TRANSIT_INTERVAL = null;

let TRANSIT_SPEED = 1000;

let TRANSIT_DIRECTION = 1;

let TRANSIT_MODE = "hour";

let CURRENT_TRANSIT_DATE = new Date();

async function loadTransitDataFromDate(dtObj) {

    try {

        const wsResponse =
            await fetch("/workspace_data");

        const wsData =
            await wsResponse.json();
        updateTransitDateDisplay(
           dtObj
        );
        const birthHeader =
            document.getElementById(
                 "birthDetailsHeader"
           );

      if(birthHeader){

        const dob =
           wsData.birth_date
           || wsData.dob
           || "";

       const tob =
          wsData.birth_time
         || wsData.tob
         || "";

      const pob =
         wsData.city
        || wsData.birth_city
        || wsData.place_name
        || wsData.location
        || "";

    birthHeader.innerHTML =

        "DOB : " + dob
        + " | TOB : " + tob
        + " | POB : " + pob;
}

        const lat = wsData.latitude;

        const lon = wsData.longitude;

        const dt =
            dtObj.getFullYear()
            + "-"
            + String(
                dtObj.getMonth() + 1
            ).padStart(2,"0")
            + "-"
            + String(
                dtObj.getDate()
            ).padStart(2,"0")
            + " "
            + String(
                dtObj.getHours()
            ).padStart(2,"0")
            + ":"
            + String(
                dtObj.getMinutes()
            ).padStart(2,"0")
            + ":"
            + String(
                dtObj.getSeconds()
            ).padStart(2,"0");

        const response =
            await fetch(
                "/transit_api",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        lat: lat,

                        lon: lon,

                        timezone:
                            "Asia/Kolkata",

                        datetime: dt
                    })
                }
            );

        const result =
            await response.json();
        console.log(
          "PLAYBACK DATE:",
           dtObj
        );

        console.log(
          "PLAYBACK DASA:",
        result.running_dasa
       );

        drawTransitChart(
            result.transit_chart || {},
            result.natal_chart || {}
        );

        renderTransitTable(
            result.transit_table || []
        );

        renderNatalTable(
            result.natal_table || []
        );

        renderTransitDasa(
            result.running_dasa
            || result.current_dasa
            || result.dasa
            || ""
        );

    } catch(err) {

        console.error(
            "TRANSIT PLAYBACK ERROR:",
            err
        );
    }
}

function advanceTransit() {

    if (TRANSIT_MODE === "minute") {

        CURRENT_TRANSIT_DATE.setMinutes(
            CURRENT_TRANSIT_DATE.getMinutes()
            + TRANSIT_DIRECTION
        );
    }

    else if (TRANSIT_MODE === "hour") {

        CURRENT_TRANSIT_DATE.setHours(
            CURRENT_TRANSIT_DATE.getHours()
            + TRANSIT_DIRECTION
        );
    }

    else if (TRANSIT_MODE === "day") {

        CURRENT_TRANSIT_DATE.setDate(
            CURRENT_TRANSIT_DATE.getDate()
            + TRANSIT_DIRECTION
        );
    }

    else if (TRANSIT_MODE === "week") {

        CURRENT_TRANSIT_DATE.setDate(
            CURRENT_TRANSIT_DATE.getDate()
            + (7 * TRANSIT_DIRECTION)
        );
    }

    else if (TRANSIT_MODE === "month") {

        CURRENT_TRANSIT_DATE.setMonth(
            CURRENT_TRANSIT_DATE.getMonth()
            + TRANSIT_DIRECTION
        );
    }

    else if (TRANSIT_MODE === "year") {

        CURRENT_TRANSIT_DATE.setFullYear(
            CURRENT_TRANSIT_DATE.getFullYear()
            + TRANSIT_DIRECTION
        );
    }

    loadTransitDataFromDate(
        CURRENT_TRANSIT_DATE
    );
}

function initTransitControls() {

    const bind = (id, fn) => {

        const el =
            document.getElementById(id);

        if (el) {
            el.onclick = fn;
        }
    };

    bind("btnStart", () => {

        clearInterval(
            TRANSIT_INTERVAL
        );

        TRANSIT_INTERVAL =
            setInterval(
                advanceTransit,
                TRANSIT_SPEED
            );
    });

    bind("btnPause", () => {

        clearInterval(
            TRANSIT_INTERVAL
        );
    });

    bind("btnReplay", () => {

        CURRENT_TRANSIT_DATE =
            new Date();

        loadTransitDataFromDate(
            CURRENT_TRANSIT_DATE
        );
    });

    bind("btnForward", () => {

        TRANSIT_DIRECTION = 1;

        advanceTransit();
    });

    bind("btnBackward", () => {

        TRANSIT_DIRECTION = -1;

        advanceTransit();
    });

    bind("btnFast", () => {

        TRANSIT_SPEED = 250;
    });

    bind("btnSlow", () => {

        TRANSIT_SPEED = 2000;
    });

    bind("btnHourly", () => {

        TRANSIT_MODE = "hour";
    });

    bind("btnDaily", () => {

        TRANSIT_MODE = "day";
    });

    bind("btnWeekly", () => {

        TRANSIT_MODE = "week";
    });

    bind("btnMonthly", () => {

        TRANSIT_MODE = "month";
    });

    bind("btnYearly", () => {

        TRANSIT_MODE = "year";
    });

    bind("btnRealTime", () => {

        CURRENT_TRANSIT_DATE =
            new Date();

        loadTransitDataFromDate(
            CURRENT_TRANSIT_DATE
        );
    });
}

window.addEventListener(
    "DOMContentLoaded",
    initTransitControls
);





/* =========================
   TRANSIT BUTTON ACTIVATION FIX
========================= */

function bindTransitButton(label, fn) {

    const buttons =
        document.querySelectorAll("button");

    buttons.forEach(btn => {

        const txt =
            btn.innerText
               .trim()
               .toLowerCase();

        if (
            txt === label.toLowerCase()
        ) {

            btn.onclick = fn;
        }
    });
}

function initTransitButtonsRobust() {

    bindTransitButton(
        "Start",
        () => {

            clearInterval(
                TRANSIT_INTERVAL
            );

            TRANSIT_INTERVAL =
                setInterval(
                    advanceTransit,
                    TRANSIT_SPEED
                );
        }
    );

    bindTransitButton(
        "Pause",
        () => {

            clearInterval(
                TRANSIT_INTERVAL
            );
        }
    );

    bindTransitButton(
        "Forward",
        () => {

            TRANSIT_DIRECTION = 1;

            advanceTransit();
        }
    );

    bindTransitButton(
        "Backward",
        () => {

            TRANSIT_DIRECTION = -1;

            advanceTransit();
        }
    );

    bindTransitButton(
        "Fast",
        () => {

            TRANSIT_SPEED = 200;
        }
    );

    bindTransitButton(
        "Slow",
        () => {

            TRANSIT_SPEED = 2000;
        }
    );

    bindTransitButton(
        "Replay",
        () => {

            CURRENT_TRANSIT_DATE =
                new Date();

            loadTransitDataFromDate(
                CURRENT_TRANSIT_DATE
            );
        }
    );

    bindTransitButton(
        "Real Time",
        () => {

            CURRENT_TRANSIT_DATE =
                new Date();

            loadTransitDataFromDate(
                CURRENT_TRANSIT_DATE
            );
        }
    );

    bindTransitButton(
        "Hourly",
        () => {

            TRANSIT_MODE = "hour";
        }
    );

    bindTransitButton(
        "Daily",
        () => {

            TRANSIT_MODE = "day";
        }
    );

    bindTransitButton(
        "Weekly",
        () => {

            TRANSIT_MODE = "week";
        }
    );

    bindTransitButton(
        "Monthly",
        () => {

            TRANSIT_MODE = "month";
        }
    );

    bindTransitButton(
        "Yearly",
        () => {

            TRANSIT_MODE = "year";
        }
    );

    bindTransitButton(
        "Reverse",
        () => {

            TRANSIT_DIRECTION = -1;
        }
    );

    bindTransitButton(
        "End",
        () => {

            clearInterval(
                TRANSIT_INTERVAL
            );
        }
    );

    const setDateFn = async () => {

        const val =
            prompt(
                "Enter Date Time\nYYYY-MM-DD HH:MM:SS",
                "2026-05-25 12:00:00"
            );

        if (!val) return;

        const dt =
            new Date(
                val.replace(
                    " ",
                    "T"
                )
            );

        if (
            isNaN(
                dt.getTime()
            )
        ) {

            alert(
                "Invalid Date"
            );

            return;
        }

        CURRENT_TRANSIT_DATE = dt;

        await loadTransitDataFromDate(
            CURRENT_TRANSIT_DATE
        );
    };

    bindTransitButton(
        "Set Date",
        setDateFn
    );

    bindTransitButton(
        "SetDate",
        setDateFn
    );
}

window.addEventListener(
    "load",
    () => {

        setTimeout(
            initTransitButtonsRobust,
            500
        );
    }
);



/* =========================
   VIMSHOTTARI DASA NAVIGATION
========================= */

function renderTransitDasa(data) {

    const transitChart =
        document.getElementById(
            "transitChart"
        );

    if (!transitChart) {

        console.log(
            "NO transitChart FOUND"
        );

        return;
    }

    let el =
        document.getElementById(
            "transitDasaStatus"
        );

    if (!el) {

        el =
            document.createElement("div");

        el.id =
            "transitDasaStatus";

        transitChart.parentNode.insertBefore(
            el,
            transitChart
        );
    }

    let text = "";

    if (typeof data === "string") {

        text = data;
    }

    else if (
        typeof data === "object"
        && data !== null
    ) {

        text = [
            data.maha,
            data.antar,
            data.pratyantar,
            data.sukshma,
            data.prana
        ]
        .filter(Boolean)
        .join(" ");
    }

    el.style.display = "block";
    el.style.width = "100%";
    el.style.textAlign = "center";
    el.style.margin = "10px 0";
    el.style.padding = "10px";
    el.style.background = "#f4f7ff";
    el.style.border = "2px solid #0a46ff";
    el.style.borderRadius = "10px";
    el.style.fontSize = "22px";
    el.style.fontWeight = "bold";
    el.style.color = "#0a2c8f";

    el.innerHTML = `
        Vimshottari Dasa :
        ${text || "Loading..."}
    `;

    console.log(
        "RUNNING DASA DISPLAY:",
        text
    );
}

function nextDasaStep() {

    TRANSIT_DIRECTION = 1;

    advanceTransit();
}

function prevDasaStep() {

    TRANSIT_DIRECTION = -1;

    advanceTransit();
}

function bindDasaButtons() {

    const backBtn =
        document.getElementById(
            "btnDasaBack"
        );

    const nextBtn =
        document.getElementById(
            "btnDasaNext"
        );

    if (backBtn) {

        backBtn.onclick =
            prevDasaStep;
    }

    if (nextBtn) {

        nextBtn.onclick =
            nextDasaStep;
    }
}

window.addEventListener(
    "load",
    () => {

        setTimeout(
            bindDasaButtons,
            500
        );
    }
);



/* =========================
   TRANSIT FOOTER CONTROLS
========================= */

window.addEventListener(
    "DOMContentLoaded",
    () => {

        updateTransitDateDisplay(
            new Date()
        );

        const stepForward =
            document.getElementById(
                "btnStepForward"
            );

        const stepBack =
            document.getElementById(
                "btnStepBack"
            );

        if(stepForward){

            stepForward.onclick = () => {

                TRANSIT_DIRECTION = 1;

                advanceTransit();
            };
        }

        if(stepBack){

            stepBack.onclick = () => {

                TRANSIT_DIRECTION = -1;

                advanceTransit();
            };
        }
    }
);
