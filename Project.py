import cv2
import numpy as np
import pickle
from flask import Flask, request,jsonify




rectW, rectH = 30,30
def rescale_frame(frame, scale):    # works for image, video, live video
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)
def check(imgPro, posList):
    spaceCount = 0
    for pos in posList:
        x, y = pos
        crop = imgPro[y:y+rectH, x:x+rectW]
        count = cv2.countNonZero(crop)
        if count < 250:
            spaceCount += 1
            
    return {'capacity': len(posList)-3, 'freespaces': spaceCount-3}

def predict():
    cap = cv2.VideoCapture('rtsp://admin:LJJRLI@193.227.12.175')
  
   
    with open('CarParkPos.pkl', 'rb') as f:
        posList = pickle.load(f)

    for i in range(1):
           _,frameee=cap.read()
           img = rescale_frame(frameee, scale=.73)
           
           gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
           blur = cv2.GaussianBlur(gray, (3, 3), 1)
           Thre = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
           blur = cv2.medianBlur(Thre, 5)
           kernel = np.ones((3, 3), np.uint8)
           dilate = cv2.dilate(blur, kernel, iterations=1)
           predictt = check(imgPro=dilate, posList=posList)
    return jsonify(predictt)




app = Flask(__name__)

@app.route('/parking', methods=["GET"])
def parking():
    return predict()

if __name__ == '__main__':
    app.run(debug=True)

