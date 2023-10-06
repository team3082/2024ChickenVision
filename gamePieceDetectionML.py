import cv2
import numpy as np
import time
import random
np.random.seed(20)
class GamePieceDetectionML:
    def __init__(self, configPath, modelPath, classesPath):
        
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath

        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(320,320)
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5,127.5,127.5))
        self.net.setInputSwapRB(True)
        
        self.readClasses()
    
    def readClasses(self):
        print("run")
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()
        self.classesList.insert(0,"__Background__")
        self.colorList = np.random.uniform(low=0, high=255, size=(len(self.classesList),3))
    
    
    def captureVideo(self,frame):
       classLabelIDs, conficences, bboxs = self.net.detect(frame, confThreshold = 0.5)
       
       bboxs = list(bboxs)
       conficences = list(np.array(conficences).reshape(1,-1)[0])
       conficences = list(map(float, conficences))
       
       bboxIdx = cv2.dnn.NMSBoxes(bboxs, conficences, score_threshold=0.5, nms_threshold= 0.2)
       
       if len(bboxIdx) != 0:
           for i in range(0,len(bboxIdx)):
               bbox = bboxs[np.squeeze(bboxIdx[i])]
               classConfidence = conficences[np.squeeze(bboxIdx[i])]
               classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
               classLabel = self.classesList[classLabelID]
               classColor = [int(c) for c in self.colorList[classLabelID]]
               imageLabel = "{}:{:.4f}".format(classLabel, classConfidence)
               
               x,y,w,h = bbox
               
               cv2.rectangle(frame,(x,y),(x+w,y+h), color=classColor, thickness=1)
               cv2.putText(frame, imageLabel,(x,y-10), cv2.FONT_HERSHEY_PLAIN, 3, classColor, 2)
               
               
       