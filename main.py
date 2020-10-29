import json
from keras.models import model_from_json

from mtcnn import MTCNN
import cv2
from PIL import Image
import math

detector = MTCNN()

class Face_Score:
    
    def __init__(self,model_path,model_weight):
        json_file = open(model_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        self.model.load_weights(model_weight)
        
    def detect_faces(self,img_loc,image_name):
        try:
            image = cv2.cvtColor(cv2.imread(img_loc),cv2.COLOR_BGR2RGB)
            face = detector.detect_faces(image)
            left = face[0]['box'][0]
            top = face[0]['box'][1]
            right = face[0]['box'][0] + face[0]['box'][2]
            bottom = face[0]['box'][1] + face[0]['box'][3]
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            pil_image.save('./face_detected_images/'+image_name)
            
        except:
            print('The image does not have face')
            
    def calculate_score(self,image_loc_1,image_loc_2):
        img1= cv2.imread(image_loc_1,0)
        img1 = cv2.resize(img1,(112,92))
        img2= cv2.imread(image_loc_2,0)
        img2 = cv2.resize(img2,(112,92))
        image1 = img1[::2, ::2]
        image2 = img2[::2,::2]
        image1 = (image1/255).reshape(1,1,56,46)
        image2 = (image2/255).reshape(1,1,56,46)
        #scaling need to be done to keep the sore in [0,1]
        #score above 73 means full match
        return 1 / (1 + math.exp(-(1-self.model.predict([image1,image2]))))
        