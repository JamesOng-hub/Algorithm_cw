import cv2
import numpy as np
from random import randint

#in python matrix. M[row,column]

##loading actual images
imgL1 = cv2.imread('pic1L.png', 0)
# cv2.imwrite('gpic1L.png', imgL1) #left grey picture saved

imgR1 = cv2.imread('pic1R.png',0)
# cv2.imwrite('gpic1R.png',imgL2) #right grey picture saved

##random dot stereograms
# B = np.zeros((512,512)) #big image
# S = np.zeros((256,256)) #small image
#
#
# for x in range(512):
#     for y in range(512):
#         B[x,y] = randint(0,255)
#
#
# for x in range(256):
#     for y in range(256):
#         S[x,y] = randint(0,255)
#
# L = np.copy(B)
# R = np.copy(B)
#
# for x in range(124,380):  #M[row,column] #M[y-axis, x-axis]
#     for y in range(128,384):   #128 + 256
#         L[y,x] = S[y-128,x-124]
#
# for x in range(132, 388):
#     for y in range(128, 384):
#         R[y,x] = S[y-128,x-132]
#
# imgL1 = L
# imgR1 = R


#mathcing cost function
def matching_cost(x_left, x_right):
    cost = ((x_left - x_right )**2)/16 #variance is 16.
    return cost

#cost matrix has dimentions of width+2 x width+2
#case matrix has dimentions of width x width
#disparity map matrix has a dimension width x height
#disparity map L will store the x values on each row
#x value is
#disparity map R will store the y value on each row












#time to fill in the blanks
#start from 2 to width-1.

def onerow(width, occlusion,row_num,mapL,mapR):
    C = np.zeros((width, width))  # numpy works like this.
    Case = np.zeros((width -2, width-2 ))

    for i in range(width - 1):
        C[1][i + 1] = i * occlusion
    for i in range(width - 1):
        C[i + 1][1] = i * occlusion

    C[0, 2:width] = imgL1[row_num]
    C[2:width, 0] = imgR1[row_num]

    for i in range(2,width):
        for j in range(2,width):

                min1 = C[i-1,j-1] + matching_cost(C[0,i],C[j,0])
                min2 = C[i-1,j] + occlusion    #take the value to the left. according to cw brief.
                min3 = C[i,j-1] + occlusion    #take the value above according to the cw brief.
                #finding the minimum cost.
                C[i,j] = min(min1, min2, min3)
                if C[i,j] == min1:
                    Case[i-2,j-2] = 1
                elif C[i,j] == min2:
                    Case[i-2,j-2] = 2
                elif C[i,j] == min3:
                    Case[i-2,j-2] = 3
    #forward pass is done
    i=416    #insert the width of the picture minus one.
    j=416 #i=x,j=y

    while (i >= 0 and j >= 0):
        if Case[i, j] == 1: #case one goes top left.
            i =i - 1
            j =j - 1
            mapL[row_num,i] = abs(i-j) + 128  #left image is stored at row
            mapR[row_num,j] = abs(i-j) + 128  #right image is stored at column.
        elif Case[i,j] == 2: #case two goes one step above
            i = i-1


        elif Case[i,j] == 3: #case three goes one step left.
            j = j-1


def program():
    # initiating a matrix with zeros with the dimensions of the picture.
    height = 370    #insert the dimensions of the picture.
    width = 417+ 2
    occlusion = 6.0

    mapL = np.zeros((height, width - 2))  # disparity map.
    mapR = np.zeros((height, width - 2))

    for i in range (height):
        print(i)
        onerow(width, occlusion,i,mapL,mapR)

    cv2.imwrite('disparityL1_2.png', mapL)
    cv2.imwrite('disparityR1_2.png', mapR)

program()





