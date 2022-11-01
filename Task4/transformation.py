import numpy as np


'''
# Rotations
roll = np.deg2rad(0)
pitch = np.deg2rad(0)
yaw = np.deg2rad(180)

# Translations
dx = 0.78
dy = 0.0
dz = 0.0
'''

def transformation_matrix(roll,pitch,yaw,dx,dy,dz):
    # Rotational Matrix (Assume rotates in counter-clockwise)
    roll = np.deg2rad(roll)
    pitch = np.deg2rad(pitch)
    yaw = np.deg2rad(yaw)

    Rx = np.array([[1,0,0,0],\
                [0,np.cos(roll),np.sin(roll),0],\
                [0,-1*np.sin(roll),np.cos(roll),0],\
                [0,0,0,1]\
                ])
                
    Ry = np.array([[np.cos(pitch),0,-1*np.sin(pitch),0],\
                [0,1,0,0],\
                [np.sin(pitch),0,np.cos(pitch),0],\
                [0,0,0,1]\
                ])
                
    Rz = np.array([[np.cos(yaw),np.sin(yaw),0,0],\
                [-1*np.sin(yaw),np.cos(yaw),0,0],\
                [0,0,1,0],\
                [0,0,0,1]\
                ])
    Rxy = np.matmul(Rx,Ry)
    Rxyz = np.matmul(Rxy,Rz)

    # Add translation
    Rxyz[0][3] = dx
    Rxyz[1][3] = dy
    Rxyz[2][3] = dz
    print("Rotational Matrix")
    print(np.round(Rxyz,3))
    return Rxyz

if __name__=='__main__':
    # Original Pose
    box_a = np.array([0.2,-0.2,0.435,1])
    print("Original Pose:",box_a)
    # Resultant Pose
    Rxyz = transformation_matrix(0,0,90,0.4,0.4,0)
    box_b = np.matmul(Rxyz,box_a)
    print("Resultant Pose (Rotate->Translate):",np.round(box_b,3))

