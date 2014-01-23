import os
import sys
import time
import cv2
import numpy as np
from stat import S_ISREG, ST_CTIME, ST_MODE

def Log(t, s):
	now = time.time()
        year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
        milliseconds = int((now - int(now)) * 1000)
        stamp = "[%02d/%02d/%04d %02d%02d%02d,%03d]" % (
                day, month, year, hh, mm, ss, milliseconds)
        print stamp,t,s

# Set window name
DASHCAM_WINDOW_NAME = "Dashcam"

# Set segment video duration in frames (default: 2 minutes)
DASHCAM_VIDEO_DURATION = 60 * 60 * 2

# Set the size limit for the videos folder in bytes (default 500Mb)
DASHCAM_VIDEO_DIR_SIZE_LIMIT = 524288000 # 2147483648

# Set the videos folder
DASHCAM_VIDEO_DIR = './videos'

# Video Capture camera
cap = cv2.VideoCapture(0)

# Open dashcam window
cv2.namedWindow(DASHCAM_WINDOW_NAME, cv2.cv.CV_WINDOW_FULLSCREEN)

# Define the codec and create VideoWriter object
fourcc = cv2.cv.CV_FOURCC('M', 'J', 'P', 'G')

# global settings
current_frame = 0
current_segment = 1


class VideoFifo(object):
	def __init__(self):
		pass

# Create directory if does not exist
if not os.path.exists(DASHCAM_VIDEO_DIR):
    os.makedirs(DASHCAM_VIDEO_DIR)

def get_oldest_video_file():
	dirpath = DASHCAM_VIDEO_DIR
	# get all entries in the directory w/ stats
	entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
	entries = ((os.stat(path), path) for path in entries)

	# leave only regular files, insert creation date
	entries = (path
        	   for stat, path in entries if S_ISREG(stat[ST_MODE]))

	if entries is not None:
		return sorted(entries)[0]

	return None


def get_size():
	path = DASHCAM_VIDEO_DIR
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(path):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			total_size += os.path.getsize(fp)
	return total_size

def get_video_filename():
	global current_segment
	now = time.time()
        year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
        milliseconds = int((now - int(now)) * 1000)
        s = "%s/vid_segment%02d_%02d-%02d-%04d-%02d%02d%02d.avi" % (
                DASHCAM_VIDEO_DIR, current_segment, day, month, year, hh, mm, ss)
	return s


# open the first video writer
out = cv2.VideoWriter(get_video_filename(), fourcc, 60, (1280,720),True)

Log("!", "Started DashPiCam")
os.system("aplay -q ./audio/Recording_Mode.wav")
while True:
	ret, frame = cap.read()

	def save_to_video(frame):
		global current_frame, current_segment, out
		current_frame += 1

		if current_frame <= DASHCAM_VIDEO_DURATION:
			if out.isOpened():
				out.write(frame)
		else:
			Log("!", "Finish segment. Start a new one")
			
			# Check for videos disk space
			if get_size() >= DASHCAM_VIDEO_DIR_SIZE_LIMIT:
				oldest_video_file = get_oldest_video_file()
				if oldest_video_file is not None:
					Log("!", "Videos folder reach the limit. Remove %s" % os.path.abspath(oldest_video_file))
					os.remove(oldest_video_file)
			
			current_segment += 1
			current_frame = 0

			# Reset video writer
			out = None
			out = cv2.VideoWriter(get_video_filename(), fourcc, 24, (640,480),True)

	# save frame
	save_to_video(frame)

	# show frame in window
	cv2.imshow(DASHCAM_WINDOW_NAME, frame)

	# Detect face in frame
#	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#	if faces is not None:
#		for (x,y,w,h) in faces:
#			os.system('echo foundface')
#			cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0),2)
#			roi_gray = gray[y:y+h, x:x+w]
#			roi_color = frame[y:y+h, x:x+w]
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

cap.release()
cv2.destroyAllWindows()

