const videodata=document.getElementById("upload");
const backendURL = "http://127.0.0.1:8000";
const tempdata=document.getElementById("tempdata");
const slider=document.createElement("input");
const confirmbut=document.createElement("button");

videodata.addEventListener('change',async()=>{
    const file = videodata.files[0];
    if (!file) return alert("Seleziona un file!");
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch(`${backendURL}/svd_vidcount`, {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    var precision=data.num_singular_values_red;
    var data1=data.data1;
    var data2=data.data2;
    tempdata.textContent=data1+"  "+"dimensione: "+data2;
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
    sliderLabel.textContent = slider.value + "%\n"+"Attenzione,una compressione eccessiva potrebbe compromettere eccessivamente la qualità del video";
  } else {
    sliderLabel.style.color = "black"; 
  }
  
});
confirmbut.textContent="comprimi"; 
confirmbut.addEventListener('click',async()=>{
        const formData2 = new FormData();
        formData2.append("file", videodata.files[0]);
        formData2.append("precision",calcprec(slider.value,precision));
        formData2.append("prec100",slider.value);
        const vidresponse = await fetch(`${backendURL}/svd_vidcompress`, {
        method: "POST",
        body: formData2
    });
    const datavid = await vidresponse.json();

});

document.body.appendChild(slider);
document.body.appendChild(sliderLabel);
document.body.appendChild(confirmbut);


});













function imgkompr(){
    window.open("index.html", "_blank")
}

