
/* =========================================================
   TIMELINE STYLE VIMSHOTTARI DASA NAVIGATOR
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

function buildBhuktiList(parent){

    const bhuktis = [
        "Sun","Moon","Mars","Mercury",
        "Jupiter","Venus","Saturn",
        "Rahu","Ketu"
    ];

    return bhuktis.map(name => {

        return {

            antar:name,
            start:parent.start || "",
            end:parent.end || "",

            antars:[

                {
                    pratyantar:name,
                    start:parent.start || "",
                    end:parent.end || ""
                }
            ]
        };
    });
}

function renderTimelineLevel(items, level){

    if(!items || !items.length){
        return "";
    }

    let html = `
    <div style="
        margin-left:${level * 28}px;
        margin-top:6px;
    ">`;

    items.forEach((item, idx) => {

        const uid =
            "timeline_" +
            level + "_" +
            idx + "_" +
            Math.random()
            .toString(36)
            .substring(2,7);

        const title =
            item.maha ||
            item.antar ||
            item.pratyantar ||
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

        let children =
            item.bhuktis ||
            item.antars ||
            item.pratyantars ||
            item.children ||
            [];

        if(
            level === 0 &&
            (!children || !children.length)
        ){
            children = buildBhuktiList(item);
        }

        html += `

        <div style="
            margin-bottom:14px;
        ">

            <div
                onclick="
                    toggleDasaNode('${uid}')
                "
                style="
                    background:#f5f5f5;
                    border-radius:8px;
                    padding:12px 16px;
                    font-family:Arial;
                    font-size:18px;
                    font-weight:bold;
                    cursor:pointer;
                    border:1px solid #d8d8d8;
                "
            >

                ▶ ${title}

                <span style="
                    margin-left:12px;
                    color:#000000;
                ">
                    | ${start} → ${end}
                </span>

            </div>

            <div
                id="${uid}"
                style="
                    display:none;
                    margin-top:8px;
                "
            >

                ${renderTimelineLevel(
                    children,
                    level + 1
                )}

            </div>

        </div>`;
    });

    html += `</div>`;

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

    rows = rows.map(r => {

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

            bhuktis:
                r.bhuktis || []
        };
    });

    container.innerHTML = `

    <div style="
        margin-top:10px;
    ">

        <div style="
            font-size:24px;
            font-weight:bold;
            margin-bottom:18px;
            font-family:Arial;
        ">
            Vimshottari Dasa Navigator
        </div>

        ${renderTimelineLevel(rows, 0)}

    </div>`;
}
