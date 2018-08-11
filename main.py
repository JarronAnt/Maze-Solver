import cv2
import numpy as np
import threading
import colorsys
from point import *

#this defines the entry point and exit point of the maze
startPoint = Point()
endPoint = Point()
#this defines the number of points we have registered 
numPoints = 0

rw = 2


#this array holds points pretatining to each 4 cardinal direction
             #UP           #DOWN       #LEFT        #RIGHT
directions = [Point(0,-1), Point(0,1), Point(-1,0), Point(1,0) ]


def handleMouseEvent(event, pX, pY, flags, param):
    global img, startPoint, endPoint, numPoints

    if(event == cv2.EVENT_LBUTTONUP):
        if numPoints == 0:
            #draw a small rectangle at the start point
            cv2.rectangle(img,(pX-rw, pY - rw), 
                    (pX+rw, pY+rw),(0,0, 255), -1 )
            startPoint = Point(pX,pY)
            print(startPoint.x, startPoint.y)
            numPoints += 1
        elif numPoints == 1 :
            #draw at the endpoint
            cv2.rectangle(img,(pX-rw, pY - rw), 
                    (pX+rw, pY+rw),(255,0, 0), -1 )
            endPoint = Point(pX, pY)
            print(endPoint.x, endPoint.y)
            numPoints += 1
            

def draw():
    global img
    #draw the image
    cv2.imshow("maze", img)
    #attach the handleMouse function to the callback
    cv2.setMouseCallback('maze', handleMouseEvent)

    #update the image every millisecond
    while True:
        cv2.imshow("maze", img)
        cv2.waitKey(1)


def BFS(s, e):

    #globals
    global img, h, w
    #out divisor
    const = 2000

    #bool flag
    found = False
    #queue
    q = []
    #array to hold visited nodes
    v = [[0 for j in range(w)] for i in range(h)]
    #array of parent nodes
    parent = [[Point() for j in range(w)] for i in range(h)]

    #add start node to the queue
    q.append(s)
    #set the start to be visited
    v[s.y][s.x] = 1
    #while we havent traversed the whole image
    while len(q) > 0:
        #pop from queue
        p = q.pop(0)
        for d in directions:
            #move to the next cell in any directions
            cell = p + d
            #if the cell is in bounds
            #if the cell hasnt been visited yet
            #if the cell isnt black(AKA a wall)
            if (cell.x >= 0 and cell.x < w and cell.y >= 0 and cell.y < h and v[cell.y][cell.x] == 0 and
                    (img[cell.y][cell.x][0] != 0 or img[cell.y][cell.x][1] != 0 or img[cell.y][cell.x][2] != 0)):
                #add the cell to the queue
                q.append(cell)
                #set the cell to be visited
                v[cell.y][cell.x] = v[p.y][p.x] + 1  

                #set the visited cell a color
                img[cell.y][cell.x] = list(reversed(
                    [i * 255 for i in colorsys.hsv_to_rgb(v[cell.y][cell.x] / const, 1, 1)])
                )
                #set the parent cell to be the point popped from the queue without the directions being attached
                parent[cell.y][cell.x] = p
                #if we reach the endpoint
                if cell == e:
                    #set the flag and delete the queue
                    found = True
                    del q[:]
                    break
    #array to hold the path
    path = []
    if found:
        #set the point to the endpoint
        p = e
        #while we havent hit the start
        while p != s:
            #add the parent to the path
            path.append(p)
            #set out cirrent point to be its parent(i.e be just travel the parent array in reverse)
            p = parent[p.y][p.x]
        #add the last node
        path.append(p)
        #reverse the array so we go from start to end
        path.reverse()

        #loop through the path and set the pixel to be white
        for p in path:
            img[p.y][p.x] = [255, 255, 255]
        print("Path Found")
    else:
        print("Path Not Found")




#prompt for the maze path
text = input("type in path to a maze or name of a provided maze: ") 
#read the image as grayscale
img = cv2.imread(text, cv2.IMREAD_GRAYSCALE)

#use the thresholding fuction to make the image from grayscale 
#to strictly black and white
_, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
#convert back to BGR
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

#get the x,y dimensions
h,w = img.shape[:2]

#prompt
print("set entry and exit points on the maze: ")

#create a seperate thread for the drawing function
thread = threading.Thread(target = draw, args=())
thread.daemon = True
thread.start()

while numPoints < 2:
    pass

#BFS OR DFS OR DIJKSTRAS (USING BFS)
#TODO implment various algos to do this 
BFS(startPoint, endPoint)

cv2.waitKey(0)