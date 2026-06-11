let traces = [];

function undoLast(){

    traces.pop();

    redraw();
}

function clearCanvas(){

    traces = [];

    redraw();
}