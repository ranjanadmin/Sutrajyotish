let canvas = document.getElementById("canvas");
let ctx = canvas.getContext("2d");
let img = new Image();

let mode = "life";
let drawing = false;
let showAges = true;

// Zoom
let scale = 1;
let originX = 0;
let originY = 0;

// Data
let lifeLinePoints = [];
let fateLinePoints = [];
let headLinePoints = [];
let heartLinePoints = [];

// ================= IMAGE =================
function loadPalmImage(e) {
    let reader = new FileReader();
    reader.onload = function(ev) {
        img.onload = () => redraw();
        img.src = ev.target.result;
    };
    reader.readAsDataURL(e.target.files[0]);
}

// ================= MODE =================
function setMode(m){ mode = m; }

// ================= COORD =================
function getMousePos(e){
    let rect = canvas.getBoundingClientRect();
    return {
        x: (e.clientX - rect.left - originX) / scale,
        y: (e.clientY - rect.top - originY) / scale
    };
}

// ================= DRAW =================
canvas.onmousedown = () => drawing = true;
canvas.onmouseup = () => drawing = false;

canvas.onmousemove = function(e){
    if(!drawing) return;

    let p = getMousePos(e);

    if(mode==="life") lifeLinePoints.push(p);
    if(mode==="fate") fateLinePoints.push(p);
    if(mode==="head") headLinePoints.push(p);
    if(mode==="heart") heartLinePoints.push(p);

    redraw();
};

// ================= REDRAW =================
function redraw(){

    ctx.setTransform(1,0,0,1,0,0);
    ctx.clearRect(0,0,canvas.width,canvas.height);

    ctx.setTransform(scale,0,0,scale,originX,originY);

    ctx.drawImage(img,0,0,canvas.width,canvas.height);

    drawLine(lifeLinePoints,"green");
    drawLine(fateLinePoints,"cyan");
    drawLine(headLinePoints,"violet");
    drawLine(heartLinePoints,"red");

    if(showAges){
        drawLifeLineAge(lifeLinePoints);
        drawFateLineAge(fateLinePoints);
        drawHeadLineAge(headLinePoints);
        drawHeartLineAge(heartLinePoints);
    }
}

// ================= DRAW LINE =================
function drawLine(pts,color){
    if(pts.length<2) return;

    ctx.beginPath();
    ctx.strokeStyle=color;
    ctx.lineWidth=2;

    ctx.moveTo(pts[0].x,pts[0].y);
    for(let i=1;i<pts.length;i++){
        ctx.lineTo(pts[i].x,pts[i].y);
    }
    ctx.stroke();
}

// ================= ZOOM =================
function zoomIn(){ scale*=1.2; redraw(); }
function zoomOut(){ scale/=1.2; redraw(); }

// ================= COMMON =================
function dist(a,b){ return Math.hypot(b.x-a.x,b.y-a.y); }

// ================= LIFE =================
function drawLifeLineAge(pts){
    if(pts.length<2) return;

    let start = pts.reduce((m,p)=>p.x<m.x?p:m, pts[0]);

    let sorted=[start], rem=[...pts];
    rem.splice(rem.indexOf(start),1);

    while(rem.length){
        let last=sorted[sorted.length-1];
        let i=rem.reduce((b,p,idx)=>dist(last,p)<dist(last,rem[b])?idx:b,0);
        sorted.push(rem[i]); rem.splice(i,1);
    }

    let total=0;
    for(let i=1;i<sorted.length;i++)
        total+=dist(sorted[i-1],sorted[i]);

    let marks=[0,10,20,30,40,50,60,70,80];

    ctx.fillStyle="yellow";
    ctx.font="bold 14px Arial";

    marks.forEach(age=>{
        let target=(age/80)*total;
        let cur=0;

        for(let i=1;i<sorted.length;i++){
            cur+=dist(sorted[i-1],sorted[i]);
            if(cur>=target){
                ctx.fillText(age,sorted[i].x+6,sorted[i].y-6);
                break;
            }
        }
    });
}

// ================= FATE =================
function drawFateLineAge(pts){
    if(pts.length<2) return;

    let sorted=[...pts].sort((a,b)=>b.y-a.y);
    let bottom=sorted[0], top=sorted.reduce((m,p)=>p.y<m.y?p:m,sorted[0]);

    let total=bottom.y-top.y;

    let marks=[0,10,20,30,40,50,60,75];

    ctx.fillStyle="cyan";
    ctx.font="bold 14px Arial";

    marks.forEach(age=>{
        let y=bottom.y-(age/75)*total;

        let p=sorted.reduce((a,b)=>
            Math.abs(b.y-y)<Math.abs(a.y-y)?b:a);

        ctx.fillText(age,p.x+6,p.y-6);
    });
}

// ================= HEAD (RIGHT → LEFT) =================
function drawHeadLineAge(pts){
    if(pts.length<2) return;

    let start = pts.reduce((m,p)=>p.x>m.x?p:m, pts[0]);

    let sorted=[start], rem=[...pts];
    rem.splice(rem.indexOf(start),1);

    while(rem.length){
        let last=sorted[sorted.length-1];
        let i=rem.reduce((b,p,idx)=>dist(last,p)<dist(last,rem[b])?idx:b,0);
        sorted.push(rem[i]); rem.splice(i,1);
    }

    let right=sorted[0].x, left=sorted[sorted.length-1].x;
    let total=right-left;

    let marks=[0,10,20,30,40,50,60,70];

    ctx.fillStyle="violet";
    ctx.font="bold 14px Arial";

    marks.forEach(age=>{
        let x=right-(age/70)*total;

        let p=sorted.reduce((a,b)=>
            Math.abs(b.x-x)<Math.abs(a.x-x)?b:a);

        ctx.fillText(age,p.x+6,p.y-6);
    });
}

// ================= HEART (LEFT → RIGHT) =================
function drawHeartLineAge(pts){
    if(pts.length<2) return;

    let start = pts.reduce((m,p)=>p.x<m.x?p:m, pts[0]);

    let sorted=[start], rem=[...pts];
    rem.splice(rem.indexOf(start),1);

    while(rem.length){
        let last=sorted[sorted.length-1];
        let i=rem.reduce((b,p,idx)=>dist(last,p)<dist(last,rem[b])?idx:b,0);
        sorted.push(rem[i]); rem.splice(i,1);
    }

    let left=sorted[0].x, right=sorted[sorted.length-1].x;
    let total=right-left;

    let marks=[0,10,20,30,40,50,60,70,75];

    ctx.fillStyle="red";
    ctx.font="bold 14px Arial";

    marks.forEach(age=>{
        let x=left+(age/75)*total;

        let p=sorted.reduce((a,b)=>
            Math.abs(b.x-x)<Math.abs(a.x-x)?b:a);

        ctx.fillText(age,p.x+6,p.y-6);
    });
}

// ================= TOGGLE =================
function toggleAges(){ showAges=!showAges; redraw(); }

// ================= RESET =================
function clearCanvas(){
    lifeLinePoints=[];
    fateLinePoints=[];
    headLinePoints=[];
    heartLinePoints=[];
    redraw();
}