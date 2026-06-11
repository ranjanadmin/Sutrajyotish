function saveSession(){

    localStorage.setItem(
        "palmsutra_v3",
        JSON.stringify({
            symbols:symbols
        })
    );

    alert("Saved");
}

function loadSession(){

    let d =
        localStorage.getItem(
            "palmsutra_v3"
        );

    if(!d) return;

    d = JSON.parse(d);

    symbols =
        d.symbols || [];

    redraw();
}