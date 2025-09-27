
const imgdata=document.getElementById("upload");
const tempdata=document.getElementById("tempdata")
const backendURL = "http://127.0.0.1:8000";
const slider=document.createElement("input");
const confirmbut=document.createElement("button");

imgdata.addEventListener('change', async () => {
    console.log("fun1")
    const file = imgdata.files[0];
    if (!file) return alert("Seleziona un file!");

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${backendURL}/svd_count`, {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    var precision=data.num_singular_values_red;
    var size=data.size;
    tempdata.textContent="il peso attuale dell'immagine è:"+size+" MB\n"
    slider.type = "range";
    slider.min = 0;
    slider.max = 100;
    slider.step = 1;
    slider.value = 50;
    slider.id = "precision";
    const sliderLabel = document.createElement("span");
    sliderLabel.id = "precisionValue";
    sliderLabel.textContent = slider.value + "%";
    slider.addEventListener("input", () => {
  sliderLabel.textContent = slider.value + "%";

  if (slider.value < 15) {
    sliderLabel.style.color = "red";   
    sliderLabel.textContent = slider.value + "%\n"+"Attenzione,una compressione eccessiva potrebbe compromettere eccessivamente la qualità dell'immagine";
  } else {
    sliderLabel.style.color = "black"; 
  }
});
    confirmbut.textContent="comprimi";
    confirmbut.addEventListener('click',async() => {
        const formData2 = new FormData();
        formData2.append("file", file);
        formData2.append("precision",calcprec(slider.value,precision));
        formData2.append("prec100",slider.value);
        const imgresponse = await fetch(`${backendURL}/svd_imgcompress`, {
        method: "POST",
        body: formData2
    });
    const dataimg = await imgresponse.json();
    var lenght=Math.round((dataimg.image_base64.length*3/4))/1000000
    const previewImg = document.createElement("img");
    previewImg.src="data:image/png;base64,"+dataimg.image_base64;
    previewImg.style.display = "block";
    const previewData= document.createElement("label")
    previewData.textContent="precisione:"+slider.value+'%'+"     peso nuova immagine:"+lenght+" MB"
    dowbu=document.createElement("button");
    dowbu.textContent="download";
    dowbu.addEventListener('click',async()=>{
        const dlink=document.createElement("a");
        dlink.href="data:image/png;base64,"+dataimg.image_base64;
        dlink.download=Date.now()+".png";
        dlink.click();


    });
    document.body.appendChild(previewData);
    document.body.appendChild(previewImg);
    document.body.appendChild(dowbu);

    

    });
    document.body.appendChild(slider);
    document.body.appendChild(confirmbut);
    document.body.appendChild(sliderLabel);

    
});


function calcprec(prec100,prec){
    val=(prec/100)*prec100;
    return val;

}