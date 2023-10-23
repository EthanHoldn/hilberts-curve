from PIL import Image
import numpy as np

# u = up
# d = down
# l = left
# l = right

# each character represents the direction of a line segment from the end of the last segment

# the seed is the initial configuration that is iterated on to get the next layer
seed = "urd"

#goes through the current step to find the next iteration
def steps(direction):
    new_direction = ""

    #first quadrant
    #rotates the previous step -90 deg and adds it to the new list of directions
    for d in direction[::-1]:
        if d == "d": new_direction += "r"
        if d == "r": new_direction += "u"
        if d == "u": new_direction += "l"
        if d == "l": new_direction += "d"

    #connects the first and second quadrant
    new_direction += "u"
    
    #second quadrant (not rotated)
    new_direction += direction

    #connects the second and third quadrants
    new_direction += "r"

    #third quadrant (not rotated)
    new_direction += direction

    #connects the third and forth quadrants
    new_direction += "d"

    #forth quadrants
    #rotates the previous step 90 deg and adds it to the new list of directions
    for d in direction[::-1]:
        if d == "d": new_direction += "l"
        if d == "r": new_direction += "d"
        if d == "u": new_direction += "r"
        if d == "l": new_direction += "u"
    return new_direction


#converts the list of directions into a list of points to be later converted into a piecewise linear curve by a septate program
def toCords(steps):
    points = [[0,0]]
    for i in steps:
        if i == "u": points += [[points[-1][0],points[-1][1]+1]]
        if i == "d": points += [[points[-1][0],points[-1][1]-1]]
        if i == "l": points += [[points[-1][0]-1,points[-1][1]]]
        if i == "r": points += [[points[-1][0]+1,points[-1][1]]]
    return points

#coverts the list of points into an image of the curve
def toImage(steps,d):

    #calculates the dimension of the image and creates the corresponding array of pixels
    size = 2**(d+2)-1
    image = [[0 for _ in range(size)] for _ in range(size)]

    #initial point
    point = [0,0]
    
    #calculates where each point is and draws a line
    #the pixel color can be changed to a gradient by replacing 255 with n%255
    for n in range(len(steps)):
        d = steps[n]

        #draws a in pixel at the current location of the point
        image[-1*(point[0]+1)][point[1]] = 255 #n%255

        #draws a pixel in between the current point and the next point
        if d == "u":
            image[-1*(point[0]+2)][point[1]] = 255 #n%255
            point = [point[0]+2,point[1]]
        elif d == "d":
            image[-1*(point[0])][point[1]] = 255 #n%255
            point = [point[0]-2,point[1]]
        elif d == "l":
            image[-1*(point[0]+1)][point[1]-1] = 255 #n%255
            point = [point[0],point[1]-2]
        elif d == "r":
            image[-1*(point[0]+1)][point[1]+1] = 255 #n%255
            point = [point[0],point[1]+2]

    #image[-1*(point[0]+1)][point[1]] = 255
    return(image)


s = 6
for i in range(s):
    seed = steps(seed)
print(seed)
img = Image.fromarray(np.array(toImage(seed,s)).astype(np.uint8))
img.show()
points = toCords(seed)

f = open("hilbert_curve.txt", "w")
for point in points:
    f.write(str(point[0])+" "+str(point[1])+"\n")
f.close()
