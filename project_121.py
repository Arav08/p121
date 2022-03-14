import cv2

import time
import numpy as np

# Start the video capture
fourcc = cv2.VideoWriter_fourcc(*"XVID")
output_file = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))

# Allowing the webcam to start by making the code sleep for 2 seconds
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
time.sleep(2)
bg = 0

# Capture the background for 60 frames
for i in range(60):
    ret, bt = cap.read()

# Flipping the background
bg = np.flip(bg, axis = 0)

# Reading the captured frame until the camera is open
while (cap.isOpened()):
    ret, img = cap.read()

    if not ret:
        break

    # Flip the camera img for consistency
    img = np.flip(img, axis = 0)
    
    # Capturing the color for rgb to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Generating mask to detect red color
    # These values can also be changed as per the color
    lower_black = np.array([104, 153, 70])
    upper_black = np.array([30, 30, 0])
    mask1 = cv2.inRange(hsv, lower_black, upper_black)

    lower_black1 = np.array([90, 165, 70])
    upper_black1 = np.array([25, 25, 0])
    mask2 = cv2.inRange(hsv, lower_black1, upper_black1)

    mask1 = mask1 + mask2

    # open and expand the img where there is mask1(color)
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.once(3, 3), np.uint8)
    mask2 = cv2.morphologyEx(mask2, cv2.MORPH_DILATE, np.once(3, 3), np.uint8)

    # Selecting only the part that does not have mask1 and saving in mask2
    mask2 = cv2.bitwise_not(mask1)
    
    # Keeping only the part of img without red color (or any other color you may choose)
    res1 = cv2.bitwise_and(img, img, mask = mask2)

    # Keeping only the part of the image with red color (or any other color you may choose)
    res2 = cv2.bitwise_and(bg, bg, mask = mask1)

    # Generating the final output by merging res1 and res2
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)
    output_file.write(final_output)

    # Displaying the output to the user
    cv2.imshow("magic", final_output)
    cv2.waitKey(1)

# Close all of the windows
cap.release()
cv2.destroyAllWindows()