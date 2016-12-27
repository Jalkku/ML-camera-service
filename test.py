import cv2
import time
import numpy as np
from datetime import datetime

class ImageProcessing:
	def mse(self, a, b):
		err = np.sum((a.astype("float") - b.astype("float")) ** 2)
		err /= float(a.shape[0] * a.shape[1])
		return err
	
	def diff(self, a, b):
		difference = 255-cv2.absdiff(a, b)
		return difference
		
		
class BoundingBox:
	def __init__(self, img, x, y):
		width, height = img.shape
		print(width,height)
		self.covered = np.zeros((height, width,1), np.uint8)
		self.boundXmin = 0
		self.boundXmax = height
		self.boundYmin = 0
		self.boundYmax = width
		while len(neighbors) != 0:
			current = neighbors[0]
			neighbors.pop(0)
			self.covered[current[0], current[1]] == 255
			for x_ in range(current[0]-1, current[0]+1):
				for y_ in range(current[1]-1, current[1]+1):
					print("trying ", x_, y_)
					if img[x_, y_] == 255 and (x_, y_) not in neighbors and self.covered[x_, y_] == 0:
						print("appent ", x_, y_)
						neighbors.append((x_, y_))
			print(neighbors)
						
		print(neighbors)
					
class Capture:
	def __init__(self, camera, width, height):
		self.camera = camera
		self.fgbg = cv2.BackgroundSubtractorMOG()
		self.camera.set(3, width)
		self.camera.set(4, height)
		self.mainloop()
	 
	def get_image(self):
		retval, im = self.camera.read()
		gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		return gray

	def mainloop(self):
		previous_image = self.get_image()
		while True:
			try:
				'''
				for i in xrange(10):
					temp = get_image()'''
				tic = time.time()
				camera_capture = self.get_image()
				mse_ = processing.mse(camera_capture, previous_image)
				if mse_ > 50:
					print("Movement with ", mse_, " MSE")
					file = "/mnt/cifs/"+datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+".jpg"
					cv2.imwrite(file, camera_capture)
					print("Captured ", file)

				previous_image = camera_capture
				toc = time.time()
				print("FPS: "+ str(1/(toc-tic)))

			except KeyboardInterrupt: 
				print("Stopping...")
				del(camera)
				break

processing = ImageProcessing()

# for testing
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
	'''
	for x in range(h-1):
		for y in range(w-1):
			if mask[x, y] == 1:
				bbox = BoundingBox(mask, x, y)
				break;'''
	cv2.imwrite("/mnt/cifs/result.jpg", original_image)
#capture = Capture(cv2.VideoCapture(0), 1000, 1000)