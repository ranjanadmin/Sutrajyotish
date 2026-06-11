
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
        data.lagna_chart_workspace || {}
    );

    drawWorkspaceChart(
        "bhavChart",
        data.bhav_chart || {}
    );
}

function renderDasa(data) {

    const box =
        document.getElementById(
            "dasaNavigator"
        );

    if (!box) return;

    let dasaText = "";

    if (data.current_dasa) {

        dasaText =
            `${data.current_dasa.maha || ""} / ` +
            `${data.current_dasa.antar || ""} / ` +
            `${data.current_dasa.pratyantar || ""}`;
    }

    box.innerHTML = `
        <div style="
            padding:10px;
            font-weight:bold;
            color:#000066;
            font-size:18px;
        ">
            ${dasaText}
        </div>
    `;
}

function renderBirthDetails(data) {

    const dob = document.getElementById("dobValue");
    const lat = document.getElementById("latValue");
    const lon = document.getElementById("lonValue");
    const sid = document.getElementById("siderealValue");

    if (dob) dob.innerHTML = data.birth_datetime || "";
    if (lat) lat.innerHTML = data.latitude || "";
    if (lon) lon.innerHTML = data.longitude || "";
    if (sid) sid.innerHTML = data.sidereal_time || "";

    if (data.birth_datetime) {

        window.birthDateTime =
            new Date(
                data.birth_datetime
            );
    }
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
                Asc Lord
            </div>

            <div class="rp-value">
                ${data.asc_ruling || ""}
            </div>

            <div class="rp-label">
                Moon Star Lord
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

        <tr class="sutra-row-head">

            <td class="sutra-label">Planet</td>

            <td><b>${r.planet || ""}</b></td>

            <td>${r.planet_houses || ""}</td>

            <td><b>${r.star_lord || ""}</b></td>

            <td>${r.star_houses || ""}</td>

            <td><b>${r.sub_lord || ""}</b></td>

            <td>${r.sub_houses || ""}</td>

        </tr>

        <tr>

            <td class="sutra-label">Star Lord</td>

            <td><b>${r.star_lord || ""}</b></td>

            <td>${r.star_houses || ""}</td>

            <td colspan="4">&nbsp;</td>

        </tr>

        <tr class="sutra-bottom-row">

            <td class="sutra-label">Sub Lord</td>

            <td><b>${r.sub_lord || ""}</b></td>

            <td>${r.sub_houses || ""}</td>

            <td colspan="4">&nbsp;</td>

        </tr>
        `;
    });
}


function drawWorkspaceChart(id, chartData) {

    const container = document.getElementById(id);

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

    const layer = container.firstElementChild || container;

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

    function renderBox(sign, planetsHtml) {

        if (!positions[sign]) {
            return;
        }

        const pos = positions[sign];

        const box = document.createElement("div");

        box.style.position = "absolute";
        box.style.zIndex = "999";
        box.style.pointerEvents = "none";
        box.style.left = pos[0] + "px";
        box.style.top = pos[1] + "px";
        box.style.width = "120px";
        box.style.minHeight = "60px";
        box.style.overflow = "visible";
        box.style.padding = "4px";
        box.style.textAlign = "center";
        box.style.fontFamily = "Arial";
        box.style.background = "rgba(255,255,255,0.01)";

        const signDiv = document.createElement("div");

       signDiv.style.fontSize = "22px";
       signDiv.style.fontWeight = "bold";
       signDiv.style.marginBottom = "6px";
       signDiv.style.color = "#0a46ff";
       signDiv.innerText = sign;

       const planetDiv = document.createElement("div");

       planetDiv.style.fontSize = "18px";
       planetDiv.style.lineHeight = "1.3";
       planetDiv.style.fontWeight = "bold";
       planetDiv.style.color = "#000000";
       planetDiv.style.display = "block";
       planetDiv.style.visibility = "visible"; 
       planetDiv.style.position = "relative";
       planetDiv.style.zIndex = "9999";
       planetDiv.innerHTML = planetsHtml || "&nbsp;";

       box.appendChild(signDiv);
       box.appendChild(planetDiv);

        layer.appendChild(box);
    }

    // SAME FORMAT FOR LAGNA + BHAV
    Object.entries(positions).forEach(([sign, pos]) => {

      const planets =
         chartData[sign]
         || chartData[String(sign)]
         || [];

     renderBox(
        Number(sign),
        planets.join("<br>")
    );
   });
 }


window.adjustBirthTime = async function(
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

    seconds = seconds * direction;

    const dobElement =
        document.getElementById(
            "dobValue"
        );

    if (!dobElement) {
        return;
    }

    const birthDateTime =
        dobElement.innerText.trim();

    try {

        const response = await fetch(
            "/workspace_time_adjust",
            {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    birth_datetime:
                        birthDateTime,

                    seconds:
                        seconds
                })
            }
        );

        const data =
            await response.json();

        console.log(
            "BTR UPDATE:",
            data
        );

        if (!data.success) {

            alert(
                data.error || "Update failed"
            );

            return;
        }

        renderCharts(data);

        renderDasa(data);

        renderBirthDetails(data);

        renderRulingPlanets(data);

        renderSutraGrid(data);

    } catch(err) {

        console.error(err);

        alert(
            "BTR update failed."
        );
    }
};

