import streamlit as st
import cv2
import mediapipe as mp
import HandTrackingModule as htm
import pyautogui
import time
import numpy as np
st.title("Virtual Mouse")
st.write("use your index finger to move mouse pointer note: other than thumb all should be down")
st.write("Single Click: use your index and middle finger as a click")
st.write("Right click: use your index and pinky finger make a yo sign to do right click")
st.write("Double click: only thumb should stick out and make your index finger down to do double click")
st.write("If your all fingers are out it will stop there")
st.write("To stop the app make a Fist")


# Constants
camera_width, camera_height = 640, 480
frame_reduction = 100
smoothing_factor = 7

# Set up camera
cap = cv2.VideoCapture(0)
cap.set(3, camera_width)
cap.set(4, camera_height)

# Set up hand detector
detector = htm.handDetector(maxHands=1, detectionCon=0.8)

# Get screen size
screen_width, screen_height = pyautogui.size()

# App state
app_running = False

def run_app():
    pTime=0
    global app_running
    plocx, plocy = 0, 0
    clocx, clocy = 0, 0
    while app_running:
        # 1. Find hand landmarks
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)

        # 2. Get the tip of the index and middle fingers
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            xt, yt = lmList[4][1:]

            # 3. Check which fingers are up
            fingers = detector.fingersUp()

            cv2.rectangle(img, (frame_reduction, frame_reduction), (camera_width - frame_reduction, camera_height - frame_reduction), (255, 0, 255), 2)

            # 4. Only Index Finger : moving mode
            if fingers[1] == 1 and fingers[2] == 0:
                # 5. Convert Coordinates
                x3 = np.interp(x1, (frame_reduction, camera_width - frame_reduction), (0, screen_width))
                y3 = np.interp(y1, (frame_reduction, camera_height - frame_reduction), (0, screen_height))

                # 6. Smoothen Value
                clocx = plocx + (x3 - plocx) / smoothing_factor
                clocy = plocy + (y3 - plocy) / smoothing_factor

                # 7. Move Mouse
                pyautogui.moveTo(screen_width - clocx, clocy)
                cv2.circle(img, (x1, y1), 15, (255, 255, 255), cv2.FILLED)
                plocx, plocy = clocx, clocy
            # 8. Both Index and middle fingers are up: Clicking mode
            if fingers[1] == 1 and fingers[2] == 1:
                # 9. Find Distance between fingers
                length, img, lineInfo = detector.findDistance(8, 12, img)
                # print(length)
                # 10. Click mouse if distance short
                time.sleep(0.25)
                if length < 30:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    time.sleep(0.5)
                    pyautogui.click()

            # 11. Right click
            if fingers[4] == 1 and fingers[1] == 1 and fingers[3] == 0 and fingers[2] == 0:
                time.sleep(0.5)
                pyautogui.click(button="right")

            # 12. Double Click
            if fingers[1] == 0 and fingers[0] == 1 and fingers[2] == 0:
                time.sleep(0.5)
                pyautogui.doubleClick()
            if fingers[0]==0 and fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
                break
        # 13. Frame Rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)

        # 14. Display
        # cv2.imshow("Hand Tracking", img)
        # cv2.waitKey(1)

        if app_running==False:
            break

    # 15. Release resources
    cap.release()
    cv2.destroyAllWindows()


if st.button("Virtual Mouse"):
    app_running = True
    run_app()
#
# else:
#     st.write("Click the button above to activate the app.")

# import streamlit as st
# import cv2
# import numpy as np
# import mediapipe as mp
# # import time
# import sys
# import HandTrackingModule as htm
# import time
# import pyautogui
#
#
#
#
# st.title("My Streamlit App")
# # Add your app code here
# ############################
# wCam, hCam = 640, 480
# frameR = 100  # frame reduction
# smoothening = 7
# y_scroll_amount = 1
# x_scroll_amount = 1
# scroll_amount = 0.25
# ############################
# run_app=False
#
# cap = cv2.VideoCapture(0)
# cap.set(3, wCam)
# cap.set(4, hCam)
# detector = htm.handDetector(maxHands=1, detectionCon=0.8)
# wScr, hScr = pyautogui.size()
# # print(wScr,hScr)
# def my_app():
#     # run_app= True
#     pTime = 0
#     plocx, plocy = 0, 0
#     clocx, clocy = 0, 0
#     while run_app==True:
#         # 1. find hand Landmarks
#
#         success, img = cap.read()
#         img = detector.findHands(img)
#         lmList, bbox = detector.findPosition(img)
#
#         # 2. Get the tip of the index and middle fingers
#
#         if len(lmList) != 0:
#             x1, y1 = lmList[8][1:]
#             x2, y2 = lmList[12][1:]
#             xt, yt = lmList[4][1:]
#             # print(x1,y1,x2,y2,xt,yt)
#             # 3. Check which fingers are up
#             fingers = detector.fingersUp()
#             # print(fingers)
#             cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
#             # 4. Only Index Finger : moving mode
#             if fingers[1] == 1 and fingers[2] == 0:
#                 # 5. Convert Coordinates
#                 x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
#                 y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
#
#                 # 6. Smoothen Value
#                 clocx = plocx + (x3 - plocx) / smoothening
#                 clocy = plocy + (y3 - plocy) / smoothening
#
#                 # 7. Move Mouse
#                 pyautogui.moveTo(wScr - clocx, clocy)
#                 cv2.circle(img, (x1, y1), 15, (255, 255, 255), cv2.FILLED)
#                 plocx, plocy = clocx, clocy
#             # 8. Both Index and middle fingres are up: Clicking mode
#             if fingers[1] == 1 and fingers[2] == 1:
#                 # 9. Find Distance between fingures
#                 length, img, lineInfo = detector.findDistance(8, 12, img)
#                 # print(length)
#                 # 10. Click mouse if distance short
#                 time.sleep(0.25)
#                 if length < 30:
#                     cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
#                     time.sleep(0.5)
#                     pyautogui.click()
#
#
#             # 9. right click
#             if fingers[4] == 1 and fingers[1] == 1 and fingers[3] == 0 and fingers[2] == 0:
#                 time.sleep(0.5)
#                 pyautogui.click(button="right")
#             # Double Click
#             if fingers[1] == 0 and fingers[0] == 1 and fingers[2] == 0:
#                 time.sleep(0.5)
#                 pyautogui.doubleClick()
#
#
#         # 11. Frame Rate
#         cTime = time.time()
#         fps = 1 / (cTime - pTime)
#         pTime = cTime
#         cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 5)
#         # 12. Display
#         # cv2.imshow("image", img)
#         # cv2.waitKey(1)
#         # if cv2.waitKey(10) & 0xFF == ord('q'):
#         #     break
#         # if st.button("STOP"):
#         #     cap.release()
#         #     cv2.destroyAllWindows()
#
# # Toggle button to activate/deactivate the app
# if st.button("Activate App"):
#     run_app= True
#     my_app()
# if st.button('Stop Application'):
#     run_app=False
#     cap.release()
#     cv2.destroyAllWindows()
# else:
#     st.write("Click the button above to activate the app.")
