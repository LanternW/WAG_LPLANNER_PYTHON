#控件
import pygame 
import gol




class Switch():    #选择器
    def __init__(self,rect = (20,10) , position = (0,0) , color = (255,255,255,100),str_name = "选择" ,id = 0):

        self.rect = rect            #控件矩形框尺寸
        self.position = position    #位置
        self.selected = False       #被选中情况
        self.color = color          #颜色
        self.str_name = str_name
        self.id = id

        self.frame_color_direct = -1 #选中框颜色变化趋势
        self.frame_color = (255,255,255,0) #选中框颜色
    
    def isPassedBy(self,x,y): #鼠标是否在控件上
        if (x > self.position[0] and x < self.position[0] + self.rect[0]) and (y > self.position[1] and y < self.position[1] + self.rect[1]):
            return True
        return False
    def onPassedBy(self,x,y):
        if self.isPassedBy(x,y) == True:
            self.frame_color_direct = 8
        else:
            self.frame_color_direct = -4

    def animationUpdate(self):
        if self.selected == False:
            fa = self.frame_color[3]
            if self.frame_color_direct != 0:
                fa = fa + self.frame_color_direct
            if fa > 128:
                fa = 128
            if fa < 0:
                fa = 0
            self.frame_color = (255,255,255,fa)

    def onClick(self): #鼠标点击
        self.selected = True
        return self.id
    def render(self,screen):

        if self.selected == True:
            self.color = (self.color[0],self.color[1],self.color[2],200)
            self.frame_color_direct = 0
            self.frame_color = (255,255,255,200)
        else:
            self.color = (self.color[0],self.color[1],self.color[2],100)

        fa = self.frame_color[3]
        if fa > 0:
            pygame.draw.rect(screen,self.frame_color,(self.position,self.rect) , 2,border_radius=3)
        offset = int((self.rect[1]-15)/2)
        pygame.draw.rect(screen,self.color,( (self.position[0] + offset , self.position[1] + offset) ,(15,15)),0,border_radius=3)
        screen.blit(gol.font_Basis.render(self.str_name, True, (200, 200, 200,128)), (self.position[0] + 30 , self.position[1] + offset))


class SwitchMulti(Switch):    #多选器
    def onClick(self):
        self.selected = not self.selected
        return (self.id,self.selected)
    def render(self,screen,color = (255,255,255,255)):
        if self.selected == True:
            self.color = (self.color[0],self.color[1],self.color[2],200)
            self.frame_color_direct = 0
            self.frame_color = (255,255,255,200)
        else:
            self.color = (self.color[0],self.color[1],self.color[2],100)

        fa = self.frame_color[3]
        if fa > 0:
            pygame.draw.rect(screen,self.frame_color,(self.position,self.rect) , 2,border_radius=3)
        offset = int((self.rect[1]-15)/2)
        pygame.draw.rect(screen,self.color,( (self.position[0] + offset , self.position[1] + offset) ,(15,15)),0,border_radius=3)
        if self.selected == True:
            screen.blit(gol.font_Basis.render(self.str_name, True, (255,255,255,255)), (self.position[0] + 30 , self.position[1] + offset))
        else:
            screen.blit(gol.font_Basis.render(self.str_name, True, color), (self.position[0] + 30 , self.position[1] + offset))


class Expander(SwitchMulti):  #展开器

    def __init__(self,rect = (20,10) , position = (0,0) , color = (255,255,255,100),str_name = "选择" ,id = 0):
        super().__init__(rect , position, color,str_name ,id)
        self.frame_color = (255,255,255,100) #选中框颜色
        self.internal_rect_size = 0.3
        self.internal_rect_size_direct = -0.01
        self.blocked = False #阻塞
        isizex = int(self.rect[0] * self.internal_rect_size)
        isizey = int(self.rect[1] * self.internal_rect_size)
        self.internal_rect = (isizex,isizey)

    def onClick(self):
        if not self.blocked:
            self.selected = not self.selected
            if (self.selected == True):
                self.frame_color_direct = 6
                self.internal_rect_size_direct = 0.04
            else:
                self.frame_color_direct = -6
                self.internal_rect_size_direct = -0.04
            return (self.id,self.selected)
        return (-1,-1)

    def animationUpdate(self):
        if not self.blocked:
            fa = self.frame_color[3]
            if self.frame_color_direct != 0:
                fa = fa + self.frame_color_direct
            if fa > 255:
                fa = 255
            if fa < 100:
                fa = 100
            self.frame_color = (255,255,255,fa)
                
            irsize = self.internal_rect_size
            if self.internal_rect_size_direct != 0:
                irsize = irsize + self.internal_rect_size_direct
            if irsize > 1:
                irsize = 1
            if irsize < 0.3:
                irsize = 0.3
            self.internal_rect_size = irsize
            isizex = int(self.rect[0] * irsize)
            isizey = int(self.rect[1] * irsize)
            self.internal_rect = (isizex,isizey)

    def render(self,screen):
        pygame.draw.rect(screen,(0,0,0,255),(self.position,self.rect),0,border_radius = 3)
        pygame.draw.rect(screen,self.frame_color,(self.position,self.rect),2,border_radius = 3)
        posx = int((self.rect[0] - self.internal_rect[0]) / 2) + self.position[0]
        posy = int((self.rect[1] - self.internal_rect[1]) / 2) + self.position[1]
        pygame.draw.rect(screen,self.frame_color,((posx,posy),self.internal_rect),2,border_radius = 3)

class DetailSwitch(SwitchMulti):
    def __init__(self,rect = (20,10) , position = (0,0) , color = (255,255,255,100),str_name = "选择" ,id = 0):
        super().__init__(rect,position,color,str_name,id)
        self.frame_color = (128,128,128,200) #选中框颜色
        self.frame_color_direct = 0

    def onPassedBy(self,x,y):
        if self.isPassedBy(x,y) == True:
            self.frame_color_direct = -30
        else:
            self.frame_color_direct = 8

    def animationUpdate(self):
        if self.selected == False:
            fa = self.frame_color[3]
            if self.frame_color_direct != 0:
                fa = fa + self.frame_color_direct
            if fa > 200:
                fa = 200
            if fa < 1:
                fa = 1
            self.frame_color = (128,128,128,fa)

    def render(self,screen,color = (255,255,255,255)):
        if self.selected == True:
            self.color = (self.color[0],self.color[1],self.color[2],255)
            self.frame_color_direct = 0
            self.frame_color = (255,255,255,220)
        else:
            self.color = (self.color[0],self.color[1],self.color[2],200)

        fa = self.frame_color[3]
        if fa > 0:
            pygame.draw.rect(screen,self.frame_color,(self.position,self.rect) , 2,border_radius=3)
        offset = int((self.rect[1]-15)/2)
        pygame.draw.rect(screen,self.color,( (self.position[0] + offset , self.position[1] + offset) ,(15,15)),0,border_radius=3)
        if self.selected == True:
            screen.blit(gol.font_Basis.render(self.str_name, True, (255,255,255,255)), (self.position[0] + 30 , self.position[1] + offset))
        else:
            screen.blit(gol.font_Basis.render(self.str_name, True, color), (self.position[0] + 30 , self.position[1] + offset))


class Button(Switch):
    def __init__(self,rect = (20,10) , position = (0,0) , color = (255,255,255,100),str_name = "选择" ,id = 0 , img_name = "btn_last.png"):
        super().__init__(rect,position,color,str_name,id)
        
        btn_img_file_name = str("imgs\\" + img_name)
        print(btn_img_file_name)
        self.btn_img = pygame.image.load(btn_img_file_name)
        self.btn_img = pygame.transform.scale(self.btn_img,(32,32))
        self.img_alpha = 128
        self.img_alpha_velocity = 0
        self.btn_img.set_alpha(self.img_alpha)

    def onPassedBy(self,x,y):
        if self.isPassedBy(x,y) == True:
            self.img_alpha_velocity = 8
        else:
            self.img_alpha_velocity = -8

    def animationUpdate(self):
        fa = self.img_alpha
        if self.img_alpha_velocity != 0:
            fa = fa + self.img_alpha_velocity
        if fa > 255:
            fa = 255
        if fa < 128:
            fa = 128
        self.img_alpha = fa

    def onClick(self): #鼠标点击
        return (self.id,2)

    def render(self,screen,color = None):

        self.btn_img.set_alpha(self.img_alpha)
        screen.blit(self.btn_img, (self.position[0], self.position[1]))

