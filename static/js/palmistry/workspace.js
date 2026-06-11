let currentPalm = "left";
let currentMode = "";

function setMode(mode){

    currentMode = mode;

    const e =
        document.getElementById(
            "statusMode"
        );

    if(e){
        e.innerText = mode;
    }
}

function switchPalm(side){

    currentPalm = side;

    const e =
        document.getElementById(
            "statusPalm"
        );

    if(e){
        e.innerText = side;
    }

    redraw();
}

function updateStatus(){

    const modeEl =
        document.getElementById("statusMode");

    const palmEl =
        document.getElementById("statusPalm");

    if(modeEl){
        modeEl.innerText =
            currentMode || "None";
    }

    if(palmEl){
        palmEl.innerText =
            currentPalm;
    }
}

document.addEventListener(
    "DOMContentLoaded",
    function(){

        updateStatus();

        if(typeof resizeCanvas === "function"){
            resizeCanvas();
        }
    }
);

let compareMode = false;
function toggleCompareMode(){

    compareMode = !compareMode;

    redraw();
}

function updateZoomDisplay(){

    const e =
        document.getElementById(
            "statusZoom"
        );

    if(e){
        e.innerText =
            Math.round(
                imgScale * 100
            ) + "%";
    }
}