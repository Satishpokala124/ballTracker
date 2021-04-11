import cv2
import numpy as np
import imutils

def colorCalibration(camera):
	ret, frame = camera.read()
	# Converting frame from 'BGR' to 'HSV'
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# Reading the values from 'Tracker' window
	lowHue = cv2.getTrackbarPos('Lower Heu', 'Tracker')
	lowSat = cv2.getTrackbarPos('Lower Sat', 'Tracker')
	lowVal = cv2.getTrackbarPos('Lower Val', 'Tracker')
	highHue = cv2.getTrackbarPos('Upper Heu', 'Tracker')
	highSat = cv2.getTrackbarPos('Upper Sat', 'Tracker')
	highVal = cv2.getTrackbarPos('Upper Val', 'Tracker')
	# Creating numpy arrays
	l_bound = np.array([lowHue, lowSat, lowVal])
	u_bound = np.array([highHue, highSat, highVal])
	# Masking all other colors except the colors in the selected range
	mask = cv2.inRange(hsv, l_bound, u_bound)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	result = cv2.bitwise_and(frame, frame, mask=mask)
	# Displaying 'frame', mask' and 'result'
	cv2.imshow('main', frame)
	cv2.imshow('hsv', hsv)
	cv2.imshow('mask', mask)
	cv2.imshow('result', result)
	# Saving selected values to 'data.txt'
	key = cv2.waitKey(1)
	if key == ord('s'):
		data = open('data.txt', 'w')
		data.write(str(lowHue)+','+str(lowSat)+','+str(lowVal)+'\n')
		data.write(str(highHue)+','+str(highSat)+','+str(highVal))
		print('Saving selected values to "data.txt"')
		data.close()

def distCalibration(camera, l_bound, u_bound):
	ret, frame = camera.read()
	# Converting frame from 'BGR' to 'HSV'
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# Masking the frame with given color bounds
	mask = cv2.inRange(hsv, l_bound, u_bound)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	# Finding out the Contours in the mask 
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	x = 0
	y = 0
	radius = 0
	area = 0
	if len(cnts)>0:
		# Finding the area of the lasgest contour
		c = max(cnts, key=cv2.contourArea)
		# Finding the center, radius of a circle needed to fit the whole contour
		((x, y), radius) = cv2.minEnclosingCircle(c)
		center = (int(x), int(y))
		cv2.circle(frame, center, int(radius), (0, 255, 255), 2)
		area = cv2.contourArea(c)
	font = cv2.FONT_HERSHEY_SIMPLEX
	fontScale = 0.8
	fontColor = (0, 0, 0) 
	thickness = 2
	screen = np.zeros(shape=[150, 300, 3], dtype=np.uint8)
	screen[:][:][:] = 255
	cv2.putText(screen, 
		"Area: "+str(area), (60, 50), 
		font, fontScale, fontColor, thickness
	)
	cv2.putText(screen, 
		"Radius: "+str(round(radius,5)), (20, 100), 
		font, fontScale, fontColor, thickness
	)
	cv2.imshow('main', frame)
	cv2.imshow('screen', screen)

def distMeasurement(camera, l_bound, u_bound):
	ret, frame = camera.read()
	# Converting frame from 'BGR' to 'HSV'
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# Masking the frame with given color bounds
	mask = cv2.inRange(hsv, l_bound, u_bound)
	# cv2.imshow('mask', mask)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	# result = cv2.bitwise_and(frame, frame, mask=mask)
	# Finding out the Conto33urs in the mask 
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	x = 0
	y = 0
	radius = 0
	area = 0
	if len(cnts)>0:
		# Finding the area of the lasgest contour
		c = max(cnts, key=cv2.contourArea)
		# Finding the center, radius of a circle needed to fit the whole contour
		((x, y), radius) = cv2.minEnclosingCircle(c)
		center = (int(x), int(y))
		cv2.circle(frame, center, int(radius), (0, 255, 255), 2)
	# Calculate dist
	if radius ==0:
		dist = 0
	else:
		# radius = 2076.056808836 / (dist**1.0161313014531)
		dist = (2076.056808836 / radius) ** (1 / 1.0161313014531)
	font = cv2.FONT_HERSHEY_SIMPLEX
	fontScale = 0.8
	fontColor = (0, 0, 0) 
	thickness = 2
	screen = np.zeros(shape=[150, 300, 3], dtype=np.uint8)
	screen[:][:][:] = 255
	if dist:
		cv2.putText(screen, 
			"Distance: "+str(round(dist, 4)), (40, 100), 
			font, fontScale, fontColor, thickness
		)
	else:
		cv2.putText(screen, 
			"Distance: "+"No Object", (40, 100), 
			font, fontScale, fontColor, thickness
		)
	cv2.putText(frame, 
		"Radius: "+str(round(radius, 2)), (0, 50), 
		font, fontScale, fontColor, thickness
	)
	cv2.imshow('frame', frame)
	cv2.imshow('screen', screen)

def nothing(x):
	pass