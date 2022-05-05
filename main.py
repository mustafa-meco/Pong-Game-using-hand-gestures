import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Importing all images
imgBackground = cv2.imread('Resources/Background.png')
imgGameOver = cv2.imread('Resources/gameOver.png')
imgBall = cv2.imread('Resources/ball.png', cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread('Resources/bat1.png', cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread('Resources/bat2.png', cv2.IMREAD_UNCHANGED)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)

    # Find the hand and its landmarks
    hands, img = detector.findHands(img, flipType=False)  # with draw




    # Overlaying the background image
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

    # Check for hands
    if hands:
        for hand in hands:
            x, y, w, h = hand["bbox"]
            h1, w1, _ = imgBat1.shape
            y1 = y - h1/2
            print(y1)

            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgBat1, (59,int(y1)))




    # Draw the ball
    img = cvzone.overlayPNG(img, imgBall, (100,100))


    cv2.imshow("Image", img)
    cv2.waitKey(1)



