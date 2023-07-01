import cv2
import numpy as np
import matplotlib.pyplot as plt 
import math 
import pandas as pd

'''
Some scripts I used when processing my experiments
**Not a working code on its own, copy the functions in to the main file**
Detecting a circle in the image worled perfectly for me with the best_circle() function
'''


#split video at videopath into images/frames, take an image from a video once an interval, put results in folder at foldername
def vid_to_frames(videopath, interval, foldername):
    cap = cv2.VideoCapture(videopath)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    time_count = 0
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        time_count += 1/fps


        if time_count >= interval:
            output_file = 'path' + str(foldername) + '\\' + str(count * interval + int(time_count)) + '.jpg'
            cv2.imwrite(output_file, frame)
            time_count = 0
            count += 1 
            print(output_file)
    cap.release()


#detecting a circular object (singular) in the image
def best_circle(image):
    gray_blur = cv2.GaussianBlur(image, (5, 5), 0)
    _, binary = cv2.threshold(gray_blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best_circle = None
    max_white_pixels = 0
    for contour in contours:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)
        mask = np.zeros_like(binary)
        cv2.circle(mask, center, radius, 255, -1)
        white_pixels = np.sum(mask == 255)
        if white_pixels > max_white_pixels:
            max_white_pixels = white_pixels
            best_circle = (center, radius)

    if best_circle is not None:
        center, radius = best_circle
        diameter = radius * 2
        print("Diameter:", diameter, "pixels")
        cv2.circle(image, center, radius, (255, 255, 255), 2)
        cv2.imshow("Best Circle Detection", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        print("No circles found in the image.")



def get_video_length(video_path):
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    video_length = total_frames / fps
    video.release()
    return video_length

#example of how I used the code to process an image for the radius of the circluar object and its fractal dimension over the course of the video, writing data to a csv file
def video_to_csv(video, csvfile, foldername):
    vid_duration = int(get_video_length(video))
    times = [i + 1 for i in range(1, vid_duration + 1)]
    dims = []
    for i in [i for i in range(1, vid_duration + 1)]:
        try:
            image_file = f'path\\{foldername}\\{i}.jpg'
            fd = fractal_dimension(image_file, showimage=False)
            print(f"video {foldername} - fd at {i}s - {fd:.3f}")
            dims.append(fd)
        except:
            print(f'SOMETHING WENT WRONG FOR FRACTAL DIMENSION {foldername}, at second {i}')
            dims.append(-1)
    
    radia = [] 
    for i in [i for i in range(1, vid_duration + 1)]:
        try:
            image_file = f'path\\{foldername}\\{i}.jpg'
            imgage_current = preprocess_image(image_file, showimage=False)
            radia.append(best_circle(imgage_current))
            print(f'video {foldername} - rad at {i}s - {radia[-1]}')
        except:
            print(f'SOMETHING WENT WRONG FOR RADIA CALCULATION {foldername}, at second {i}')
            radia.append(-1)


    description = [foldername, vid_duration]
    print(description)
    print(times)
    print(dims)
    print(radia)
    df = pd.read_csv('path.csv')
    df = df.reset_index(drop=True)
    new_row = pd.DataFrame({'name': [foldername], 'duration': [vid_duration], 'dimensions': [dims], 'radia': [radia]}, index=[0])
    df = pd.concat([new_row, df.loc[:]]).reset_index(drop=True)
    df.to_csv('path.csv')
    print(f'video {foldername} processed')
