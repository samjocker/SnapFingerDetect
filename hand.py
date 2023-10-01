import cv2
import mediapipe as mp
import time
import math

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
handLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=3)
handConStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=3)
pTime = 0
cTime = 0
sTime_snap = 0
sTime_ninja = 0
eTime_snap = 0
eTime_ninja = 0
state_snap = True
state_ninja = True
state_check_ninja = True
point_color = (50, 134, 255)


def snap_fingers(pt4, pt8, pt12, pt14, pt16, pt18):
    global state_snap, sTime_snap, eTime_snap, point_color
    standard_x = math.dist(pt14, pt18)
    P4toP8 = math.dist(pt4, pt8)
    P8toP12 = math.dist(pt8, pt12)
    P12toP16 = math.dist(pt12, pt16)
    if P4toP8 < standard_x*0.7 and P8toP12 < standard_x*0.7 and P12toP16 > standard_x*4.2:
        sTime_snap = time.time()
        state_snap = False
    elif P12toP16 <= standard_x and state_snap == False:
        eTime_snap = time.time()
        if eTime_snap-sTime_snap <= 0.3:
            state_snap = True
            point_color = (168, 110, 82)
            print("snap")
            print("///////////")
            return "snap"
        elif P12toP16 >= standard_x:
            point_color = (50, 134, 255)
            eTime_snap = time.time()
            if eTime_snap-sTime_snap >= 0.5:
                state_snap = True
        #print("get")
        #print("Got")
    #data = "dtp:",int(P14toP18*1000),"dst1:",int(P12toP16*1000),"dst2:",int(P8toP12*1000)
    #print(data)


def ninja_gesture(pt4, pt7, pt8, pt11, pt12, pt14, pt16, pt18):
    global state_ninja, state_check_ninja,point_color, sTime_ninja, eTime_ninja
    standard_x = math.dist(pt14, pt18)
    standard_y = math.dist(pt14, pt16)
    P12toP8 = math.dist(pt12, pt8)
    P12toP16 = math.dist(pt12, pt16)
    data = "P12toP8/x=",P12toP8/standard_x,"P12toP16/y=",P12toP16/standard_y
    #print(data)
    if P12toP8 < standard_x*1.1 and P12toP16 > standard_y*2.35 and state_ninja == True:
        state_ninja = False
        sTime_ninja = time.time()
        print("ninja")
        print("------")
        point_color = (93, 179, 240)
        return True
    elif P12toP8 >= standard_x*1.1 or P12toP16 <= standard_y*2.35:
        sTime_ninja = 0
        if state_ninja == False:
            state_ninja = True
            point_color = (50, 134, 255)
            return False
    eTime_ninja = time.time()
    if eTime_ninja - sTime_ninja >= 2 and sTime_ninja != 0 and state_check_ninja == True:
        state_check_ninja = False
        print("check ninja hand")
    elif eTime_ninja - sTime_ninja <= 2 and sTime_ninja != 0 and state_check_ninja == False:
        state_check_ninja = True


while True:
    ret, img = cap.read()
    if ret:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)

        imgHeight = img.shape[0]
        imgWidth = img.shape[1]

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle)
                for i, lm in enumerate(handLms.landmark):
                    if i == 4:
                        p4 = [lm.x, lm.y]
                    elif i == 7:
                        p7 = [lm.x, lm.y]
                    elif i == 8:
                        p8 = [lm.x, lm.y]
                    elif i == 9:
                        p9 = [lm.x, lm.y]
                    elif i == 11:
                        p11 = [lm.x, lm.y]
                    elif i == 12:
                        p12 = [lm.x, lm.y]
                    elif i == 16:
                        p16 = [lm.x, lm.y]
                    elif i == 14:
                        p14 = [lm.x, lm.y]
                    elif i == 18:
                        p18 = [lm.x, lm.y]
                        snap_fingers(p4, p8, p12, p14, p16, p18)
                        #ninja_gesture(p4, p7, p8, p11, p12, p14, p16, p18)
                    xPos = int(lm.x*imgWidth)
                    yPos = int(lm.y*imgHeight)
                    cv2.putText(img, str(i), (xPos-25, yPos+5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                    if i == 4 or i == 8 or i== 10 or i==12 or i==14 or i == 16 or i == 18:
                        cv2.circle(img, (xPos,yPos), 10, point_color, cv2.FILLED)
                        #print(i, lm.x, lm.y)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, f"FPS : {int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        cv2.imshow('img', img)

    if cv2.waitKey(1) == 27:
        break