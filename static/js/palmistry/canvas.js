const canvas =
    document.getElementById("canvas");

const ctx =
    canvas.getContext("2d");

let img = new Image();

let imgScale = 1;
let imgX = 0;
let imgY = 0;

function resizeCanvas(){

    canvas.width =
        canvas.clientWidth;

    canvas.height =
        canvas.clientHeight;

    redraw();
}

window.addEventListener(
    "resize",
    resizeCanvas
);

function loadPalmImage(event){

    const file =
        event.target.files[0];

    if(!file) return;

    const reader =
        new FileReader();

    reader.onload = function(e){

        img.onload = function(){

            fitImageToCanvas();

            redraw();
        };

        img.src =
            e.target.result;
    };

    reader.readAsDataURL(file);
}


function redraw(){

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    if(
        img &&
        img.complete &&
        img.width > 0
    ){

        ctx.drawImage(
            img,
            imgX,
            imgY,
            img.width*imgScale,
            img.height*imgScale
        );
    }
}

function fitImageToCanvas(){

    const scaleX =
        canvas.width / img.width;

    const scaleY =
        canvas.height / img.height;

    imgScale =
        Math.min(scaleX, scaleY);

    imgX =
        (canvas.width -
        img.width * imgScale) / 2;

    imgY =
        (canvas.height -
        img.height * imgScale) / 2;
}
function zoomIn(){

    imgScale *= 1.1;

    redraw();
    if(typeof updateZoomDisplay === "function"){
    updateZoomDisplay();
}
}

function zoomOut(){

    imgScale /= 1.1;

    redraw();
    if(typeof updateZoomDisplay === "function"){
    updateZoomDisplay();
}
}
canvas.addEventListener(
    "wheel",
    function(e){

        e.preventDefault();

        if(e.deltaY < 0){

            zoomIn();

        }else{

            zoomOut();
        }
    }
);
let isPanning = false;
let startX = 0;
let startY = 0;
canvas.addEventListener(
    "mousedown",
    function(e){

        if(!panMode) return;

        isPanning = true;

        startX = e.clientX;
        startY = e.clientY;
    }
);

canvas.addEventListener(
    "mousemove",
    function(e){

        if(!isPanning) return;

        imgX +=
            e.clientX - startX;

        imgY +=
            e.clientY - startY;

        startX = e.clientX;
        startY = e.clientY;

        redraw();
    }
);

canvas.addEventListener(
    "mouseup",
    function(){

        isPanning = false;
    }
);
