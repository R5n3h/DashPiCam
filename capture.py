import pygame
import Image
import sys
import numpy
import cv2

class Camera:
	pass

cap = cv2.VideoCapture(0)
i=0
def get_image():
    ret, im = cap.read()
    #convert numpy array to PIL image
    im = numpy.array(im)
    return Image.fromarray(im)
 
fps = 25.0
pygame.init()
window = pygame.display.set_mode((1280,720))
#pygame.display.toggle_fullscreen()
pygame.display.set_caption("WebCAM Demo")
screen = pygame.display.get_surface()
 
while True:
    events = pygame.event.get()
    for event in events:
	if event.type == pygame.QUIT:
		pygame.display.quit()
	elif event.type == pygame.KEYUP:
		print event.key
		if event.key == 102:
			pygame.display.toggle_fullscreen()


    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))

