import os
import cv2
import sys

def draw_ocr_results(image, rect, color=(0, 255, 0)):
    
	# unpacking the bounding box rectangle and draw a bounding box
	# surrounding the text along with the OCR'd text itself
	(start_x, start_y, end_x, end_y) = rect
	cv2.rectangle(image, (start_x, start_y), (end_x, end_y), color, 2)
 
	# return the output image
	return image

def draw_image(path, modelo, interes):

	# The name of the image file to annotate
	file_name = os.path.abspath(path)

	## Performs label detection on the image file
	final = cv2.imread(file_name)

	for array in interes[0::]:
		rect = (array[0][0], array[0][1], array[1][0], array[1][1])
		final = draw_ocr_results(final, rect, (0, 255, 0))

	for array in modelo[0::]:
		rect = (array[0][0], array[0][1], array[1][0], array[1][1])
		final = draw_ocr_results(final, rect, (0, 0, 255))

	# show the final output image
	cv2.imshow("CROWD IA2", final)
	cv2.waitKey(0)


if __name__ == "__main__":
    
  sys.stdin.reconfigure(encoding='utf-8')
  sys.stdout.reconfigure(encoding='utf-8')
  
  # [(x1, y1), (x2, y2)]
  interes =[
		[(275, 85), (303, 92)], 
		[(210, 103), (248, 114)]
  ]
  
  modelo =[]
  
  draw_image(path="resources/caratula.jpg", modelo=modelo, interes=interes)