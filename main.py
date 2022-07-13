import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

from utils import *








cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Importing all images
imgBackground = cv2.imread('Resources/Background.png')
imgGameOver = cv2.imread('Resources/gameOver.png')
imgGameStart = cv2.imread('Resources/gameStart.png')
imgBall = cv2.imread('Resources/ball.png', cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread('Resources/bat1.png', cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread('Resources/bat2.png', cv2.IMREAD_UNCHANGED)
capSinglePlayer = cv2.VideoCapture('Resources/singlePlayer.gif')
capTwoPlayers = cv2.VideoCapture('Resources/Two Players.gif')
capSinglePlayerHover = cv2.VideoCapture('Resources/SinglePlayerHover.gif')
capTwoPlayersHover = cv2.VideoCapture('Resources/TwoPlayersHover.gif')

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Variables
ballPos = [100, 100]
speedX = 15
speedY = 15
gameOver = False
score = [0, 0]

gameStart=True
solo = True

while True:
    _, img = cap.read()

    img = cv2.flip(img, 1)
    imgRaw = img.copy()



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
            y1 = np.clip(y1, 20, 415)

            if solo:
                if hand['type'] == "Left":
                    img = cvzone.overlayPNG(img, imgBat1, (59,int(y1)))
                    if 59 < ballPos[0] < 59 +w1 and y1< ballPos[1] < y1+h1:
                        speedX = -speedX
                        ballPos[0] += 30
                        score[0] += 1

                if hand['type'] == "Right":
                    img = cvzone.overlayPNG(img, imgBat2, (1195, int(y1)))
                    if 1195-50 < ballPos[0] < 1195 and y1< ballPos[1] < y1+h1:
                        # if y1+h1-ballPos[1] < h1/3:
                        #     ballPos[1] += 15
                        #     speedY = abs(speedY) * 1.1
                        # if y1 + h1 - ballPos[1] > h1 * 2/3:

                            # speedY = -abs(speedY) * 1.1
                        # ballPos[1] -= 15
                        # speedY = -speedY
                        speedX = -speedX
                        ballPos[0] -= 30
                        score[1] += 1
            else:
                if hand['type'] == "Right":
                    img = cvzone.overlayPNG(img, imgBat1, (59, int(y1)))
                    if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                        speedX = -speedX
                        ballPos[0] += 30

                if hand['type'] == "Left":
                    img = cvzone.overlayPNG(img, imgBat2, (1195, int(y1)))
                    if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                        speedX = -speedX
                        ballPos[0] -= 30



    # Game Over
    if solo:
        if ballPos[0]<40 or ballPos[0] > 1200:
            gameOver = True
    else:
        if ballPos[0] < 40:
            score[1] += 1
        elif ballPos[0] > 1200:
            score[0] += 1
        if ballPos[0] < 40 or ballPos[0] > 1200:
            ballPos = [100, 100]
            speedX = 15
            speedY = 15
        if max(score) == 5:
            gameOver = True


    if gameOver and solo:
        img = imgGameOver
        cv2.putText(img, str(score[0]+score[1]).zfill(2), (585,360), cv2.FONT_HERSHEY_COMPLEX,
                    2.5, (200,0,200), 5)
    elif gameOver:
        img = imgGameOver
        cv2.putText(img, str(score[0]) + ":" + str(score[1]), (585, 360), cv2.FONT_HERSHEY_COMPLEX,
                    2.5, (200, 0, 200), 5)

    elif gameStart:
        img = imgGameStart

    # if game not over move the ball
    else:

        # Move the Ball
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY


        ballPos[0] += speedX
        ballPos[1] += speedY


        # Draw the ball
        img = cvzone.overlayPNG(img, imgBall, ballPos)

        cv2.putText(img, str(score[0]), (300,650), cv2.FONT_HERSHEY_COMPLEX, 3, (255,255,255), 5)
        cv2.putText(img, str(score[1]), (900,650), cv2.FONT_HERSHEY_COMPLEX, 3, (255,255,255), 5)

    img[580:700, 20:233] = cv2.resize(imgRaw, (213,120))

    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('r'):
        ballPos = [100, 100]
        speedX = 15
        speedY = 15
        gameOver = False
        score = [0, 0]
        imgGameOver = cv2.imread('Resources/gameOver.png')
        gameStart = True
    elif key == ord('1') and gameStart :
        solo = True
        gameStart = False
        displayGif(capSinglePlayer)
    elif key == ord('2') and gameStart:
        solo = False
        gameStart = False
        displayGif(capTwoPlayers)
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()





