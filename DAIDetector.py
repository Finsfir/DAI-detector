#Detection class

import cv2 as cv
import numpy as np
import time
import math
import mathFunctions

from imageai.Detection.Custom import CustomObjectDetection

class DAIdetector:
    
    def __init__(self, fstProb = 50, secProb = 50):
        self.fstProb = fstProb
        self.secProb = secProb
        
        self.detector = CustomObjectDetection()
        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath("res/first cascade/models/detection_model-ex-015--loss-0013.902.h5")
        self.detector.setJsonPath("res/first cascade/json/detection_config.json")
        self.detector.loadModel()

        self.AngleDetector = CustomObjectDetection()
        self.AngleDetector.setModelTypeAsYOLOv3()
        self.AngleDetector.setModelPath("res/second cascade/models/detection_model-ex-015--loss-0022.383.h5")
        self.AngleDetector.setJsonPath("res/second cascade/json/detection_config.json")
        self.AngleDetector.loadModel()
        pass
    
    def detectDAI(self, inputImg, inputType = "file"):       
        inputImg = inputImg.copy()
        #inputImg = cv.resize(inputImg, (640, 640))
        detectedImage, detections = self.detector.detectObjectsFromImage(output_type="array", input_type = inputType,
                                                                         input_image = inputImg, 
                                                                         minimum_percentage_probability = self.fstProb)
        DAI, DAIcoord, alpha, DAIimgSet = np.array([]), np.array([]), np.array([]), []
    
        i = 0
           
        for eachDAI in detections:
            if eachDAI["name"] == "DAI":
                eachDAI["name"] = "DAI {0}".format(i)
                x,y,w,h = eachDAI["box_points"]
                #x,y,w,h = scale(x,y,w,h)
                cropImg = inputImg[y : h, x : w] 
                cropImg = cv.resize(cropImg, (320, 320))
                
                current_time = time.strftime("%d%m%y %H%M%S", time.localtime())
                cropPath = "res/buffer/SecCasImg/{0} {1}.jpg".format(current_time, i)
                cv.imwrite(cropPath, cropImg)
            
                Angles, detAngles = self.AngleDetector.detectObjectsFromImage(output_type='array', input_type = 'array',
                                                                              input_image = cropImg,
                                                                              minimum_percentage_probability = self.secProb)
                procIMG, a = self.secondCascade(cropImg, detAngles)
                if a == None:
                    a = 'Can not detect'
                    procIMG = Angles
                DAI = np.append(DAI, eachDAI["name"])
                DAIcoord = np.append(DAIcoord, eachDAI["box_points"])
                alpha = np.append(alpha, a)
                DAIimgSet.append(procIMG) 
                i += 1

        return detectedImage, DAI, DAIcoord, alpha, DAIimgSet

    def secondCascade(self, Angles, detAngles):
        x1, x2, x3, x4, y1, y2, y3, y4 = -1,-1,-1,-1,-1,-1,-1,-1
        cMCH, MCH, mmWS, mmCH = 0,0,0,0
        for el in detAngles:
            if el['name'] == 'cMCH' and el['percentage_probability'] > cMCH:
                cMCH = el['percentage_probability']
                x1, y1, a, b = el['box_points']
                x1, y1 = round((x1 + a)/2), round((y1 + b)/2)
            elif el['name'] == 'MCH'and el['percentage_probability'] > MCH:
                MCH = el['percentage_probability']
                x2, y2, a, b = el['box_points']
                x2, y2 = round((x2 + a)/2), round((y2 + b)/2)
            elif el['name'] == 'mmWS'and el['percentage_probability'] > mmWS:
                mmWS = el['percentage_probability']
                x3, y3, a, b = el['box_points']
                x3, y3 = round((x3 + a)/2), round((y3 + b)/2)
            elif el['name'] == 'mmCH'and el['percentage_probability'] > mmCH:
                mmCH = el['percentage_probability']
                x4, y4, a, b = el['box_points']
                x4, y4 = round((x4 + a)/2), round((y4 + b)/2)
        if x1 == -1 or x2 == -1 or x3 == -1:
            return Angles, None
            
        mathFunctions.drawLine(Angles, x1, x2, y1, y2, approx = 1)
        
        
        #drawLine(Angles, x1, x3, y1, y3)
        micronAngle = mathFunctions.cosTh(x1, x2, x3, y1, y2, y3)
        
        org = (6, 15)
        fontScale = 0.4
        thickness = 1
        
        micronAngle = round(micronAngle / 180 * 50) #angle to microns
        if micronAngle == 100:
            micronAngle = 0
        if x4 != -1:
            mathFunctions.drawLine(Angles, x3, x4, y3, y4)
            mmAngle = mathFunctions.cosTh(x3, x4, x1, y3, y4, y1)
            if micronAngle < 50 and (mmAngle - math.floor(mmAngle) >= 20):
                mmAngle = math.ceil(mmAngle / 180 * 5) #angle to mm
            else:
                mmAngle = round(mmAngle / 180 * 5) #angle to mm
            if mmAngle >= 10 or mmAngle <= 0:
                mmAngle = 0
            image = cv.putText(Angles, 'a= {0} mm'.format(round(mmAngle + micronAngle/100, 2)), org, cv.FONT_HERSHEY_SIMPLEX, 
                           fontScale, (0,0,255), thickness, cv.LINE_AA)
            return image, mmAngle + micronAngle/100
        else:
            if micronAngle >= 10:
                image = cv.putText(Angles, 'a=?.{0} mm'.format(micronAngle), org, cv.FONT_HERSHEY_SIMPLEX, 
                           fontScale, (0,0,255), thickness, cv.LINE_AA)
                return image, '?.{0}'.format(micronAngle)
            else:
                image = cv.putText(Angles, 'a=?.0{0} mm'.format(micronAngle), org, cv.FONT_HERSHEY_SIMPLEX, 
                           fontScale, (0,0,255), thickness, cv.LINE_AA)
                return image, '?.0{0}'.format(micronAngle)
        