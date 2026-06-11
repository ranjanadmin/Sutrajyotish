
/* =========================================================
   HOROSOFT STYLE VIMSHOTTARI DASA NAVIGATOR
   Replace existing:
   - renderNestedLevel()
   - toggleDasaNode()
   - buildFlatDasaTree()
   - renderDasaDrilldown()
   ========================================================= */

function toggleDasaNode(id){

    const el =
        document.getElementById(id);

    if(!el){
        return;
    }

    if(
        el.style.display === "none"
        ||
        !el.style.display
    ){
        el.style.display = "block";
    }

    else{
        el.style.display = "none";
    }
}

function buildFlatDasaTree(rows){

    if(!rows || !rows.length){
        return [];
    }

    return rows.map(r => {

        return {

            maha:
                r.dasa ||
                r.maha ||
                r.name ||
                "",

            start:
                r.start ||
                r.start_date ||
                "",

            end:
                r.end ||
                r.end_date ||
                "",

            bhuktis:[

                {
                    antar:"Bhukti",
                    start:
                        r.start ||
                        r.start_date ||
                        "",

                    end:
                        r.end ||
                        r.end_date ||
                        "",

                    antars:[

                        {
                            pratyantar:"Antar",
                            start:
                                r.start ||
                                r.start_date ||
                                "",

                            end:
                                r.end ||
                                r.end_date ||
                                ""
                        }
                    ]
                }
            ]
        };
    });
}

function renderNestedLevel(items, level){

    if(!items || !items.length){
        return "";
    }

    let html = `
    <table style="
        width:100%;
        border-collapse:collapse;
        font-family:Tahoma;
        font-size:15px;
    ">`;

    items.forEach((item, idx) => {

        const uid =
            "dasa_" +
            level + "_" +
            idx;

        const title =
            item.maha ||
            item.antar ||
            item.pratyantar ||
            item.sookshma ||
            item.name ||
            "Dasa";

        const start =
            item.start ||
            item.start_date ||
            "";

        const end =
            item.end ||
            item.end_date ||
            "";

        const children =
            item.bhuktis ||
            item.antars ||
            item.pratyantars ||
            item.children ||
            [];

        const color =
            level === 0
            ? "#000000"
            : "#ff0000";

        html += `

        <tr
            onclick="toggleDasaNode('${uid}')"
            style="
                cursor:pointer;
                border-bottom:1px solid #dddddd;
            "
        >

            <td style="
                width:40px;
                padding:6px;
                color:${color};
                font-weight:bold;
            ">
                ○
            </td>

            <td style="
                width:90px;
                padding:6px;
                color:${color};
                font-size:18px;
            ">
                ${title}
            </td>

            <td style="
                width:220px;
                padding:6px;
                color:${color};
                font-size:18px;
            ">
                ${start}
            </td>

            <td style="
                width:40px;
                padding:6px;
                text-align:center;
                color:${color};
                font-size:18px;
            ">
                -
            </td>

            <td style="
                padding:6px;
                color:${color};
                font-size:18px;
            ">
                ${end}
            </td>

        </tr>

        <tr id="${uid}" style="display:none;">

            <td colspan="5" style="
                padding-left:${(level + 1) * 35}px;
                background:#fafafa;
            ">

                ${renderNestedLevel(
                    children,
                    level + 1
                )}

            </td>

        </tr>
        `;
    });

    html += `</table>`;

    return html;
}

function renderDasaDrilldown(data){

    const container =
        document.getElementById(
            "dasaDrilldownContainer"
        );

    if(!container){
        return;
    }

    let rows =
        data.vimshottari_rows ||
        data.dasa_tree ||
        [];

    if(!rows.length){

        container.innerHTML = `
        <div style="
            padding:15px;
            color:#7c2d12;
            font-weight:bold;
        ">
            No Vimshottari data available
        </div>`;

        return;
    }

    if(
        !rows[0].bhuktis &&
        !rows[0].antars
    ){
        rows = buildFlatDasaTree(rows);
    }

    container.innerHTML = `

    <div style="
        border:2px solid #55aa00;
        background:#ffffff;
    ">

        <div style="
            padding:6px 10px;
            border-bottom:2px solid #55aa00;
            font-size:24px;
            color:#5a00ff;
            text-decoration:underline;
            font-family:Tahoma;
        ">
            Vimshottari Dasa
        </div>

        <div style="
            padding:8px 12px;
            font-size:28px;
            color:#000000;
            font-family:Tahoma;
        ">
            ${data.running_dasa || ""}
        </div>

        ${renderNestedLevel(rows, 0)}

    </div>`;
}
