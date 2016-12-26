import cv2
import time
import numpy as np
from datetime import datetime

class ImageProcessing:
	def mse(self, a, b):
		err = np.sum((a.astype("float") - b.astype("float")) ** 2)
		err /= float(a.shape[0] * a.shape[1])
		return err

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
					#subtraction = camera_capture - previous_image
					#fgmask = fgbg.apply(camera_capture)
					file = "/mnt/cifs/"+datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+".jpg"
					#file_s = "/mnt/cifs/"+datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+"_s.jpg"
					#file_f = "/mnt/cifs/"+datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+"_f.jpg"
					cv2.imwrite(file, camera_capture)
					#cv2.imwrite(file_s, subtraction)
					#cv2.imwrite(file_f, fgmask)
					print("Captured ", file)

				previous_image = camera_capture
				toc = time.time()
				print("FPS: "+ str(1/(toc-tic)))

			except KeyboardInterrupt: 
				print("Stopping...")
				del(camera)
				break

processing = ImageProcessing()

fgbg = cv2.BackgroundSubtractorMOG()
previous_image = cv2.imread('test_images/1.jpg')
previous_image = cv2.cvtColor(previous_image, cv2.COLOR_BGR2GRAY)
camera_capture = cv2.imread('test_images/2.jpg')
camera_capture = cv2.cvtColor(camera_capture, cv2.COLOR_BGR2GRAY)

mse_ = processing.mse(camera_capture, previous_image)
if mse_ > 50:
	subtraction = 255-(camera_capture/2-previous_image/2)
	cv2.imwrite("/mnt/cifs/result.jpg",subtraction)
#capture = Capture(cv2.VideoCapture(0), 1000, 1000)