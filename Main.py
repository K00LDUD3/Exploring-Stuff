import numpy as np
from patchify import patchify
import cv2
import matplotlib.pyplot as plt
from SocketClass import MeshInfo
import random

inp_img = cv2.imread('Tile.png')

# Variables
block_size = 30
size_tset = [int(inp_img.shape[0]/block_size)-1, int(inp_img.shape[1]/block_size)-1]
map_size = [10,10]
Map = np.full((map_size[0],map_size[1]),-1).tolist()
sockets = np.full((map_size[0], map_size[1], 12), -1, dtype=int).tolist()


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

        #Creating prototype
        for rot in range(4):
            prototypes[count] = MeshInfo(socket, rot, l[i*size_tset[0]+j])
            count+=1

print(f"{len(prototypes)=}")
#subplot(r,c) provide the no. of rows and columns
f, axarr = plt.subplots(5,5) 

# use the created array to output your multiple images
for i in range(size_tset[0]):
    for j in range(size_tset[1]):
        axarr[i,j].imshow(l[i*size_tset[0]+j], interpolation='none')
plt.show()

x = list(prototypes.keys())
candidates = np.full((map_size[0], map_size[1], len(x)), x, dtype=int).tolist()

def MinEntropy():
    #Getting least entropy length
    min_entropy = len(x)
    max_entropy = min_entropy-1
    for i in range(len(candidates)):
        for j in range(len(candidates[0])):
                if len(candidates[i][j]) < min_entropy and len(candidates[i][j]) > 1:
                    min_entropy = len(candidates[i][j])
                if len(candidates[i][j]) > max_entropy:
                    max_entropy = len(candidates[i][j])
    #If maximum entropy (possibilites) is 1, then return -1
    if max_entropy == 1:
        return -1

    #Looking for first cell with minimum entropy
    for i in range(len(candidates)):
        for j in range(len(candidates[0])):
            if len(candidates[i][j]) == min_entropy:
                return (i,j)
    return -1

def ChooseRandomTile(c_cell : list):
    choice = random.choice(candidates[c_cell[0]][c_cell[1]])
    candidates[c_cell[0]][c_cell[1]], Map[c_cell[0]][c_cell[1]] = [choice], choice
    print(f"Random Choice for {c_cell[0]},{c_cell[1]}: {choice}")

def UpdateCurrentCellSockets(c_cell : list):
    x,y = c_cell
    key = Map[x][y]
    sockets[x][y] = prototypes[key].sockets
    print(f"{sockets[x][y]=}")
    return

def UpdateNeighborSockets(c_cell : list):
    #look in 4 directions NESW
    #Update that section of sockets(12)
    
    #Getting neighbor cells
    x,y = c_cell
    n_cells=[]
    if x-1 in range(size_tset[0]):
        n_cells.append([x-1,y])
    else:
        n_cells.append(-1)
    #look east
    if y+1 in range(size_tset[1]):
        n_cells.append([x,y+1])
    else:
        n_cells.append(-1)
    #look south
    if x+1 in range(size_tset[0]):
        n_cells.append([x+1,y])
    else:
        n_cells.append(-1)
    #look west
    if y-1 in range(size_tset[0]):
        n_cells.append([x,y-1])
    else:
        n_cells.append(-1)
    
    #setting neighbor cells sockets to current cells sockets which are facing the neighbor
    #NORTH
    if n_cells[0] != -1:
        sockets[n_cells[0][0]][n_cells[0][1]][6:9] = prototypes[Map[x][y]].sockets[0:3][::-1]
    #EAST
    if n_cells[1] != -1:
        sockets[n_cells[1][0]][n_cells[1][1]][9:12] = prototypes[Map[x][y]].sockets[3:6][::-1]
    #SOUTH
    if n_cells[2] != -1:
        sockets[n_cells[2][0]][n_cells[2][1]][0:3] = prototypes[Map[x][y]].sockets[6:9][::-1]
    #WEST
    if n_cells[3] != -1:
        sockets[n_cells[3][0]][n_cells[3][1]][3:6] = prototypes[Map[x][y]].sockets[9:12][::-1]
    
    return n_cells

def UpdateNeighborCells(c_cell : list, n_cells : list):
    #Eliminating possibilities for the neighbor cell
    #Cycle thru candidates of neighbor cells
    #Check if each candidate has the sockets listed
    #if they do, add it to new candidates 

    for i in range(len(n_cells)):
        if n_cells ==-1:
            continue
        
    return

def epoch():
    c_cell = MinEntropy()

    if c_cell == -1:
        return -1

    # Starting with a random tile
    ChooseRandomTile(c_cell=c_cell)
    # Update Current cell sockets
    UpdateCurrentCellSockets(c_cell)
    # Eliminate Neighbor sockets
    n_cells = UpdateNeighborSockets(c_cell=c_cell)
    # Eliminate Neighbor Cells
    UpdateNeighborCells(c_cell, n_cells)
        
epoch()