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


