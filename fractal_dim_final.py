import cv2
import numpy as np
import matplotlib.pyplot as plt 
import math 
import pandas as pd


#filling the contour of the object in the image in, it was usefull for me as there was a lot of noise in the countour; you can remove it if you dont need it 
def fillin(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:

        if cv2.contourArea(cnt) < 10 ** 9:
            cv2.drawContours(img, [cnt], 0, (0, 0, 0), -1)


def preprocess_image(image_file, showimage):
    image = cv2.imread(image_file)
    fillin(image)
    
    image = cv2.fastNlMeansDenoisingColored(image, None, h=20)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.medianBlur(gray, 5)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)
    thresh = cv2.fastNlMeansDenoising(thresh, None, 30)
    if showimage:
        cv2.imshow('', thresh)
        cv2.waitKey(0)

    return thresh


'''
showimage - display the edited image, usefull to understand whether the preprocess fucntion worked properly
showgraph - graph is used in determening the fractal dimension, ultimately it should be close to a straight line,
if it is not, it would be usefull to ignore the 'ends' of it and only take the middle part that is more simmilar to a straigth line,
to determine the slope of the graph 
'''
def fractal_dimension(image_file, showimage=False, showgraph=False):
    image = preprocess_image(image_file, showimage)

    counts = []
    scales = []
    for i in range(1, min(image.shape)//2):
        boxes = np.zeros((i, i))
        for j in range(i):
            for k in range(i):
                boxes[j][k] = np.sum(image[j * (image.shape[0] // i) : (j + 1) * (image.shape[0] // i),
                                     k * (image.shape[1] // i):(k + 1) * (image.shape[1] // i)])
        counts.append(np.sum(boxes > 0))
        scales.append(1 / i)

    if showgraph:
        countslog = [math.log10(i) for i in counts]
        scaleslog = [math.log10(i) for i in scales]
        print(countslog, scaleslog)
        plt.scatter(countslog, scaleslog, s = 5)
        plt.show()
    
    coeffs = np.polyfit(np.log(scales), np.log(counts), 1)
    return -coeffs[0]





def main():
    #sample usage
    image_file = 'C:\\path.jpg'
    fd = fractal_dimension(image_file, showimage=True, showgraph=True)
    print(f"fractal dimension is {fd:.3f}")
