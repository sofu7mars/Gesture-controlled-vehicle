import cv2
import time
import mediapipe as mp
import math


class handDetector():
    def __init__(self, mode=False, maxHands=2, modelC=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelC = modelC
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelC, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipsIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #imgRGB = cv2.flip(imgRGB, 1)
        self.result = self.hands.process(imgRGB)
        # print(result.multi_hand_landmarks)

        if self.result.multi_hand_landmarks:
            for handLand in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLand, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw1=True, draw2=True):
        xList = []
        yList = []
        bbox = []
        self.PosList = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.PosList.append([id, cx, cy])
                if draw1:
                    cv2.circle(img, (cx, cy), 4, (255, 255, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw2:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2)

        return self.PosList, bbox

    def fingersUp(self):
        fingers = []

        if self.PosList[self.tipsIds[0]][1] > self.PosList[self.tipsIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)


        for id in range(1, 5):
            if self.PosList[self.tipsIds[id]][2] < self.PosList[self.tipsIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.PosList[p1][1:]
        x2, y2 = self.PosList[p2][1:]

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]

def main():

    pTime = 0
    cTime = 0
    wCam, hCam = 1280, 720
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        PosList, bbox = detector.findPosition(img)

        if len(PosList) != 0:
            print(PosList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 0, 0), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == "__main__":
    main()
'''
def main():
    pTime = 0
    cTime = 0
    wCam, hCam = 1280, 720
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img, draw=True)

        left_hand_pos = detector.findPosition(img, handNo=0, draw=True)
        right_hand_pos = detector.findPosition(img, handNo=1, draw=True)

        if len(left_hand_pos) != 0:
            print("Left Hand Landmarks:", left_hand_pos[4])
        if len(right_hand_pos) != 0:
            print("Right Hand Landmarks:", right_hand_pos[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
'''