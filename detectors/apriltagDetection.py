import apriltag as apriltag
import cv2 as cv2

class ApriltagDetector:
    def __init__(self, options: apriltag.DetectorOptions = apriltag.DetectorOptions(families="tag16h5"), decisionMargin: int = 30):
        self.options = options
        self.detector = apriltag.Detector(options)
        self.decisionMargin = decisionMargin
        self.frame = None
        self.tags = None
    
    def updateOptions(self, options: apriltag.DetectorOptions = apriltag.DetectorOptions()):
        self.options = options
        self.detector = apriltag.Detector(options)

    def updateDecisionMargin(self, decisionMargin: int):
        self.decisionMargin = decisionMargin
        
    def getLatestFrame(self, frame):
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

class ApriltagDetector2D(ApriltagDetector):
    def detectTags2D(self):
        self.tags = self.detector.detect(self.frame)
        
    def printTagData2D(self):
        print("tags: ")
        for tag in self.tags:
            if tag.decision_margin >= self.decisionMargin:
                print(f"Tag ID: {tag.tag_id}")
                print(f"Tag Center: {tag.center}")
                print(f"Decision Margin: {tag.decision_margin}")
                print("")

    def renderTags(self,frame):
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        fontColor = (0, 0, 255)
        lineType = 2
        for tag in self.tags:
            if tag.decision_margin >= self.decisionMargin:
                tagCorners = tag.corners.astype(int)
                cv2.polylines(frame, [tagCorners], isClosed=True, color=(0, 255, 0), thickness=2)
                cv2.putText(frame, str(tag.tag_id), (int(tag.center[0]), int(tag.center[1])), font, fontScale, fontColor, lineType)
        return frame

    def update(self, labeledFrame, frame):
        self.getLatestFrame(frame)
        self.detectTags2D()
        renderedFrame = self.renderTags(labeledFrame)
        return renderedFrame

class ApriltagDetector3D(ApriltagDetector):
    def __init__(self, options: apriltag.DetectorOptions = apriltag.DetectorOptions(families="tag16h5", nthreads=4), decisionMargin: int = 30, tagSize: float = 1.0, camParams: tuple() = (765.00, 764.18, 393.72, 304.66)):
        self.options = options
        self.detector = apriltag.Detector(options)
        self.decisionMargin = decisionMargin
        self.frame = None
        # [tags[], poses[], initError[], finalError[]]
        self.tags = [None, [], [], []]
        self.camParams = camParams
        self.tagSize = tagSize

    def setCamParams(self, camParams):
        self.camParams = camParams

    def detectTags3D(self):
        self.tags = [None, [], [], []]

        if self.detector.detect(self.frame, return_image=True) != []:
            self.tags[0], dimg = self.detector.detect(self.frame, return_image=True)
            for i, tag in enumerate(self.tags[0]):
                pose, e0, e1 = self.detector.detection_pose(tag, self.camParams, self.tagSize)
                self.tags[1].append(pose)
                self.tags[2].append(e0)
                self.tags[3].append(e1)

    def printTagData3D(self):
        for i in range(len(self.tags[0])):
            print(f"pose data: {self.tags[1][i]}")
            print(f"tag id: {self.tags[0][i].tag_id}")
            print(f"decision margin: {self.tags[0][i].decision_margin}")
            print("")

    def renderTags3D(self, frame):
        for pose in self.tags[1]:
            apriltag._draw_pose(frame,
                               self.camParams,
                               self.tagSize,
                               pose)
        return frame
    
    def update(self, labeledFrame, frame):
        self.getLatestFrame(frame)
        self.detectTags3D()
        if self.tags[1] != []:
            labeledFrame = self.renderTags3D(labeledFrame)
            # self.printTagData3D()
        return labeledFrame