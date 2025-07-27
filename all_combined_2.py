import cv2
import time

import cvzone
import numpy as np
import mediapipe as mp
import handTrackingModule as htm
import math
import serial
from cvzone.SerialModule import SerialObject


def main():
    pTime = 0
    cTime = 0
    wCam, hCam = 800, 600
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    detector = htm.handDetector(detectionCon=0.75)

    arduinoData = SerialObject('COM3')  # COM4

    thumb = 0
    index = 0
    middle = 0
    ring = 0
    little = 0
    length = 0
    leftHandList = []
    rightHandList = []
    left_hand_assigned = False
    right_hand_assigned = False
    choose = 0
    whichType = 0
    data_array = [0, 0, 0, 0, 0, 0, 0, 0]

    forward = 0
    backward = 0
    right = 0
    left = 0
    rightforw = 0
    leftforw = 0

    lenBarG = 0
    lenBarJ = 0

    #data_array[6] is a type pointer
    #data_array[5] is extra byte for type 2

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img, draw=True)
        leftHandList, leftbbox = detector.findPosition(img, handNo=0, draw1=True)
        rightHandList, rightbbox = detector.findPosition(img, handNo=1, draw1=True)

        if len(leftHandList) != 0 and len(rightHandList) != 0 and (not left_hand_assigned or not right_hand_assigned):

            left_avg_y = sum(landmark[2] for landmark in leftHandList) / len(leftHandList)
            right_avg_y = sum(landmark[2] for landmark in rightHandList) / len(rightHandList)

            if left_avg_y > right_avg_y and not left_hand_assigned:
                leftHandList, rightHandList = rightHandList, leftHandList
                left_hand_assigned = True

            elif left_avg_y >= right_avg_y and not right_hand_assigned:
                right_hand_assigned = True


        cv2.circle(img, (40, 80), 20, (0, 0, 0), cv2.FILLED)
        cv2.circle(img, (50, 80), 20, (0, 0, 0), cv2.FILLED)
        cv2.circle(img, (60, 80), 20, (0, 0, 0), cv2.FILLED)
        cv2.circle(img, (70, 80), 20, (0, 0, 0), cv2.FILLED)
        cv2.circle(img, (80, 80), 20, (0, 0, 0), cv2.FILLED)
        cv2.circle(img, (90, 80), 20, (0, 0, 0), cv2.FILLED)
        cv2.circle(img, (40, 80), 16, (140, 140, 145), cv2.FILLED)
        cv2.circle(img, (50, 80), 16, (140, 140, 145), cv2.FILLED)
        cv2.circle(img, (60, 80), 16, (140, 140, 145), cv2.FILLED)
        cv2.circle(img, (70, 80), 16, (140, 140, 145), cv2.FILLED)
        cv2.circle(img, (80, 80), 16, (140, 140, 145), cv2.FILLED)
        cv2.circle(img, (90, 80), 16, (140, 140, 145), cv2.FILLED)

        if whichType == 0:
            cv2.circle(img, (65, 80), 16, (0, 0, 255), cv2.FILLED)
            cvzone.putTextRect(img, f'Mode: NONE', [30, 40], scale=2, thickness=2, colorT=(255, 255, 255),
                               colorR=(0, 0, 0), offset=10)
        elif whichType == 1:
            cv2.circle(img, (40, 80), 16, (0, 255, 0), cv2.FILLED)
        elif whichType == 2:
            cv2.circle(img, (90, 80), 16, (255, 0, 0), cv2.FILLED)


        if len(rightHandList) != 0:
            if rightHandList[16][2] < rightHandList[14][2]:
                ring = 100
            else:
                ring = 200
            if rightHandList[20][2] < rightHandList[18][2]:
                little = 100
            else:
                little = 200

            if ring == 100 and little == 100:
                choose = 1
            elif ring == 200 and little == 200:
                choose = 0

            #print(choose)

            cv2.putText(img, "Right Hand", (rightbbox[0] - 20, rightbbox[1] - 30), cv2.FONT_HERSHEY_DUPLEX, 1,
                        (0, 255, 0), 1)
        if len(leftHandList) != 0:
            cv2.putText(img, "Left Hand", (leftbbox[0] - 20, leftbbox[1] - 25), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0),
                        1)
            if choose == 1:
                cvzone.putTextRect(img, f'Choose mode', [30, 40], scale=2, thickness=2, colorT=(255, 255, 255), colorR=(0, 0, 0), offset=10)
                if 30 <= leftHandList[8][1] <= 100 and 70 <= leftHandList[8][2] <= 90:
                    whichType = 1
                    #print(whichType)
                if 30 <= leftHandList[8][1] <= 100 and 70 <= leftHandList[8][2] <= 90 and 30 <= leftHandList[12][1] <= 100 and 70 <= leftHandList[12][2] <= 90:
                    whichType = 2
                    #print(whichType)
                if 30 <= leftHandList[12][1] <= 100 and 70 <= leftHandList[12][2] <= 90 and 30 <= leftHandList[16][1] <= 100 and 70 <= leftHandList[16][2] <= 90:
                    whichType = 0
                    #print(whichType)

        if choose == 0:
            cvzone.putTextRect(img, f'Mode:', [30, 40], scale=2, thickness=2, colorT=(255, 255, 255), colorR=(0, 0, 0), offset=10)
            if whichType == 1:
                cvzone.putTextRect(img, f'Mode: Gesture Control', [30, 40], scale=2, thickness=2, colorT=(255, 255, 255), colorR=(0, 0, 0), offset=10)
                if len(leftHandList) != 0:
                    cv2.putText(img, "Left Hand", (leftbbox[0] - 20, leftbbox[1] - 25), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0),
                        1)
                    x_min, y_min = leftHandList[20][1], leftHandList[12][2]
                    x_max, y_max = leftHandList[4][1], leftHandList[0][2]
                    if leftHandList[18][1] < leftHandList[20][1]:
                        x_min = leftHandList[18][1]
                    else:
                        x_min = leftHandList[20][1]
                    if leftHandList[2][1] > leftHandList[4][1]:
                        x_max = leftHandList[2][1]
                    else:
                        x_max = leftHandList[4][1]
                    '''
                    if leftHandList[10][2] < leftHandList[12][2] and leftHandList[10][2] < leftHandList[8][2] and leftHandList[10][2] < leftHandList[16][2] and leftHandList[10][2] < leftHandList[20][2]:
                        y_min = leftHandList[10][2]
                    if leftHandList[8][2] < leftHandList[12][2] and leftHandList[8][2] < leftHandList[10][2] and leftHandList[8][2] < leftHandList[16][2] and leftHandList[8][2] < leftHandList[20][2]:
                        y_min = leftHandList[8][2]
                    if leftHandList[16][2] < leftHandList[12][2] and leftHandList[16][2] < leftHandList[10][2] and leftHandList[16][2] < leftHandList[8][2] and leftHandList[16][2] < leftHandList[20][2]:
                        y_min = leftHandList[16][2]
                    if leftHandList[20][2] < leftHandList[12][2] and leftHandList[20][2] < leftHandList[10][2] and leftHandList[20][2] < leftHandList[16][2] and leftHandList[20][2] < leftHandList[8][2]:
                        y_min = leftHandList[20][2]


                    cv2.rectangle(img, (x_min - 20, y_min - 20), (x_max + 20, y_max + 20), (0, 255, 0), 2)
                    '''
                    cv2.putText(img, "Left Hand", (leftbbox[0] - 20, leftbbox[1] - 25), cv2.FONT_HERSHEY_DUPLEX, 1,
                                (0, 255, 0), 1)

                    if leftHandList[4][1] > leftHandList[2][1]:
                        thumb = 100
                    else:
                        thumb = 200
                    if leftHandList[8][2] < leftHandList[6][2]:
                        index = 100
                    else:
                        index = 200
                    if leftHandList[12][2] < leftHandList[10][2]:
                        middle = 100
                    else:
                        middle = 200
                    if leftHandList[16][2] < leftHandList[14][2]:
                        ring = 100
                    else:
                        ring = 200
                    if leftHandList[20][2] < leftHandList[18][2]:
                        little = 100
                    else:
                        little = 200

                    if thumb == 200 and index == 100 and middle == 200 and ring == 200 and little == 100:
                        cvzone.putTextRect(img, f'Forward', [30, 450], scale=3, thickness=3, colorT=(255, 255, 255), colorR=(0, 0, 0), offset=10)
                    elif thumb == 100 and index == 200 and middle == 200 and ring == 200 and little == 200:
                        cvzone.putTextRect(img, f'Backward', [30, 450], scale=3, thickness=3, colorT=(255, 255, 255), colorR=(0, 0, 0), offset=10)
                    elif thumb == 200 and index == 100 and middle == 200 and ring == 200 and little == 200:
                        cvzone.putTextRect(img, f'Turn right', [30, 450], scale=3, thickness=3, colorT=(255, 255, 255), colorR=(0, 0, 0), offset=10)
                    elif thumb == 200 and index == 200 and middle == 200 and ring == 200 and little == 100:
                        cvzone.putTextRect(img, f'Turn left', [30, 450], scale=3, thickness=3, colorT=(255, 255, 255), colorR=(0, 0, 0), offset=10)
                    elif thumb == 100 and index == 100 and middle == 200 and ring == 200 and little == 200:
                        cvzone.putTextRect(img, f'Soft turn right', [30, 450], scale=3, thickness=3, colorT=(255, 255, 255), colorR=(0, 0, 0), offset=10)
                    elif thumb == 100 and index == 200 and middle == 200 and ring == 200 and little == 100:
                        cvzone.putTextRect(img, f'Soft turn left', [30, 450], scale=3, thickness=3, colorT=(255, 255, 255), colorR=(0, 0, 0), offset=10)
                    elif (thumb == 100 and index == 100 and middle == 100 and ring == 100 and little == 100) or (thumb == 200 and index == 200 and middle == 200 and ring == 200 and little == 200):
                        None
                    data_array[0] = thumb
                    data_array[1] = index
                    data_array[2] = middle
                    data_array[3] = ring
                    data_array[4] = little
                    data_array[5] = 200  # extra byte for type 2
                    data_array[6] = 100  # type pointer





                if len(rightHandList) != 0:
                    x_max, y_max = rightHandList[20][1], rightHandList[0][2]
                    x_min, y_min = rightHandList[4][1], rightHandList[12][2]
                    if rightHandList[18][1] > rightHandList[20][1]:
                        x_max = rightHandList[18][1]
                    else:
                        x_max = rightHandList[20][1]
                    if rightHandList[2][1] < rightHandList[4][1]:
                        x_min = rightHandList[2][1]
                    else:
                        x_min = rightHandList[4][1]
                    '''
                    if rightHandList[10][2] < rightHandList[12][2] and rightHandList[10][2] < rightHandList[8][2] and rightHandList[10][2] < rightHandList[16][2] and rightHandList[10][2] < rightHandList[20][2]:
                        y_min = rightHandList[10][2]
                    if rightHandList[8][2] < rightHandList[12][2] and rightHandList[8][2] < rightHandList[10][2] and rightHandList[8][2] < rightHandList[16][2] and rightHandList[8][2] < rightHandList[20][2]:
                        y_min = rightHandList[8][2]
                    if rightHandList[16][2] < rightHandList[12][2] and rightHandList[16][2] < rightHandList[10][2] and rightHandList[16][2] < rightHandList[8][2] and rightHandList[16][2] < rightHandList[20][2]:
                        y_min = rightHandList[16][2]
                    if rightHandList[20][2] < rightHandList[12][2] and rightHandList[20][2] < rightHandList[10][2] and rightHandList[20][2] < rightHandList[16][2] and rightHandList[20][2] < rightHandList[8][2]:
                        y_min = rightHandList[20][2]
                    cv2.rectangle(img, (x_min - 20, y_min - 20), (x_max + 20, y_max + 20), (0, 255, 0), 2)
                    '''
                    cv2.putText(img, "Right Hand", (rightbbox[0] - 20, rightbbox[1] - 30), cv2.FONT_HERSHEY_DUPLEX, 1,
                                (0, 255, 0), 1)

                    x1, y1 = rightHandList[4][1], rightHandList[4][2]
                    x2, y2 = rightHandList[8][1], rightHandList[8][2]

                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # center of the line
                    cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
                    cv2.circle(img, (x2, y2), 7, (255, 0, 255), cv2.FILLED)
                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

                    length = math.hypot(x2 - x1, y2 - y1)
                    lenBarG = np.interp(length, [15, 170], [350, 113])
                    length = int(length)
                    data_array[7] = length
                    if length < 30:
                        cv2.circle(img, (cx, cy), 7, (0, 0, 0), cv2.FILLED)
                    cv2.rectangle(img, (50, 110), (80, 350), (0, 0, 0), 3)
                    cv2.rectangle(img, (53, int(lenBarG)), (77, 347), (255, 255, 255), cv2.FILLED)
                    cvzone.putTextRect(img, f'Power', [20, 385], scale=2, thickness=2, colorT=(255, 255, 255), colorR=(0, 0, 0), offset=8)

                #for data in range(len(data_array)):
                #    print(f"{data_array[data]}", end=" ")
                #print("")

            if whichType == 2:
                cvzone.putTextRect(img, f'Mode: Joystick', [30, 40], scale=2, thickness=2, colorT=(255, 255, 255),
                                   colorR=(0, 0, 0), offset=10)
                if len(leftHandList) != 0:
                    x_min, y_min = leftHandList[20][1], leftHandList[12][2]
                    x_max, y_max = leftHandList[4][1], leftHandList[0][2]
                    if leftHandList[18][1] < leftHandList[20][1]:
                        x_min = leftHandList[18][1]
                    else:
                        x_min = leftHandList[20][1]
                    if leftHandList[2][1] > leftHandList[4][1]:
                        x_max = leftHandList[2][1]
                    else:
                        x_max = leftHandList[4][1]

                    cv2.putText(img, "Left Hand", (leftbbox[0] - 20, leftbbox[1] - 25), cv2.FONT_HERSHEY_DUPLEX, 1,
                                (0, 255, 0), 1)

                if len(rightHandList) != 0:

                    x_max, y_max = rightHandList[20][1], rightHandList[0][2]
                    x_min, y_min = rightHandList[4][1], rightHandList[12][2]
                    if rightHandList[18][1] > rightHandList[20][1]:
                        x_max = rightHandList[18][1]
                    else:
                        x_max = rightHandList[20][1]
                    if rightHandList[2][1] < rightHandList[4][1]:
                        x_min = rightHandList[2][1]
                    else:
                        x_min = rightHandList[4][1]

                    cv2.putText(img, "Right Hand", (rightbbox[0] - 20, rightbbox[1] - 30), cv2.FONT_HERSHEY_DUPLEX, 1,
                                (0, 255, 0), 1)

                    #cv2.circle(img, (650, 250), 7, (0, 0, 0), cv2.FILLED)
                    cv2.circle(img, (650, 250), 145, (0, 0, 0), 3)

                    x1, y1 = 650, 250
                    x2, y2 = rightHandList[8][1], rightHandList[8][2]

                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # center of the line
                    cv2.circle(img, (x1, y1), 7, (0, 0, 0), cv2.FILLED)
                    cv2.circle(img, (x2, y2), 20, (0, 0, 0), cv2.FILLED)
                    cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
                    cv2.circle(img, (cx, cy), 7, (0, 255, 0), cv2.FILLED)

                    length = math.hypot(x2 - x1, y2 - y1)
                    lenBarJ = np.interp(length, [10, 145], [350, 113])
                    length = int(length)
                    if length > 145:
                        length = 145
                    else:
                        length = length

                    if y1 - 30 < y2 < y1 + 30 and x1 - 30 < x2 < x1 + 30:
                        length = 0
                        data_array[0] = 200 # forward
                        data_array[1] = 200 # backward
                        data_array[2] = 200 # right
                        data_array[3] = 200 # left
                        data_array[4] = 200 # rightforw
                        data_array[5] = 200 # leftforw
                    else:
                        length = length
                        if y2 < y1 - 20 and x1 - 20 < x2 < x1 + 20:
                            data_array[0] = 100
                            cvzone.putTextRect(img, f'Forward', [30, 450], scale=3, thickness=3, colorT=(255, 255, 255),
                                               colorR=(0, 0, 0), offset=10)
                        else:
                            data_array[0] = 200
                        if y2 > y1 + 20 and x1 - 20 < x2 < x1 + 20:
                            data_array[1] = 100
                            cvzone.putTextRect(img, f'Backward', [30, 450], scale=3, thickness=3, colorT=(255, 255, 255),
                                               colorR=(0, 0, 0), offset=10)
                        else:
                            data_array[1] = 200
                        if x2 > x1 + 20 and y1 - 20 < y2 < y1 + 20:
                            data_array[2] = 100
                            cvzone.putTextRect(img, f'Turn right', [30, 450], scale=3, thickness=3, colorT=(255, 255, 255),
                                               colorR=(0, 0, 0), offset=10)
                        else:
                            data_array[2] = 200
                        if x2 < x1 - 20 and y1 - 20 < y2 < y1 + 20:
                            data_array[3] = 100
                            cvzone.putTextRect(img, f'Turn left', [30, 450], scale=3, thickness=3, colorT=(255, 255, 255),
                                               colorR=(0, 0, 0), offset=10)
                        else:
                            data_array[3] = 200

                        if y2 < y1 - 20 and x2 > x1 + 20:
                            data_array[4] = 100
                            cvzone.putTextRect(img, f'Turn soft right', [30, 450], scale=3, thickness=3, colorT=(255, 255, 255),
                                               colorR=(0, 0, 0), offset=10)

                        else:
                            data_array[4] = 200
                        if y2 < y1 - 20 and x2 < x1 - 20:
                            data_array[5] = 100
                            cvzone.putTextRect(img, f'Turn soft left', [30, 450], scale=3, thickness=3, colorT=(255, 255, 255),
                                               colorR=(0, 0, 0), offset=10)
                        else:
                            data_array[5] = 200

                    data_array[7] = length
                    data_array[6] = 200
                    cv2.rectangle(img, (50, 110), (80, 350), (0, 0, 0), 3)
                    cv2.rectangle(img, (53, int(lenBarJ)), (77, 347), (255, 255, 255), cv2.FILLED)
                    cvzone.putTextRect(img, f'Power', [20, 385], scale=2, thickness=2, colorT=(255, 255, 255),
                                       colorR=(0, 0, 0), offset=8)

                    if length < 30:
                        cv2.circle(img, (cx, cy), 7, (0, 0, 255), cv2.FILLED)

            for data in range(len(data_array)):
                print(f"{data_array[data]}", end=" ")
            print()

            arduinoData.sendData(data_array)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (790, 40), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 0, 0), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == "__main__":
    main()