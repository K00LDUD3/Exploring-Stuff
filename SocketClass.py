import cv2
import numpy as np
class MeshInfo:
    #Prototypes to be stored in a dictionary with key -> code 

    #Note: Shifting by 1 means north becomes east, etc.

    
    def __init__(self, sockets : list, rotation_index : int, img : np.ndarray) -> None:
        self.sockets = sockets
        self.rot_index = rotation_index
        if rotation_index == 1:
            self.img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        if rotation_index == 2:
            self.img = cv2.rotate(img, cv2.ROTATE_180)
        if rotation_index == 3:
            self.img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            self.img = img
        pass
    def shift_sockets(self):
        #FINISH THIS 
        pass