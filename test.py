import cv2
import time
import numpy as np
from datetime import datetime

capture = Capture(cv2.VideoCapture(0), 1000, 1000)
processing = ImageProcessing()

class Capture:
	def __init__(self, camera, width, height):
		self.camera = camera
		self.fgbg = cv2.BackgroundSubtractorMOG()
		self.camera.set(3, width)
		self.camera.set(4, height)
	 
	def get_image():
		retval, im = this.camera.read()
		gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		return gray

	def mainloop():
		previous_image = self.get_image()
		while True:
			try:
				'''
				for i in xrange(10):
					temp = get_image()'''
				tic = int(round(time.time() * 1000))
				camera_capture = self.get_image()
				mse_ = processing.mse(self.camera_capture, previous_image)
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
				toc = int(round(time.time() * 1000))
				print("FPS: ", 1/(tic-toc))

			except KeyboardInterrupt: 
				print("Stopping...")
				del(camera)
				break

class ImageProcessing:
	def mse(a, b):
		err = np.sum((a.astype("float") - b.astype("float")) ** 2)
		err /= float(a.shape[0] * a.shape[1])
		return err