import matplotlib.pyplot as plt 
import numpy as np 
import random
import math
from PIL import Image
import glob
import os
import cv2 
import time 

def create_image_with_point(array, point_coordinates, save_path):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.imshow(array, cmap='binary', origin='upper')
    if len(point_coordinates) == 2:
        x, y = point_coordinates
        ax.plot(x, y, 'ro', markersize=10)
    ax.axis('off')
    plt.savefig(save_path, dpi=600, bbox_inches='tight')
    plt.close()



class Walker:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.prevx = x
        self.prevy = y
    
    def update_pos(self, greed_size):
        move = random.choice([(-1, 0), (0, -1), (1, 0), (0, 1)])
        if self.x + move[0] <= greed_size and self.x + move[0]>= 0:
            self.prevx = self.x
            self.x += move[0]
        if self.y + move[1] <= greed_size and self.y + move[1]>= 0:
            self.prevy = self.y
            self.y += move[1]

    def update_offgrid(self, radius):
        return 0


def visual(grid, grid_size):
    rng = random.randint(1, 4)
    if rng == 1:
        walker1 = Walker(random.randint(1, grid_size - 1), 1)
    elif rng == 2:
        walker1 = Walker(random.randint(1, grid_size - 1), grid_size - 1)
    elif rng == 3:
        walker1 = Walker(1,random.randint(1, grid_size - 1))
    else:
        walker1 = Walker(grid_size - 1, random.randint(1, grid_size - 1))

    #walk until meets the tree 
    c = 0
    while True: 
        if grid[walker1.x, walker1.y] == 1:
            grid[walker1.prevy, walker1.prevx] = 1
            for i in range(50):
                create_image_with_point(grid, (walker1.x, walker1.y), f'C:\\path\\DLA\\animation\\{c + i * 2}.jpg')
            break
        walker1.update_pos(grid_size)
        if c % 2 == 0:
            create_image_with_point(grid, (walker1.x, walker1.y), f'C:\\path\\DLA\\animation\\{c}.jpg')
        c += 1




def simplewalk(grid, grid_size, total_walkers, save_figure = True):      
    for i in range(total_walkers):
        #random spawn along any of 4 walls 
        rng = random.randint(1, 4)
        if rng == 1:
            walker1 = Walker(random.randint(1, grid_size - 1), 1)
        elif rng == 2:
            walker1 = Walker(random.randint(1, grid_size - 1), grid_size - 1)
        elif rng == 3:
            walker1 = Walker(1,random.randint(1, grid_size - 1))
        else:
            walker1 = Walker(grid_size - 1, random.randint(1, grid_size - 1))

        #walk until meets the tree 
        while True: 
            if grid[walker1.x, walker1.y] == 1:
                xxx = random.randint(1, 50)
                if xxx == 1:
                    grid[walker1.prevx, walker1.prevy] = 1
                break
            walker1.update_pos(grid_size)

        #save figure 
        if save_figure:
            fig, ax = plt.subplots()
            ax.set_aspect('equal')
            ax.imshow(grid, cmap='binary', origin='upper')
            ax.axis('off')
            plt.savefig(f'C:\\path\\DLA\\frames\\{i}.jpg', dpi=600, bbox_inches='tight')
            plt.close()





def batch_walk(grid, grid_size, batchsize, batchnum, save_figure = False, savefinal = False, savefinal_name = 'none'):
    for i in range(batchnum):
        newspots = []
        for j in range(batchsize):
            #random spawn along any of 4 walls 
            rng = random.randint(1, 4)
            if rng == 1:
                walker1 = Walker(random.randint(1, grid_size - 1), 1)
            elif rng == 2:
                walker1 = Walker(random.randint(1, grid_size - 1), grid_size - 1)
            elif rng == 3:
                walker1 = Walker(1,random.randint(1, grid_size - 1))
            else:
                walker1 = Walker(grid_size - 1, random.randint(1, grid_size - 1))

            ##uncomment for circular seed
            # alpha = random.randint(0, 359)
            # x1 = int(((grid_size - 10) // 2) * math.sin(alpha * 3.14159 / 180)) + grid_size // 2
            # y1 = int(((grid_size - 10) // 2) * math.cos(alpha * 3.14159 / 180)) + grid_size // 2
            # #print(x1, y1)
            # walker1 = Walker(x1, y1) 

            #walk until meets the tree 
            while True: 
                if grid[walker1.x, walker1.y] == 1:
                    newspots.append((walker1.prevx, walker1.prevy))
                    break
                walker1.update_pos(grid_size)




        #save figure 
        if save_figure:
            fig, ax = plt.subplots()
            ax.set_aspect('equal')
            ax.imshow(grid, cmap='binary', origin='upper')
            ax.axis('off')
            plt.savefig(f'C:\\path\\DLA\\frames\\{i}.jpg', dpi=600, bbox_inches='tight')
            plt.close()

    if savefinal:
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.imshow(grid, cmap='binary', origin='upper')
        ax.axis('off')
        plt.savefig(f'C:\\path\\DLA\\batches\\{batchsize}.jpg', dpi=800, bbox_inches='tight')
        plt.close()




def make_gif(framestotal, frame_duration=1):
    image_directory = 'C:\\path\\DLA\\animation\\'
    image_paths = glob.glob(image_directory + '*.jpg') 
    image_paths.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
    if len(image_paths) < framestotal:
        framestotal = len(image_paths)
    k = len(image_paths) // framestotal
    image_paths = [image_paths[i * k] for i in range(framestotal)]
    images = []
    for image_path in image_paths:
        image = Image.open(image_path)
        images.append(image)
    output_path = 'C:\\path\\DLA\\output.gif'

    # Save the images as an animated GIF
    images[0].save(output_path, save_all=True, append_images=images[1:], duration=frame_duration, loop=0)


def main(): 
    start_time = time.time()

    n = 500
    grid = np.zeros((n + 1, n + 1))

    #set single-point seed
    #grid[n // 2, n // 2] = 1 

    #set circle seed
    r = n // 5
    for i in range(n * 4):
        grid[int((n // 2) + r * math.sin(i)), int((n // 2) + r * math.cos(i))] = 1

    #perform a single, one-by-one walker simulation 
    simplewalk(grid, n, 50000, True)

    #perform a series of batch simulations (can be a series of one-by-one walker symulation)
    # for size in [i * 50 for i in range(13, 16)]:
    #     n = 700
    #     grid = np.zeros((n + 1, n + 1))
    #     r = n // 5
    #     for i in range(n * 4):
    #         grid[int((n // 2) + r * math.sin(i)), int((n // 2) + r * math.cos(i))] = 1

    #     batch_walk(grid, n, size, 100, save_figure= False, savefinal= True)


    end_time = time.time()
    print("Simulation execution time:", end_time - start_time, "seconds")


    #create a gif of saved images 
    make_gif(249, frame_duration=0.1)
    gif_time = time.time()
    print("GIF rendering time:", gif_time - end_time, "seconds")

    #create a simple example visual animation of DLA algortihm, better with small map/seed/number of walkers, has to be used separely and with its own make_gif
    #visual(grid, n)


if __name__ == '__main__':
    main()