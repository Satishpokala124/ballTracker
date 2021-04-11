import os
import cv2
import numpy as np
import imutils
from functions import *
import sys
import time

print('\nballTracker')
print('Press and hold "q" to quit he program at any time...\n')

# Selected Camera
if len(sys.argv) == 1:
	selectedCamera = 0
	print('\nUsing the default webcam...')
else:
	selectedCamera = int(sys.argv[1])
	print('\n Using camera:', selectedCamera)

time.sleep(1)

# Modes of operation
colorCalibrationMode = 1
distCalibrationMode = 2
distMeasurementMode = 3

# Initialising a mode
mode = 0

# check if the 'data.txt' file exists
if os.path.exists('data.txt'):
	# Open the file 'data.txt'
	data = open('data.txt', 'r')
	# read the color calibrated values 
	try:
		lowHue, lowSat, lowVal = map(int,data.readline().split(','))
		highHue, highSat, highVal = map(int,data.readline().split(','))
		data.close()     # close the 'data.txt' file
		l_bound = np.array([lowHue, lowSat, lowVal])
		u_bound = np.array([highHue, highSat, highVal])
		# Set the mode to 'distance calibration' or 'distance Measurement' based on user imput
		# Read mode from user
		print('\nSelect any mode by entering the corresponding number shown below:')
		print('\t"1" - Distance Calibration')
		print('\t"2" - Distance Measurement')
		while True:
			readMode = input()
			if readMode == '1':
				mode = distCalibrationMode
				break
			elif readMode == '2':
				mode = distMeasurementMode
				break
			else:
				print('\nPlease select a valid option!!')

	except :
		print('\nThe data is empty!!')
		print('Entering calibration mode automatically...')
		# Set the mode to color calibration
		mode = colorCalibrationMode

else :
	print('\nNo "data.txt" found!!')
	print('Creating a new "data.txt" file...')
	data = open('data.txt', 'x')
	data.close()
	print('\nEntering calibration mode...')
	# Set mode to color calibration
	mode = colorCalibrationMode

# Opening the camera
camera = cv2.VideoCapture(selectedCamera)

# Displaying the main menu
print('\nStarting the program...')
print('To switch between modes press the corresponding keys below')
print('\t"1" - Color Calibration')
print('\t"2" - Distance Calibration')
print('\t"3" - Distance Measurement')
print('\t"q" - Quit')

if mode == colorCalibrationMode:
	cv2.namedWindow('Tracker')
	cv2.createTrackbar('Lower Heu', 'Tracker', 0, 255, nothing)
	cv2.createTrackbar('Lower Sat', 'Tracker', 0, 255, nothing)
	cv2.createTrackbar('Lower Val', 'Tracker', 0, 255, nothing)
	cv2.createTrackbar('Upper Heu', 'Tracker', 255, 255, nothing)
	cv2.createTrackbar('Upper Sat', 'Tracker', 255, 255, nothing)
	cv2.createTrackbar('Upper Val', 'Tracker', 255, 255, nothing)
	print('\nColor Calibration Mode')
	print('Select the color range by using the Tracker window')
	print('Press "s" to save the color settings')

# The main while loop
while True:
	key = cv2.waitKey(1)
	if key == ord('q'):
		print('\nClosing all windows')
		cv2.destroyAllWindows()
		print('Releasing camera')
		camera.release()
		print('Bye')
		quit()
	elif key == ord('1'):
		print('\n"1" is pressed...')
		cv2.destroyAllWindows()
		time.sleep(1)
		cv2.namedWindow('Tracker')
		try:
			data = open('data.txt', 'r')
			lowHue, lowSat, lowVal = map(int,data.readline().split(','))
			highHue, highSat, highVal = map(int,data.readline().split(','))
			data.close()
		except :
			print('\nError while reading')
			lowHue, lowSat, lowVal = 0, 0, 0
			highHue, highSat, highVal = 255, 255, 255
		cv2.createTrackbar('Lower Heu', 'Tracker', lowHue, 255, nothing)
		cv2.createTrackbar('Lower Sat', 'Tracker', lowSat, 255, nothing)
		cv2.createTrackbar('Lower Val', 'Tracker', lowVal, 255, nothing)
		cv2.createTrackbar('Upper Heu', 'Tracker', highHue, 255, nothing)
		cv2.createTrackbar('Upper Sat', 'Tracker', highSat, 255, nothing)
		cv2.createTrackbar('Upper Val', 'Tracker', highVal, 255, nothing)
		print('\nColor Calibration Mode')
		print('Select the color range by using the Tracker window')
		print('Press "s" to save the color settings')
		mode = colorCalibrationMode
	elif key == ord('2'):
		cv2.destroyAllWindows()
		print('\n"2" is pressed...')
		print('Distance Calibration Mode')
		# Read values from "data.txt" file
		data = open('data.txt', 'r')
		lowHue, lowSat, lowVal = map(int,data.readline().split(','))
		highHue, highSat, highVal = map(int,data.readline().split(','))
		# Create numpy arrays
		l_bound = np.array([lowHue, lowSat, lowVal])
		u_bound = np.array([highHue, highSat, highVal])
		data.close()
		print('\nNote the area and radius of the ball with the help of screen window')
		time.sleep(1)
		mode = distCalibrationMode
	elif key == ord('3'):
		cv2.destroyAllWindows()
		print('\n"3" is pressed...')
		print('Distance Measurement Mode')
		data = open('data.txt', 'r')
		lowHue, lowSat, lowVal = map(int,data.readline().split(','))
		highHue, highSat, highVal = map(int,data.readline().split(','))
		# Create numpy arrays
		l_bound = np.array([lowHue, lowSat, lowVal])
		u_bound = np.array([highHue, highSat, highVal])
		data.close()
		time.sleep(1)
		mode = distMeasurementMode

	if mode == colorCalibrationMode:
		colorCalibration(camera)
	elif mode == distCalibrationMode:
		distCalibration(camera, l_bound, u_bound)
	elif mode == distMeasurementMode:
		distMeasurement(camera, l_bound, u_bound)