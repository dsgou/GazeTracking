"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
import pyautogui
from collections import Counter
from gaze_tracking import GazeTracking

screenWidthLeft = 2560
screenHeightLeft = 1440
screenWidthRight = 1920
screenHeightRight = 1080
state_length = 100
history_length = 20

def move_mouse(state, time_since_move, minimum_delay=10):
    if time_since_move > minimum_delay:
        if state in ['right', 'center'] and pyautogui.position()[0] < screenWidthLeft:
            pyautogui.moveTo(screenWidthLeft + screenWidthRight / 2, screenHeightRight / 2)
            pyautogui.click()
            time_since_move = 0
        elif state == 'left' and pyautogui.position()[0] > screenWidthRight:
            pyautogui.moveTo(screenWidthLeft / 2, screenHeightLeft / 2)
            pyautogui.click()
            time_since_move = 0
    else:
        time_since_move += 1
    return time_since_move

def calculate_majority(previous_states, state, history_length=10):
    previous_states_majority = state
    if len(previous_states) > history_length:
        previous_states_majority = Counter(previous_states[-history_length:]).most_common(1)[0][0]
    return previous_states_majority


if __name__ == '__main__':
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)
    screenWidth, screenHeight = pyautogui.size()
    print(screenWidth, screenHeight)

    previous_states = []
    time_since_move = 0
    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""
        state = ""
        if gaze.is_blinking():
            text = "Blinking"
        elif gaze.is_right():
            text = "Looking right"
            state = "right"
            if pyautogui.position()[0] < screenWidthLeft:
                pyautogui.moveTo(screenWidthLeft + screenWidthRight/2, screenHeightRight/2)
                pyautogui.click()
        elif gaze.is_left():
            text = "Looking left"
            state = "left"
        elif gaze.is_right() or gaze.is_center():
            text = "Looking center"
            state = "center"

        majority = calculate_majority(previous_states, state)
        time_since_move = move_mouse(majority, time_since_move)

        if len(previous_states) > state_length:
            previous_states.pop(0)
        if state:
            print(state)
            previous_states.append(state)
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        cv2.imshow("Demo", frame)

        if cv2.waitKey(1) == 27:
            break

    webcam.release()
    cv2.destroyAllWindows()
