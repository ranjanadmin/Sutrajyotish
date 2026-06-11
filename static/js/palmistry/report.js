function generateReport(){

    let report = [];

    report.push("PALMSUTRA REPORT");
    report.push("====================");
    report.push("");

    report.push(
        "Palm: " +
        currentPalm
    );

    report.push("");

    report.push("Mount Analysis");

    report.push(
        "Jupiter: " +
        (document.getElementById("m_jupiter")?.value || "")
    );

    report.push(
        "Saturn: " +
        (document.getElementById("m_saturn")?.value || "")
    );

    report.push(
        "Sun: " +
        (document.getElementById("m_sun")?.value || "")
    );

    report.push(
        "Mercury: " +
        (document.getElementById("m_mercury")?.value || "")
    );

    report.push(
        "Mars: " +
        (document.getElementById("m_mars")?.value || "")
    );

    report.push(
        "Moon: " +
        (document.getElementById("m_moon")?.value || "")
    );

    report.push(
        "Venus: " +
        (document.getElementById("m_venus")?.value || "")
    );

    report.push("");

    report.push("Notes");

    report.push(
        document.getElementById("notes")?.value || ""
    );

    report.push("");

    report.push("Symbols");

    if(typeof symbols !== "undefined"){

        symbols
        .filter(
            s => s.palm === currentPalm
        )
        .forEach(function(s){

            report.push(
                s.type +
                " (" +
                s.palm +
                ")"
            );
        });
    }

    const text =
        report.join("\n");

    const reportBox =
        document.getElementById(
            "report"
        );

    if(reportBox){

        reportBox.value = text;

    }else{

        alert(text);
    }
}