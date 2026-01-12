import numpy as np
import cv2
import matplotlib.pyplot as plt
import random

class MeshInfo:
    def __init__(self, img, sockets, index):
        self.img = img
        self.sockets = sockets 
        self.id = index

inp_img = cv2.imread('Tile7.png')
if inp_img is None:
    inp_img = np.zeros((180, 180, 3), dtype=np.uint8)
    cv2.rectangle(inp_img, (60, 0), (120, 180), (255, 255, 255), -1)

gray = cv2.cvtColor(inp_img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
inp_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)

block_size = 30
map_size = [20, 20]
Map = np.full((map_size[0], map_size[1]), -1).tolist()

l = []
for i in range(0, inp_img.shape[0], block_size):
    for j in range(0, inp_img.shape[1], block_size):
        l.append(inp_img[i:i+block_size, j:j+block_size])

prototypes = {}
unique_hashes = {}
count = 0

def get_edge_id(edge_pixels):
    return tuple(map(tuple, edge_pixels))

for tile_img in l:
    if tile_img.shape[0] != block_size or tile_img.shape[1] != block_size:
        continue

    curr_img = tile_img.copy()
    
    for _ in range(4):
        img_hash = curr_img.tobytes()
        
        if img_hash not in unique_hashes:
            curr_sockets = [
                get_edge_id(curr_img[0, :]),
                get_edge_id(curr_img[:, -1]),
                get_edge_id(curr_img[-1, :]),
                get_edge_id(curr_img[:, 0])
            ]
            
            prototypes[count] = MeshInfo(curr_img, curr_sockets, count)
            unique_hashes[img_hash] = count
            count += 1
        
        curr_img = cv2.rotate(curr_img, cv2.ROTATE_90_CLOCKWISE)

possible_indices = list(prototypes.keys())
candidates = []
for i in range(map_size[0]):
    row = []
    for j in range(map_size[1]):
        row.append(possible_indices.copy())
    candidates.append(row)

def MinEntropy():
    min_val = float('inf')
    min_cell = -1
    
    for i in range(map_size[0]):
        for j in range(map_size[1]):
            ent = len(candidates[i][j])
            if ent > 1 and ent < min_val:
                min_val = ent
                min_cell = [i, j]
    
    return min_cell

def CheckConnection(id1, id2, direction):
    s1 = prototypes[id1].sockets
    s2 = prototypes[id2].sockets
    
    if direction == 0: return s1[0] == s2[2] 
    if direction == 1: return s1[1] == s2[3] 
    if direction == 2: return s1[2] == s2[0] 
    if direction == 3: return s1[3] == s2[1] 
    return False

def Propagate(start_cell):
    stack = [start_cell]
    
    while len(stack) > 0:
        cx, cy = stack.pop(0)
        curr_possible = candidates[cx][cy]
        
        neighbors = [[cx-1, cy, 0], [cx, cy+1, 1], [cx+1, cy, 2], [cx, cy-1, 3]]
        
        for nx, ny, direction in neighbors:
            if nx < 0 or nx >= map_size[0] or ny < 0 or ny >= map_size[1]:
                continue
                
            neighbor_possible = candidates[nx][ny]
            new_neighbor_possible = []
            
            for n_id in neighbor_possible:
                compatible = False
                for c_id in curr_possible:
                    if CheckConnection(c_id, n_id, direction):
                        compatible = True
                        break
                if compatible:
                    new_neighbor_possible.append(n_id)
            
            if len(new_neighbor_possible) < len(neighbor_possible):
                candidates[nx][ny] = new_neighbor_possible
                if len(new_neighbor_possible) == 0:
                    return False
                stack.append([nx, ny])
    return True

def epoch():
    while True:
        c_cell = MinEntropy()
        if c_cell == -1:
            break
            
        x, y = c_cell
        choice = random.choice(candidates[x][y])
        candidates[x][y] = [choice]
        Map[x][y] = choice
        
        if not Propagate(c_cell):
            return 
epoch()

def StitchFinalMap():
    final_h = map_size[0] * block_size
    final_w = map_size[1] * block_size
    stitched = np.zeros((final_h, final_w, 3), dtype=np.uint8)

    for i in range(map_size[0]):
        for j in range(map_size[1]):
            if len(candidates[i][j]) > 0:
                idx = candidates[i][j][0]
                img = prototypes[idx].img
                stitched[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size] = img
            else:
                stitched[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size] = [0, 0, 255]

    return stitched

final_img = StitchFinalMap()

final_img_bgr = cv2.cvtColor(final_img, cv2.COLOR_RGB2BGR)
cv2.imwrite("wfc_output_7.png", final_img_bgr)

print("Map save to wfc_output_7.png")
# plt.figure(figsize=(10,10))
# plt.imshow(final_img)
# plt.axis('off')
# plt.show()