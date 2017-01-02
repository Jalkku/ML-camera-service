import cv2
import time
import numpy as np
import subprocess
from datetime import datetime

class ImageProcessing:
	def mse(self, a, b):
		err = np.sum((a.astype("float") - b.astype("float")) ** 2)
		err /= float(a.shape[0] * a.shape[1])
		return err
	
	def diff(self, a, b):
		difference = 255-cv2.absdiff(a, b)
		return difference
		
	def blur(self, img):
		blurred = cv2.medianBlur(img, 7)
		return blurred
					
class Capture:
	def __init__(self, camera, width, height):
		self.camera = camera
		self.fgbg = cv2.BackgroundSubtractorMOG()
		self.camera.set(3, width)
		self.camera.set(4, height)
		subprocess.call("camera_settings.sh", shell=True)
		test_img = self.get_image()
		cv2.imwrite("mnt/cifs/test.jpg", test_img)
		self.mainloop()

	def get_image(self):
		retval, im = self.camera.read()
		gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		return gray

	def mainloop(self):
		previous_image = self.get_image()
		bg = self.get_image()
		while True:
			try:
				#tic = time.time()
				camera_capture = self.get_image()
				mse_ = processing.mse(camera_capture, previous_image)
				#print(mse_)
				original_image = camera_capture.copy()
				if mse_ > 150:
					print("Captured with ", mse_, " MSE")
					camera_capture_ = processing.blur(camera_capture)
					temp_bg = processing.blur(bg)
					difference = processing.diff(camera_capture_, temp_bg)
					_, mask = cv2.threshold(difference,240,255,cv2.THRESH_BINARY_INV)
					#result = 255 - original_image*mask
					# resize mask for faster operations
					#mask = cv2.resize(mask,None,fx=0.3, fy=0.3, interpolation = cv2.INTER_CUBIC)
					#h, w = mask.shape'

					contours, _ = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
					marked_image = original_image.copy()
					for c in contours:
						x,y,w,h = cv2.boundingRect(c)
						if w > 50 and h > 50:
							cv2.rectangle(marked_image,(x,y),(x+w,y+h),(255,0,0),2)
					filename = "/mnt/cifs/"+datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+".jpg"
					filename_m = "/mnt/cifs/"+datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+"_m.jpg"
					cv2.imwrite(filename, marked_image)
					#cv2.imwrite(filename_m, mask)
				else:
					bg = previous_image.copy()
				previous_image = original_image.copy()
				#toc = time.time()

			except KeyboardInterrupt: 
				print("Stopping...")
				del(camera)
				break

processing = ImageProcessing()
capture = Capture(cv2.VideoCapture(0), 1200, 1080)
# for testing
'''
previous_image = cv2.imread('test_images/blank.jpg')
previous_image = cv2.cvtColor(previous_image, cv2.COLOR_BGR2GRAY)
previous_image = cv2.bilateralFilter(previous_image,9,75,75)
original_image = cv2.imread('test_images/2016-12-14_13-46-35_391.jpg')
camera_capture = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
camera_capture = cv2.bilateralFilter(camera_capture,9,75,75)

mse_ = processing.mse(camera_capture, previous_image)
if mse_ > 50:
	difference = processing.diff(camera_capture, previous_image)
	_, mask = cv2.threshold(difference,240,255,cv2.THRESH_BINARY_INV)
	result = 255 - camera_capture*mask
	# resize mask for faster operations
	#mask = cv2.resize(mask,None,fx=0.3, fy=0.3, interpolation = cv2.INTER_CUBIC)
	#h, w = mask.shape
	contours, _ = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	areas = [cv2.contourArea(c) for c in contours]
	max_index = np.argmax(areas)
	cnt=contours[max_index]
	x,y,w,h = cv2.boundingRect(cnt)
	print(x,y,w,h)
	cv2.rectangle(original_image,(x,y),(x+w,y+h),(128,255,128),2)
	#bbox
	for x in range(h-1):
		for y in range(w-1):
			if mask[x, y] == 1:
				bbox = BoundingBox(mask, x, y)
				break;
	cv2.imwrite("/mnt/cifs/result.jpg", original_image)
#capture = Capture(cv2.VideoCapture(0), 1000, 1000)
'''