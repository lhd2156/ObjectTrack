# Louis Do
# 1002072156
# Windows 11
# Python 3.11.3
import sys
import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog
from PySide6.QtGui import QPixmap, QImage
from motion_detection import detectMotion
from kalman_filter import kalmanfilter

# class Tracker will track multiple objects that're moving using kalm filter and update per frame
class Tracker:
    def __init__(self, alpha=10, delta=50, maxCount=20):
        self.alpha = alpha
        self.delta = delta
        self.maxCount = maxCount
        self.objects = []
        self.ages = []

    # the update function keeps track of any new detection per frame
    def update(self, boxs):
        match = set()

        for x1, y1, x2, y2 in boxs:
            cordX = (x1 + x2) // 2
            cordY = (y1 + y2) // 2
            seen = False
            for i, obj in enumerate(self.objects):
                preX, preY = obj.predict()
                dist = np.linalg.norm([cordX - preX, cordY - preY])
                if dist < self.delta:
                    obj.update((cordX, cordY))
                    self.ages[i] = 0
                    match.add(i)
                    seen = True
                    break

            if not seen and len(self.objects) < self.maxCount:
                self.objects.append(kalmanfilter(cordX, cordY))
                self.ages.append(0)

        for i in range(len(self.ages)):
            if i not in match:
                self.ages[i] += 1

        self.objects = [o for i, o in enumerate(self.objects) if self.ages[i] < self.alpha]
        self.ages = [a for a in self.ages if a < self.alpha]

# class VideoApp will load the video provided, use the motion detection to actually keep track of objects through each frame
class VideoApp(QWidget):
    # the init is used to construct our entire gui to run the program
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Track Object")
        self.vidPath = None
        self.label = QLabel("Load a video to begin.")
        self.btnLoad = QPushButton("Load Video")
        self.btnBack = QPushButton("< Back")
        self.btnNext = QPushButton("Next Frame")
        self.btnBack60 = QPushButton("<< Back 60")
        self.btnNext60 = QPushButton("Forward 60 >>")
        self.btnReset = QPushButton("Reset")
        layout = QVBoxLayout()
        row = QHBoxLayout()
        for btn in [self.btnLoad, self.btnBack, self.btnNext, self.btnBack60, self.btnNext60, self.btnReset]:
            row.addWidget(btn)
        layout.addWidget(self.label)
        layout.addLayout(row)
        self.setLayout(layout)
        self.btnLoad.clicked.connect(self.loadVideo)
        self.btnBack.clicked.connect(lambda: self.jump(-1))
        self.btnNext.clicked.connect(self.nextFrame)
        self.btnReset.clicked.connect(self.resetTracker)
        self.btnBack60.clicked.connect(lambda: self.jump(-60))
        self.btnNext60.clicked.connect(lambda: self.jump(60))
        self.cap = None
        self.frames = []
        self.frameId = 2
        self.tracker = Tracker()

    # loadVideo will open the file when prompted to then store all of the frames needed
    def loadVideo(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi)")
        if file:
            self.vidPath = file
            self.cap = cv2.VideoCapture(file)
            self.frames = []
            while True:
                render, frame = self.cap.read()
                if not render:
                    break
                self.frames.append(frame)
            self.frameId = 2
            self.resetTracker()
            self.renderFrame(self.frameId)

    # the resetTracker will be clearing the tracker for the CURRENT given frame
    def resetTracker(self):
        self.tracker = Tracker()
        if self.frameId < len(self.frames):
            frame = self.frames[self.frameId]
            img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_BGR888)
            self.label.setPixmap(QPixmap.fromImage(img))

    # the jump function just moves the frame index with the provided amount + keeps tracking
    def jump(self, amount):
        self.frameId = max(2, min(self.frameId + amount, len(self.frames) - 1))
        self.resetTracker()
        for i in range(2, self.frameId + 1):
            self.processFrame(i, dry=True)
        self.renderFrame(self.frameId)

    # the nextFrame process allows to go to the next frame
    def nextFrame(self):
        if not self.cap or self.frameId >= len(self.frames):
            self.label.setText("End of video reached.")
            return
        self.processFrame(self.frameId)
        self.renderFrame(self.frameId)
        self.frameId += 1

    # the processFrame begins to run the motion detection while updating tracker
    def processFrame(self, index, dry=False):
        if index < 2:
            return
        f1 = cv2.cvtColor(self.frames[index - 2], cv2.COLOR_BGR2GRAY)
        f2 = cv2.cvtColor(self.frames[index - 1], cv2.COLOR_BGR2GRAY)
        f3 = cv2.cvtColor(self.frames[index], cv2.COLOR_BGR2GRAY)
        _, boxs = detectMotion(f1, f2, f3)
        self.tracker.update(boxs)

    # the renderFrame will display/load tracking results on the current frame
    def renderFrame(self, index):
        frame = self.frames[index].copy()
        for obj in self.tracker.objects:
            x, y = map(int, obj.predict())
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            for hx, hy in obj.history:
                cv2.circle(frame, (int(hx), int(hy)), 2, (255, 0, 0), -1)
        img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_BGR888)
        self.label.setPixmap(QPixmap.fromImage(img))

# Run our gui here
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = VideoApp()
    gui.resize(950, 700)
    gui.show()
    sys.exit(app.exec())