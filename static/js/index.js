



var ctx = canvas.getContext('2d');
resize();
ctx.fillRect(0,0,250,250,'#000')
// last known position
var pos = { x: 0, y: 0 };

//window.addEventListener('resize', resize);
window.addEventListener('load', ()=>{
    
    document.addEventListener('mousemove', draw);
    document.addEventListener('mousedown', setPosition);
    document.addEventListener('mouseenter', setPosition);
    
})
function getOffset(el) {
    const rect = el.getBoundingClientRect();
    return {
      left: rect.left + window.scrollX,
      top: rect.top + window.scrollY
    };
  }
  
// new position from mouse event
function setPosition(e) {
    e.preventDefault();
    e.stopPropagation();
    //console.log(e)
    let cr = canvas.getBoundingClientRect()
    x = e.clientX - cr.left
    y = e.clientY - cr.top
    //console.log(`${x} ${y}`)
    pos.x = x
    pos.y = y
}

// resize canvas
function resize() {
    ctx.canvas.width = 250;
    ctx.canvas.height = 250;
}

function draw(e) {
    e.preventDefault();
    e.stopPropagation();
    // mouse left button must be pressed
    if (e.buttons !== 1) return;
    ctx.beginPath(); // begin
    ctx.lineWidth = 25;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#FFFFFF';
    ctx.moveTo(pos.x, pos.y); // from
    setPosition(e);
    ctx.lineTo(pos.x, pos.y); // to
    ctx.stroke(); // draw it!
}

async function load() {
    pred.innerHTML = `<img width=55 height=55 src='static/load.gif'/>`
    let form = document.getElementById('form1')
    console.log(form)
    let res = await fetch('/load', {
        method: 'POST', 
        body: new FormData(form)
    })
    if (res.status == 200){
        let src = await res.text()
        pred.innerHTML = `<img width=640 height=480 src='${src}'/>`
    } else {
        let errMsg = await res.text()
        pred.innerHTML = `<h2>Ошибка: ${errMsg}</h2>`;
    }
    
}

async function loadCanvas() {
    pred.innerHTML = `<img width=55 height=55 src='static/load.gif'/>`
    let form = document.getElementById('form2')
    let formData = new FormData(form)

    let dataURL =  canvas.toDataURL('image/jpeg', 0.5)
    let blob = dataURItoBlob(dataURL)
    formData.append('image', blob)
    console.log(formData.get('image'))

    let res = await fetch('/load', {
        method: 'POST', 
        body:formData
    })

    if (res.status == 200){
        let src = await res.text()
        pred.innerHTML = `<img width=640 height=480 src='${src}'/>`
    } else {
        let errMsg = await res.text()
        pred.innerHTML = `<h2>Ошибка: ${errMsg}</h2>`;
    }
}

function dropCanvas() {
    ctx.fillRect(0,0,500,500,'#000')
}

function dataURItoBlob (dataURI) {
    // convert base64/URLEncoded data component to raw binary data held in a string
    var byteString;
    if (dataURI.split(',')[0].indexOf('base64') >= 0)
        byteString = atob(dataURI.split(',')[1]);
    else
        byteString = unescape(dataURI.split(',')[1]);

    // separate out the mime component
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

    // write the bytes of the string to a typed array
    var ia = new Uint8Array(byteString.length);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }

    return new Blob([ia], {type: mimeString});
}