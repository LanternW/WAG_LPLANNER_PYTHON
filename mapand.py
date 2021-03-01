from constants import *
import pygame
import math
import gol
from asistant import *


class LandMark():

    def __init__(self,posx = 0 , posz = 0 , name = "地标",color = (255,0,0,255) , id = 100, dor = False):
        self.posx = posx
        self.posz = posz
        self.name = name
        self.color = color
        self.id = id
        self.dor = dor
    

class LDMKManager():

    def worldXZ2screenXY(self,OFFSET_X,OFFSET_Z,SCALE,x,z):
        screen_x = (SCREEN_HEIGHT / 2) + (x - OFFSET_X) * 100 / (16*SCALE)
        screen_z = (SCREEN_HEIGHT / 2) + (z - OFFSET_Z) * 100 / (16*SCALE)
        return (screen_x,screen_z)

    def __init__(self):
        self.landmarks = []

    def render(self,OFFSET_X,OFFSET_Z,SCALE):

        for item in self.landmarks:
            screen_pos = self.worldXZ2screenXY(OFFSET_X,OFFSET_Z,SCALE,item.posx,item.posz)
            if isInMap(screen_pos[0],screen_pos[1]):
                pygame.draw.rect(MAP_SCREEN,item.color,(screen_pos,(10,10)),0)
                MAP_SCREEN.blit(gol.font_Basis.render(item.name, True, (0, 0, 0,128)), (screen_pos[0] - 10 , screen_pos[1] - 15))

    def getLandmarkById(self,id):

        for item in self.landmarks:
            if item.id == id:
                return item
        return None



        


def colorMerge(color1 , color2): #颜色线性插值器
    k = 0.5
    (r1,g1,b1,a1) = color1
    (r2,g2,b2,a2) = color2
    r = r1 + k * (r2 - r1)
    g = g1 + k * (g2 - g1)
    b = b1 + k * (b2 - b1)
    a = 0.5 * (a1 + a2)
    return (r,g,b,a)


class Map():
    def __init__(self,bc = (128,0,0,0)):
        self.back_color = bc
        self.SCALE = 1.0
        self.OFFSET_X = 0
        self.OFFSET_Z = 0
        self.landmarks_manager = LDMKManager()

    def addLDMK(self,color,name,pos,id,dor):
        self.landmarks_manager.landmarks.append(LandMark(pos[0],pos[1],name,color,id,dor))

    def worldXZ2screenXY(self,x,z):
        screen_x = (SCREEN_HEIGHT / 2) + (x - self.OFFSET_X) * 100 / (16*self.SCALE)
        screen_z = (SCREEN_HEIGHT / 2) + (z - self.OFFSET_Z) * 100 / (16*self.SCALE)
        return (screen_x,screen_z)

    def screenXY2worldXZ(self,x,y):
        world_x = (x - (SCREEN_HEIGHT / 2)) * (16*self.SCALE) / 100 + self.OFFSET_X
        world_z = (y - (SCREEN_HEIGHT / 2)) * (16*self.SCALE) / 100 + self.OFFSET_Z
        return (world_x,world_z)

    def renderGrid(self):

        delta_scan = 16
        if self.SCALE > 10:
            delta_scan = 64
        center_x = math.floor(self.OFFSET_X / delta_scan)
        center_z = math.floor(self.OFFSET_Z / delta_scan)
        temp_x = center_x * delta_scan
        temp_z = center_z * delta_scan
        (ts_x , ts_y) = self.worldXZ2screenXY(temp_x,temp_z)

        
        while True:
            if ts_x < 0 and ts_y < 0:
                break
            if (False) :
                line_width = 2
                line_color = colorMerge(self.back_color,(0,0,0,255))
            else:
                line_width = 1
                line_color = colorMerge(self.back_color,(100,100,100,255))
            pygame.draw.lines(MAP_SCREEN, line_color, False, [(ts_x,0) , (ts_x,SCREEN_HEIGHT)],line_width)
            pygame.draw.lines(MAP_SCREEN, line_color, False, [(0,ts_y) , (SCREEN_HEIGHT,ts_y)],line_width) 
            temp_x = temp_x - delta_scan
            temp_z = temp_z - delta_scan
            (ts_x , ts_y) = self.worldXZ2screenXY(temp_x,temp_z) 
        
        temp_x = center_x * delta_scan + delta_scan
        temp_z = center_z * delta_scan + delta_scan
        (ts_x , ts_y) = self.worldXZ2screenXY(temp_x,temp_z)

        while True:
            if ts_x > SCREEN_HEIGHT and ts_y > SCREEN_HEIGHT:
                break
            if ts_x < 0 and ts_y < 0:
                break
            if (False) :
                line_width = 2
                line_color = colorMerge(self.back_color,(0,0,0,255))
            else:
                line_width = 1
                line_color = colorMerge(self.back_color,(100,100,100,255))
            pygame.draw.lines(MAP_SCREEN, line_color, False, [(ts_x,0) , (ts_x,SCREEN_HEIGHT)],line_width)
            pygame.draw.lines(MAP_SCREEN, line_color, False, [(0,ts_y) , (SCREEN_HEIGHT,ts_y)],line_width) 
            temp_x = temp_x + delta_scan
            temp_z = temp_z + delta_scan
            (ts_x , ts_y) = self.worldXZ2screenXY(temp_x,temp_z) 

    def renderLDMKS(self):

        layer_ldmk_sw = gol.get_value("layer_ldmk_sw")
        layer_ldmc_sw = gol.get_value("layer_ldmc_sw")
        layer_wlwl_sw = gol.get_value("layer_wlwl_sw")

        if gol.get_value("map_jump_sw") == 1:
            MAP_SCREEN.blit(gol.font_Basis.render(str("自动寻路中..."), True, (100, 0, 0,128)), (20 , 30))
        if layer_ldmk_sw == True:
            self.landmarks_manager.render(self.OFFSET_X,self.OFFSET_Z,self.SCALE)

    def renderCross(self):
        MAP_SCREEN.blit(gol.font_Basis.render(str("+"), True, (100, 0, 0,128)), (int(SCREEN_HEIGHT/2) ,int(SCREEN_HEIGHT/2) - 4 ))
        
    def render(self):

        MAP_SCREEN.fill(self.back_color)
        self.renderGrid()

