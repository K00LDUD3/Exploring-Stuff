import cv2
import numpy as np
import math
class MeshInfo:
    #Prototypes to be stored in a dictionary with key -> code 

    #Note: Shifting by 1 means north becomes east, etc. (Clockwise shifting)

    
    def __init__(self, sockets : list, rotation_index : int, img : np.ndarray) -> None:
        self.rot_index = rotation_index
        self.sockets = MeshInfo.rotate(sockets, -self.rot_index*3)
        self.img_default = img

    def rotate(l, n):
        return l[n:] + l[:n]

    def Img(self):
        if self.rot_index == 1:
            return cv2.rotate(self.img_default, cv2.ROTATE_90_CLOCKWISE)
        if self.rot_index == 2:
            return cv2.rotate(self.img_default, cv2.ROTATE_180)
        if self.rot_index == 3:
            return cv2.rotate(self.img_default, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            return self.img_default
