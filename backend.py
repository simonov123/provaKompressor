#backend.py
from fastapi import FastAPI, UploadFile, File,Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import numpy as np
import componentcounter 
import photokompressor
from io import BytesIO
import base64 
import cv2
import tempfile
import time

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o metti l'URL preciso del tuo frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/svd_count")
async def getdata(file: UploadFile=File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    A = np.array(image).astype(float)
    compnum=componentcounter.counterscript(A)
    file_size_bytes = len(contents)
    size_mb=file_size_bytes/1000000
    return {"num_singular_values_red": compnum,"size": size_mb}

@app.post("/svd_imgcompress")
async def compress(file: UploadFile=File(...),precision: int = Form(...),prec100: int= Form(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    A = np.array(image).astype(float)
    A_compressed=photokompressor.compression(precision,A)
    compressed_pil = Image.fromarray(np.clip(A_compressed,0,255).astype(np.uint8))
    buf = BytesIO()
    compressed_pil.save(buf,format="JPEG", quality=prec100)
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return {"image_base64": img_base64}

@app.post("/svd_vidcount")
async def getvidata(file: UploadFile=File(...)):
    contents = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name
    cap=cv2.VideoCapture(tmp_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    data1=f"Frames: {frame_count}, FPS: {fps}, Risoluzione: {width}x{height}"

    #lettura frame
    counter=0
    frames=[]
    for i in range(frame_count):
     ret, frame = cap.read()  # spacchetta la tupla
     if not ret:
        break  # fine video
     frames.append(frame)
     counter += 1
    
    sample=frames[0]
    RGBsample= Image.fromarray(sample).convert("RGB") 
    A = np.array(RGBsample).astype(float)
    compnum=componentcounter.counterscript(A)
    file_size_bytes = len(contents)
    size_mb=file_size_bytes/1000000
    data2=str(size_mb)+" MB"
    dat=data1+" "+data2
    print(dat)
    return {"num_singular_values_red": compnum,"data1": data1,"data2":data2}

@app.post("/svd_vidcompress")
async def vidcompress(file: UploadFile=File(...),precision: int = Form(...),prec100: int= Form(...)):
    print("compress!")
    contents = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name
    cap=cv2.VideoCapture(tmp_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    #lettura frame
    counter=0
    frames=[]
    for i in range(frame_count):
     ret, frame = cap.read()  # spacchetta la tupla
     if not ret:
        break  # fine video
     frames.append(frame)
     counter += 1
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # codec per mp4
    out = cv2.VideoWriter(str(time.localtime)+"compressed_video.mp4", fourcc, fps, (width, height))

    for act in frames:
     RGBact = Image.fromarray(act).convert("RGB") 
     A = np.array(RGBact).astype(float)
     A_compressed = photokompressor.compression(precision, A)
     compressed_np = np.clip(A_compressed, 0, 255).astype(np.uint8)
     out.write(compressed_np)   # scrive il frame nel video

    out.release()

    
    
    








    


    

    



