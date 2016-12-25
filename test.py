import cv2
import time
import numpy as np
from datetime import datetime

camera_port = 0
 
ramp_frames = 10

camera = cv2.VideoCapture(0)

fgbg = cv2.BackgroundSubtractorMOG()

camera.set(3,1000)
camera.set(4,1000)
 
def get_image():
	retval, im = camera.read()
	gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	return gray

def mse(a, b):
	err = np.sum((a.astype("float") - b.astype("float")) ** 2)
	err /= float(a.shape[0] * a.shape[1])
	return err

previous_image = get_image()

while True:
	try:
		'''
		for i in xrange(ramp_frames):
			temp = get_image()'''

		camera_capture = get_image()
		mse_ = mse(camera_capture, previous_image)
		if mse_ > 50:
			print("Movement with ", mse_, " MSE")
			subtraction = camera_capture - previous_image
			fgmask = fgbg.apply(camera_capture)
			file = "/mnt/cifs/"+datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+".jpg"
			file_s = "/mnt/cifs/"+datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+"_s.jpg"
			file_f = "/mnt/cifs/"+datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+"_f.jpg"
			cv2.imwrite(file, camera_capture)
			cv2.imwrite(file_s, subtraction)
			cv2.imwrite(file_f, fgmask)
			print("Captured ", file)
		else:
			print(mse_)

		previous_image = camera_capture
		#time.sleep(1)

	except KeyboardInterrupt: 
		print("Stopping...")
		del(camera)
		break


