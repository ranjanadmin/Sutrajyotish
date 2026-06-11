// ================= UTILITY =================
function dateDiffInDays(start, end) {
    try {
        const s = new Date(start);
        const e = new Date(end);

        if (isNaN(s) || isNaN(e)) return 1;

        return Math.max(1, (e - s) / (1000 * 60 * 60 * 24));
    } catch {
        return 1;
    }
}

// ================= MAIN ENTRY =================
function renderDasha(dasha) {

    const mahaContainer = document.getElementById("mahadasha-list");
    const antarContainer = document.getElementById("antardasha-list");

    if (!mahaContainer || !antarContainer) return;

    mahaContainer.innerHTML = "";
    antarContainer.innerHTML = "";

    if (!dasha || dasha.length === 0) {
        mahaContainer.innerHTML = "<div>No Dasha Data</div>";
        return;
    }

    renderMahadasha(dasha);
}

// ================= MAHADASHA =================
function renderMahadasha(dasha) {

    const container = document.getElementById("mahadasha-list");
    if (!container) return;

    container.innerHTML = "";

    dasha.forEach(m => {

        const duration = dateDiffInDays(m.start, m.end);
        const width = Math.max(80, duration * 0.3);

        const btn = document.createElement("button");

        btn.innerHTML = `
            <b>${m.name || ""}</b><br>
            ${m.start || ""} → ${m.end || ""}
        `;

        btn.onclick = () => renderAntardasha(m);

        container.appendChild(btn);
    });
}

// ================= ANTARDASHA =================
function renderAntardasha(maha) {

    const container = document.getElementById("antardasha-list");
    if (!container) return;

    container.innerHTML = `<h4>Antardasha (${maha.name || ""})</h4>`;

    if (!maha.children || maha.children.length === 0) {
        container.innerHTML += "<div>No Antardasha Data</div>";
        return;
    }

    maha.children.forEach(sub => {

        const duration = dateDiffInDays(sub.start, sub.end);
        const width = Math.max(120, duration * 0.4);

        const div = document.createElement("div");

        div.style.border = "1px solid #ccc";
        div.style.marginBottom = "6px";
        div.style.padding = "6px";
        div.style.cursor = "pointer";

        div.innerHTML = `
            <b>${sub.name || ""}</b><br>
            ${sub.start || ""} → ${sub.end || ""}
        `;

        div.onclick = () => renderPratyantar(sub);

        container.appendChild(div);
    });
}

// ================= PRATYANTAR =================
function renderPratyantar(sub) {

    const container = document.getElementById("antardasha-list");

    if (!container) return;

    let html = `<h4>Pratyantar (${sub.name || ""})</h4>`;

    if (!sub.children || sub.children.length === 0) {
        html += "<div>No Pratyantar Data</div>";
        container.innerHTML = html;
        return;
    }

    sub.children.forEach(ss => {

        html += `
            <div style="padding:5px; border-bottom:1px solid #ddd;">
                ${ss.name || ""}<br>
                ${ss.start || ""} → ${ss.end || ""}
            </div>
        `;
    });

    container.innerHTML = html;
}