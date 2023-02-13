import numpy as np
from patchify import patchify
import cv2
import matplotlib.pyplot as plt
from SocketClass import MeshInfo

inp_img = cv2.imread('Tile.png')

# Variables
block_size = 30
size_tset = [int(inp_img.shape[0]/30)-1, int(inp_img.shape[1]/30)-1]
map_size = [10,10]
Map = np.full((map_size[0],map_size[1]),-1)
sockets = np.full((map_size[0], map_size[1], 4), 1, dtype=int)
candidates = np.ndarray((map_size[0], map_size[1]))

prototypes = {}

# Extracting tiles from input (inp_img)
l = []
for i in range(0, inp_img.shape[0]-block_size, block_size):
    for j in range(0, inp_img.shape[1]-block_size, block_size):
        l.append(inp_img[i:i+block_size,j:j+block_size])



n_cells = []
count = 0
# Setting the sockets to neighbor sockets pixel to side length ratio (1/6, 3/6, 5/6)
# Basically Creating prototypes so we can start placing tiles
for i in range(size_tset[0]):
    for j in range(size_tset[1]):
        # Fetching neighbor cells
        #look north
        n_cells=[]
        if i-1 in range(size_tset[0]):
            n_cells.append([i-1,j])
        else:
            n_cells.append(-1)
        #look east
        if j+1 in range(size_tset[1]):
            n_cells.append([i,j+1])
        else:
            n_cells.append(-1)
        #look south
        if i+1 in range(size_tset[0]):
            n_cells.append([i+1,j])
        else:
            n_cells.append(-1)
        #look west
        if j-1 in range(size_tset[0]):
            n_cells.append([i,j-1])
        else:
            n_cells.append(-1)
        
        # Gettings neighbor sockets
        socket = []
        #look north
        if n_cells[0] != -1:
            x,y = n_cells[0]
            o,m,n = l[x*size_tset[0]+y][29,int(block_size/6)], l[x*size_tset[0]+y][29,int(block_size*3/6)], l[x*size_tset[0]+y][29,int(block_size*5/6)]
            o = int(sum(o)/3/255)
            m = int(sum(m)/3/255)
            n = int(sum(n)/3/255)
            socket.extend([o,m,n])
        else:
            socket.extend([-1,-1,-1])

        #look east
        if n_cells[1] != -1:
            x,y = n_cells[1]
            o,m,n = l[x*size_tset[0]+y][int(block_size/6),0], l[x*size_tset[0]+y][int(block_size*3/6),0], l[x*size_tset[0]+y][int(block_size*5/6),0]
            o = int(sum(o)/3/255)
            m = int(sum(m)/3/255)
            n = int(sum(n)/3/255)
            socket.extend([o,m,n])
        else:
            socket.extend([-1,-1,-1])

        #look south
        if n_cells[2] != -1:
            x,y = n_cells[2]
            o,m,n = l[x*size_tset[0]+y][0,int(block_size/6)], l[x*size_tset[0]+y][0,int(block_size*3/6)], l[x*size_tset[0]+y][0,int(block_size*5/6)]
            o = int(sum(o)/3/255)
            m = int(sum(m)/3/255)
            n = int(sum(n)/3/255)
            socket.extend([n,m,o])
        else:
            socket.extend([-1,-1,-1])
       

        #look west
        if n_cells[3] != -1:
            x,y = n_cells[3]
            o,m,n = l[x*size_tset[0]+y][int(block_size/6),29], l[x*size_tset[0]+y][int(block_size*3/6),29], l[x*size_tset[0]+y][int(block_size*5/6),29]
            o = int(sum(o)/3/255)
            m = int(sum(m)/3/255)
            n = int(sum(n)/3/255)
            socket.extend([n,m,o])
            
        else:
            socket.extend([-1,-1,-1])
        print(socket)


        #Creating prototype
        for rot in range(4):
            prototypes[count] = MeshInfo(socket, rot, l[i*size_tset[0]+j])
            count+=1

print(len(prototypes))
#subplot(r,c) provide the no. of rows and columns
f, axarr = plt.subplots(5,5) 

# use the created array to output your multiple images
for i in range(size_tset[0]):
    for j in range(size_tset[1]):
        axarr[i,j].imshow(l[i*size_tset[0]+j], interpolation='none')
plt.show()