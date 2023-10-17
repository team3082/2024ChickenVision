import apriltag as apriltag
import cv2 as cv2
import solver
import json

class ApriltagDetector:
    def __init__(self, options: apriltag.DetectorOptions = apriltag.DetectorOptions(families="tag16h5"), decisionMargin: int = 30):
        self.options = options
        self.detector = apriltag.Detector(options)
        self.decisionMargin = decisionMargin
        self.frame = None
        self.tags = []
    
    def updateOptions(self, options: apriltag.DetectorOptions = apriltag.DetectorOptions()):
        self.options = options
        self.detector = apriltag.Detector(options)

    def updateDecisionMargin(self, decisionMargin: int):
        self.decisionMargin = decisionMargin
        
    def getLatestFrame(self, frame):
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

class ApriltagDetector2D(ApriltagDetector):
    def detectTags2D(self):
        self.tags = []
        
        # detecting tags
        tags = self.detector.detect(self.frame)

        # formatting and storing tag data
        for tag in tags:
            if tag.decision_margin >= self.decisionMargin:
                self.tags.append({"id": tag.tag_id, "decisionMargin": tag.decision_margin, "pose": [tag.center[0], tag.center[1]]})
                
    def renderTags(self,frame):
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        fontColor = (0, 0, 255)
        lineType = 2
        for tag in self.tags:
            if tag.decision_margin >= self.decisionMargin:
                tagCorners = tag.corners.astype(int)
                cv2.polylines(frame, [tagCorners], isClosed=True, color=(0, 255, 0), thickness=2)
                cv2.putText(frame, str(tag["id"]), (int(tag["pose"][0]), int(tag["pose"][1])), font, fontScale, fontColor, lineType)
        return frame
        
    def printTagData2D(self):
        print("tags: ")
        for tag in self.tags:
            if tag.decision_margin >= self.decisionMargin:
                print(f"Tag ID: {tag.tag_id}")
                print(f"Tag Center: {tag.center}")
                print(f"Decision Margin: {tag.decision_margin}")
                print("")
    
    def returnPose(self):
        return self.tags

    def update(self, labeledFrame, frame):
        self.getLatestFrame(frame)
        self.detectTags2D()
        renderedFrame = self.renderTags(labeledFrame)
        return renderedFrame

class ApriltagDetector3D(ApriltagDetector):
    def __init__(self, options: apriltag.DetectorOptions = apriltag.DetectorOptions(families="tag16h5", nthreads=4), decisionMargin: int = 30, tagSize: float = 1.0, camParams: tuple() = (765.00, 764.18, 393.72, 304.66), fov:float = 70):
        # configurations
        self.options = options
        self.detector = apriltag.Detector(options)
        self.decisionMargin = decisionMargin
        self.tagSize = tagSize
        self.camParams = camParams
        
        # {"tagData": tag, "poseRaw": poseRaw, "pose": pose}
        self.tags = []
        
        # storage for latest frame
        self.frame = None

    def setCamParams(self, camParams):
        self.camParams = camParams
    
    def detectTags3D(self):
        # empty array
        self.tags = []

        if self.detector.detect(self.frame, return_image=True) != []:
            tags, dimg = self.detector.detect(self.frame, return_image=True)
            
            for tag in tags:
                # gets the raw position data matrix, then converts it to x, y, z
                poseRaw, e0, e1 = self.detector.detection_pose(tag, self.camParams, self.tagSize)
                pose, matrices = self.solver.solve(poseRaw)
                
                # adds the tag data if the decision margin is high enough
                if tag.decision_margin >= self.decisionMargin:
                    self.tags.append({"tagData": tag, "poseRaw": poseRaw, "pose": pose})
                    
    def renderTags3D(self, frame):
        for tag in self.tags:
            poseRaw = tag["poseRaw"]
            apriltag._draw_pose(frame,
                               self.camParams,
                               self.tagSize,
                               poseRaw)
        return frame

    def printTagData3D(self):
        for tag in self.tags:
            
            id = tag["tag"].tag_id
            pose = tag["pose"]
            
            print(f"ID: {id}")
            print("")
            print(f"Pose: {pose}")
            
    def returnTags3D(self):
        tagData = []
        
        # formatting tag data for NT
        for tag in self.tags:
            id = tag["tagData"].tag_id
            decisionMargin = tag["tagData"].decision_margin
            pose = tag["pose"]
            tagData.append({"id": id, "decisionMargin": decisionMargin, "pose": pose})
            
        return tagData
    
    def update(self, labeledFrame, frame):
        self.getLatestFrame(frame)
        self.detectTags3D()
        if self.tags != []:
            labeledFrame = self.renderTags3D(labeledFrame)
        return labeledFrame