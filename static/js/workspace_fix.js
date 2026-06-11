
/* =========================
   SUTRA WORKSPACE FINAL FIX
========================= */

console.log("WORKSPACE FINAL FIX LOADED");

function renderDasa(data){

    const box =
        document.getElementById(
            "dasaNavigator"
        );

    const panel =
        document.getElementById(
            "dasaOnlyContent"
        );

    let dasaText =
        data.running_dasa || "";

    if(
        data.current_dasa &&
        data.current_dasa.maha
    ){

        dasaText =
            `${data.current_dasa.maha || ""} / `
            + `${data.current_dasa.antar || ""} / `
            + `${data.current_dasa.pratyantar || ""}`;
    }

    if(box){

        box.innerHTML = `
        <div style="
            padding:12px;
            font-size:22px;
            font-weight:bold;
            color:#0b3aa4;
        ">
            ${dasaText}
        </div>`;
    }

    if(panel){

        panel.innerHTML = `
        <div style="
            padding:20px;
            font-size:24px;
            font-weight:bold;
            color:#0b3aa4;
        ">
            ${dasaText}
        </div>`;
    }
}

function renderAdditionalPanels(data){

    console.log(
        "WORKSPACE DATA FULL:",
        data
    );

    console.log(
        "KP249 LENGTH:",
        (data.kp_249 || []).length
    );

    // PLANETS
    const planets =
        document.getElementById(
            "planetsContent"
        );

    if(planets){

        let html = `
        <table class="sutra-grid-horosoft">
        <tr>
            <th>Planet</th>
            <th>Sign</th>
            <th>Degree</th>
            <th>Nak</th>
            <th>Sub</th>
        </tr>`;

        (data.natal_table || []).forEach(r => {

            html += `
            <tr>
                <td>${r.planet || ""}</td>
                <td>${r.sign || ""}</td>
                <td>${r.sign_degree || r.degree || ""}</td>
                <td>${r.nak || ""}</td>
                <td>${r.sub || ""}</td>
            </tr>`;
        });

        html += `</table>`;

        planets.innerHTML = html;
    }

    // CUSPS
    const cusps =
        document.getElementById(
            "cuspsContent"
        );

    if(cusps){

        let html = `
        <table class="sutra-grid-horosoft">
        <tr>
            <th>House</th>
            <th>Sign</th>
            <th>Degree</th>
            <th>Nak</th>
            <th>Sub</th>
        </tr>`;

        (data.cusps || []).forEach(r => {

            html += `
            <tr>
                <td>${r.house || ""}</td>
                <td>${r.sign || ""}</td>
                <td>${r.sign_degree || r.degree || ""}</td>
                <td>${r.nak || ""}</td>
                <td>${r.sub || ""}</td>
            </tr>`;
        });

        html += `</table>`;

        cusps.innerHTML = html;
    }

    // KP249
    const kp =
        document.getElementById(
            "kp249Content"
        );

    if(kp){

        let html = `
        <table class="sutra-grid-horosoft">
        <tr>
            <th>SL</th>
            <th>Sign Lord</th>
            <th>Nak Lord</th>
            <th>Sub Lord</th>
            <th>Start</th>
            <th>End</th>
        </tr>`;

        const rows =
            data.kp_249 || [];

        rows.forEach(r => {

            html += `
            <tr>
                <td>${r.serial || ""}</td>
                <td>${r.sign_lord || ""}</td>
                <td>${r.nak_lord || ""}</td>
                <td>${r.sub_lord || ""}</td>
                <td>${r.start_dms || ""}</td>
                <td>${r.end_dms || ""}</td>
            </tr>`;
        });

        html += `</table>`;

        kp.innerHTML = html;
    }

    renderDasa(data);
}
