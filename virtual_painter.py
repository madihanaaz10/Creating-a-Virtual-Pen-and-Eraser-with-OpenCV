import cv2
import numpy as np
import os
from cvzone.HandTrackingModule import HandDetector

def virtual_painter():
    # 1. Setup
    current_thickness = 15 
    folderPath = "Header"

    if not os.path.exists(folderPath):
        print(f"Error: The '{folderPath}' folder was not found.")
        return

    myList = os.listdir(folderPath)
    myList.sort()
    overlayList = []
    
    header_height = 210
    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}')
        if image is not None:
            image = cv2.resize(image, (1280, header_height))
            overlayList.append(image)

    if not overlayList or len(overlayList) < 14:
        print("Error: Not enough header images found.")
        return

    header = overlayList[0]
    drawColor = (255, 0, 255)
    shape = 'freestyle'
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    cap.set(3, 1280)
    cap.set(4, 720)

    imgCanvas = np.zeros((720, 1280, 3), np.uint8)
    
    detector = HandDetector(detectionCon=0.85, maxHands=1)
    xp, yp = 0, 0

    print("Starting Advanced Virtual Painter. Press 'q' to quit.")

    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.flip(img, 1)

        hands, img = detector.findHands(img, flipType=False)

        if hands:
            hand1 = hands[0]
            lmList = hand1['lmList']

            x0, y0 = lmList[4][0], lmList[4][1]
            x1, y1 = lmList[8][0], lmList[8][1]
            x2, y2 = lmList[12][0], lmList[12][1]
            x4, y4 = lmList[20][0], lmList[20][1]

            fingers = detector.fingersUp(hand1)

            # Thickness Adjustment Gesture
            if fingers == [1, 0, 0, 0, 1]:
                length, _, img = detector.findDistance((x0, y0), (x4, y4), img)
                current_thickness = int(np.interp(length, [30, 200], [5, 100]))

            # Selection Mode
            elif fingers[1] and fingers[2]:
                xp, yp = 0, 0 
                if y1 < 120:
                    if 250 < x1 < 450: header = overlayList[0]; drawColor = (255, 0, 255)
                    elif 550 < x1 < 750: header = overlayList[1]; drawColor = (255, 0, 0)
                    elif 800 < x1 < 950: header = overlayList[10]; drawColor = (0, 255, 0)
                    elif 1050 < x1 < 1200: header = overlayList[5]; drawColor = (0, 0, 0)
                if y1 > 120 and y1 < 210:
                    if 250 < x1 < 450 and drawColor == (255, 0, 255): header = overlayList[0]; shape = 'freestyle'
                    elif 550 < x1 < 750 and drawColor == (255, 0, 255): header = overlayList[6]; shape = 'circle'
                    elif 800 < x1 < 950 and drawColor == (255, 0, 255): header = overlayList[7]; shape = 'rectangle'
                    elif 1050 < x1 < 1200 and drawColor == (255, 0, 255): header = overlayList[8]; shape = 'elipse'
                    elif 250 < x1 < 450 and drawColor == (255, 0, 0): header = overlayList[10]; shape = 'freestyle'
                    elif 550 < x1 < 750 and drawColor == (255, 0, 0): header = overlayList[11]; shape = 'circle'
                    elif 800 < x1 < 950 and drawColor == (255, 0, 0): header = overlayList[12]; shape = 'rectangle'
                    elif 1050 < x1 < 1200 and drawColor == (255, 0, 0): header = overlayList[13]; shape = 'elipse'
                    elif 250 < x1 < 450 and drawColor == (0, 255, 0): header = overlayList[1]; shape = 'freestyle'
                    elif 550 < x1 < 750 and drawColor == (0, 255, 0): header = overlayList[2]; shape = 'circle'
                    elif 800 < x1 < 950 and drawColor == (0, 255, 0): header = overlayList[3]; shape = 'rectangle'
                    elif 1050 < x1 < 1200 and drawColor == (0, 255, 0): header = overlayList[4]; shape = 'elipse'
                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

            # Drawing Mode
            elif fingers[1] and not fingers[2]:
                cv2.circle(img, (x1, y1), 15, drawColor)

                if drawColor == (0, 0, 0): # Eraser Mode
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, current_thickness)
                    xp, yp = x1, y1 # Update for continuous erasing
                else: # Drawing Modes
                    if shape == 'freestyle':
                        # --- THIS IS THE "PINCH TO DRAW" FIX ---
                        length, _, _ = detector.findDistance((x0, y0), (x1, y1))
                        # If fingers are close (pinching), then draw
                        if length < 35:
                            if xp == 0 and yp == 0:
                                xp, yp = x1, y1
                            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, current_thickness)
                        # If fingers are not close, "lift the pen" by resetting the start point
                        else:
                            xp, yp = 0, 0
                    
                    # For shapes, we don't reset xp, yp, as they are not used
                    elif shape == 'rectangle':
                        cv2.rectangle(img, (x0, y0), (x1, y1), drawColor, current_thickness)
                        if fingers[4]: cv2.rectangle(imgCanvas, (x0, y0), (x1, y1), drawColor, current_thickness)
                    elif shape == 'circle':
                        radius = int(((((x0 - x1) ** 2) + ((y0 - y1) ** 2)) ** 0.5))
                        cv2.circle(img, (x0, y0), radius, drawColor, current_thickness)
                        if fingers[4]: cv2.circle(imgCanvas, (x0, y0), radius, drawColor, current_thickness)
                    elif shape == 'elipse':
                        axis1 = abs(x1 - x0); axis2 = abs(y1 - y0)
                        cv2.ellipse(img, (x0, y0), (axis1, axis2), 0, 0, 360, drawColor, current_thickness)
                        if fingers[4]: cv2.ellipse(imgCanvas, (x0, y0), (axis1, axis2), 0, 0, 360, drawColor, current_thickness)
                
                # Update the last point ONLY if we are in freestyle mode and pinching
                if shape == 'freestyle' and 'length' in locals() and length < 35:
                    xp, yp = x1, y1

            # Clear Canvas Gesture
            elif fingers == [0, 0, 1, 1, 1]:
                imgCanvas = np.zeros((720, 1280, 3), np.uint8)

        # Merge and display
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)
        img[0:header_height, 0:1280] = header
        cv2.rectangle(img, (30, 650), (300, 700), (200, 200, 200), cv2.FILLED)
        cv2.putText(img, f'Thickness: {current_thickness}', (40, 685), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)
        cv2.imshow("Advanced Virtual Painter", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    virtual_painter()