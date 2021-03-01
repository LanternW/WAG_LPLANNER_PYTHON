from constants import *
import math

def sign(num):
    if num >= 0:
        return 1
    else:
        return -1

def abs(num):
    if num < 0:
        return -num
    return num

def colorMerge(color1 , color2,k): #颜色线性插值器
    (r1,g1,b1,a1) = color1
    (r2,g2,b2,a2) = color2
    r = r1 + k * (r2 - r1)
    g = g1 + k * (g2 - g1)
    b = b1 + k * (b2 - b1)
    a = 0.5 * (a1 + a2)
    return (r,g,b,a)
    
def norm2(num1,num2):
    return math.sqrt(num1 * num1 + num2 * num2)

def distance(point1,point2):
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    return math.sqrt(dx*dx + dy*dy)

def inWhichArea(posx,posy):

    in_detail = gol.get_value("detail_menu")
    if in_detail != 0:
        if (posx > 50 and posx < SCREEN_WIDTH - 50) and (posy > 50 and posy < SCREEN_HEIGHT - 50):
            return IN_DETAIL

    if (posx > 0 and posx < SCREEN_HEIGHT) and (posy > 0 and posy < SCREEN_HEIGHT):
        return IN_MAP
    elif (posx > SCREEN_HEIGHT and posx < SCREEN_WIDTH) and (posy > 0 and posy < SCREEN_HEIGHT):
        return IN_SWITCH
    
    
    return 0

def isInMap(posx,posy):
    if (posx > 0 and posx < SCREEN_HEIGHT) and (posy > 0 and posy < SCREEN_HEIGHT):
        return True
    return False
