from typing import List
import shutil
import os
import glob

from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile

from main import Face_Score

app = FastAPI()

model = Face_Score('./model/model.json','./model/model.h5')

@app.get("/")
def read_root():
    return {"status": 200,"message":"Face scoring model is running"}
    
    
@app.post("/uploadfile/")
async def image(images: List[UploadFile] = File(...)):
    file_names = []
    count = 1
    upload_data = glob.glob('./uploaded_images/*')
    face_data = glob.glob('./face_detected_images/*')
    
    if len(upload_data)>0:
        for f in upload_data:
            os.remove(f)
            
    if len(face_data)>0:
        for f in face_data:
            os.remove(f)
            
    for image in images:
        with open('./uploaded_images/'+image.filename, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        file_names.append(image.filename)
        count += 1
        
    for img in file_names:
        model.detect_faces('./uploaded_images/'+img,img)
        
        
    image_loc_1 = './face_detected_images/'+file_names[0]
    image_loc_2 = './face_detected_images/'+file_names[1]
    
    score = model.calculate_score(image_loc_1,image_loc_2)
    return {'Face match score': score}   