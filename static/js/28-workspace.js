
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

    renderAdditionalPanels(data);
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

    const box = document.getElementById("dasaNavigator");

    if (!box) return;

    const tree = data.dasa_tree || [];

    if (!tree.length) {

        box.innerHTML = `
            <div style="
                padding:10px;
                color:#aa0000;
                font-size:18px;
            ">
                No Vimshottari data available
            </div>
        `;

        return;
    }

    let html = `
        <div style="
            font-size:22px;
            font-weight:bold;
            margin-bottom:14px;
            color:#002b7f;
        ">
            Vimshottari Dasa Navigator
        </div>
    `;

    tree.forEach((maha, mi) => {

        const mahaId = "maha_" + mi;

        html += `
            <div style="
                border:1px solid #d7ddff;
                border-radius:8px;
                margin-bottom:12px;
                overflow:hidden;
                background:#fff;
            ">

                <div
                    onclick="toggleDasa('${mahaId}')"
                    style="
                        padding:12px;
                        cursor:pointer;
                        background:#eef3ff;
                    "
                >
                    <div style="
                        font-size:18px;
                        font-weight:bold;
                        color:#003399;
                    ">
                        ▶ ${(maha.maha || maha.name || maha.lord || "")} Mahadasa
                    </div>

                    <div style="
                        margin-top:4px;
                        font-size:14px;
                        color:#333;
                    ">
                        ${maha.start || ""} → ${maha.end || ""}
                    </div>
                </div>

                <div
                    id="${mahaId}"
                    style="
                        display:none;
                        padding:10px;
                        background:#fff;
                    "
                >
        `;

        const bhuktis = maha.children || maha.bhukti || [];

        bhuktis.forEach((bhukti, bi) => {

            const bhuktiId = mahaId + "_bhukti_" + bi;

            html += `
                <div style="
                    margin-bottom:10px;
                    border-left:4px solid #5c7cff;
                    background:#f8faff;
                    border-radius:4px;
                ">

                    <div
                        onclick="toggleDasa('${bhuktiId}')"
                        style="
                            padding:10px;
                            cursor:pointer;
                        "
                    >

                        <div style="
                            font-size:15px;
                            font-weight:bold;
                            color:#1f45a5;
                        ">
                            ▶ ${(bhukti.bhukti || bhukti.name || bhukti.lord || "")} Bhukti
                        </div>

                        <div style="
                            margin-top:3px;
                            font-size:13px;
                            color:#444;
                        ">
                            ${bhukti.start || ""} → ${bhukti.end || ""}
                        </div>

                    </div>

                    <div
                        id="${bhuktiId}"
                        style="
                            display:none;
                            padding:8px 12px;
                            background:#fff;
                        "
                    >
            `;

            const antarList = bhukti.children || bhukti.antar || [];

            antarList.forEach((antara) => {

                html += `
                    <div style="
                        margin-bottom:8px;
                        padding:8px;
                        border-left:3px solid #9fb2ff;
                        background:#fcfdff;
                    ">

                        <div style="
                            font-size:14px;
                            font-weight:bold;
                            color:#333;
                        ">
                            ${(antara.pratyantar || antara.name || antara.lord || "")} Antara
                        </div>

                        <div style="
                            margin-top:2px;
                            font-size:12px;
                            color:#555;
                        ">
                            ${antara.start || ""} → ${antara.end || ""}
                        </div>

                    </div>
                `;
            });

            html += `
                    </div>
                </div>
            `;
        });

        html += `
                </div>
            </div>
        `;
    });

    box.innerHTML = html;
}

function toggleDasa(id){

    const el = document.getElementById(id);

    if(!el) return;

    el.style.display =
        el.style.display === "none"
        ? "block"
        : "none";
}


function toggleDasa(id){

    const el =
        document.getElementById(id);

    if(!el) return;

    el.style.display =
        el.style.display === "none"
        ? "block"
        : "none";
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

            <td class="sutra-label">Planet Significators</td>

            <td><b>${r.planet || ""}</b></td>

            <td>${r.planet_houses || ""}</td>

            <td><b>${r.star_lord || ""}</b></td>

            <td>${r.star_houses || ""}</td>

            <td><b>${r.sub_lord || ""}</b></td>

            <td>${r.sub_houses || ""}</td>

        </tr>

        <tr>

            <td class="sutra-label">Star Lord Significators</td>

            <td><b>${r.star_lord || ""}</b></td>

            <td>${r.star_houses || ""}</td>

            <td colspan="4">&nbsp;</td>

        </tr>

        <tr class="sutra-bottom-row">

            <td class="sutra-label">Sub Lord Significators</td>

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

    renderAdditionalPanels(data);

    } catch(err) {

        console.error(err);

        alert(
            "BTR update failed."
        );
    }
};



function showWorkspacePanel(panelId, btn){

    document.querySelectorAll('.workspace-panel')
    .forEach(panel => {
        panel.style.display = 'none';
    });

    const active =
        document.getElementById(panelId);

    if(active){
        active.style.display = 'block';
    }

    document.querySelectorAll('.workspace-tab')
    .forEach(tab => {
        tab.classList.remove('active-tab');
    });

    if(btn){
        btn.classList.add('active-tab');
    }
}

function renderAdditionalPanels(data){

    const planets =
        document.getElementById('planetsContent');

    if(planets){

        let html =
            '<table class="sutra-grid-horosoft">';

        const sourcePlanets =
             data.planets
            || data.natal_table
            || [];

        const planetRows =
        Array.isArray(sourcePlanets)
        ? sourcePlanets
        : Object.values(sourcePlanets || {});

        planetRows.forEach(p => {

            html += '<tr>'
                + '<td><b>' + (p.planet || '') + '</b></td>'
                + '<td>' + (p.sign || '') + '</td>'
                + '<td>' + (p.degree || p.sign_degree || '') + '</td>'
                + '</tr>';
        });

        html += '</table>';

        planets.innerHTML = html;
    }

    const cusps =
        document.getElementById('cuspsContent');

    if(cusps){

        let html =
            '<table class="sutra-grid-horosoft">';

        const cuspRows =
            Array.isArray(data.cusps)
            ? data.cusps
            : Object.values(data.cusps || {});

        cuspRows.forEach(c => {

            html += '<tr>'
                + '<td><b>' + (c.house || '') + '</b></td>'
                + '<td>' + (c.sign || '') + '</td>'
                + '<td>' + (c.degree || '') + '</td>'
                + '</tr>';
        });

        html += '</table>';

        cusps.innerHTML = html;
    }

    const kp249 =
        document.getElementById('kp249Content');

    if(kp249){

        kp249.innerHTML =
            '<pre style="font-size:18px;">'
            + JSON.stringify(data.kp_249 || {}, null, 2)
            + '</pre>';
    }
    
}




/* ===== SAFE REVOLVE SUPPORT ===== */

window.workspaceData = null;

const __originalRenderWorkspace = renderWorkspace;

renderWorkspace = function(data){

    window.workspaceData = data;

    __originalRenderWorkspace(data);
};

const __originalAdjustBirthTime = window.adjustBirthTime;

window.adjustBirthTime = async function(unit, direction){

    await __originalAdjustBirthTime(unit, direction);

    try{

        const response =
            await fetch("/workspace_data");

        const data =
            await response.json();

        window.workspaceData = data;

    }catch(e){

        console.log(
            "workspace refresh failed",
            e
        );
    }
};

window.revolveFromHouse = function(){

    try{

        const input =
            document.getElementById(
                "revolveHouseInput"
            );

        if(!input){
            return;
        }

        const fromHouse =
            parseInt(input.value || "1");

        if(
            isNaN(fromHouse)
            || fromHouse < 1
            || fromHouse > 12
        ){
            alert("Enter house 1-12");
            return;
        }

        if(!window.workspaceData){
            return;
        }

        function rotate(chart){

            const rotated = {};

            for(let i=1;i<=12;i++){

                const newHouse =
                    (((i - fromHouse + 12) % 12) + 1);

                rotated[newHouse] =
                    chart[i]
                    || chart[String(i)]
                    || [];
            }

            return rotated;
        }

        drawWorkspaceChart(
            "lagnaChart",
            rotate(
                window.workspaceData
                .lagna_chart_workspace || {}
            )
        );

        drawWorkspaceChart(
            "bhavChart",
            rotate(
                window.workspaceData
                .bhav_chart || {}
            )
        );

    }catch(e){

        console.log(
            "revolve failed",
            e
        );
    }
};

