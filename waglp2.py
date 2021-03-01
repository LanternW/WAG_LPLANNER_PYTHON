import pygame
import sys

pygame.init()
pygame.display.set_caption('WAGLP2.0')

import gol

gol.init()


from constants import *
from asistant import *
from animation import *
from pygame.locals import * # pygame 的所有常亮名导入进来WWWW
import control
import record

record.load()


tick = 0
velocity_x = 0
velocity_z = 0
mouse_posx = -100000
mouse_posy = -100000
mosue_posx_old = -100000
mouse_posy_old = -100000
left_button_down = 0
id = 1
detail_id = 0

id_detail = 0
bk = bk_main
map_choice_id = 1
app_mark = pygame.image.load("imgs\\mark.png")
app_mark = pygame.transform.scale(app_mark,(SCREEN_HEIGHT,SCREEN_HEIGHT))
app_mark.blit(bk,(0,0),None,BLEND_MAX)

route_pos_start = (0,0)
route_pos_end   = (1,1)
route_switch    =  0 #导航开关
route_title = " "
route_str1 = "尚无相关交通信息，建议直接tp"
route_str2 = " "
route_under_bed = 0
route_production = " "
route_description = "暂无介绍"
route_photo = None

detail_controls = []

current_map = gol.get_value("current_map")


#初始化
gol.set_value("map_mark",255)
def findRoute(ldmk): #导航规划
    global route_pos_start,route_pos_end,route_str1,route_str2,route_title,route_under_bed,route_photo,route_production,route_description
    if map_choice_id == 1:
        posx_b = int(ldmk.posx / 8) #下界对应坐标
        posz_b = int(ldmk.posz / 8)
        point_b = (posx_b,posz_b)
        min_distance = 1000000000
        ldmk_b = None
        for item in gol.map_hell.landmarks_manager.landmarks:
            point_a = (item.posx,item.posz)
            dis = distance(point_a,point_b)
            if dis < min_distance and item.dor == True:
                min_distance = dis
                ldmk_b = item
        
        posx_bw = ldmk_b.posx * 8
        posz_bw = ldmk_b.posz * 8

        point_bus_station = (posx_bw,posz_bw)
        point_end = (ldmk.posx,ldmk.posz)

        route_title = str(ldmk.name + " 最优路径")
        route_str1 = str("从下界地标 [" + ldmk_b.name + "] 处进入主世界,")
        route_str2 = str("飞行 %d m 到达目的地" % (distance(point_bus_station,point_end) ))

        route_pos_start = point_bus_station
        route_pos_end = point_end

        if ldmk_b.name[-1] == '>':
            route_under_bed = 0
        else:
            route_under_bed = 1
        
        spot_item = gol.guide.getSpotById(ldmk.id)
        print(spot_item.photo)
        route_photo = pygame.image.load(spot_item.photo)
        route_photo = pygame.transform.scale(route_photo,(320,196))
        route_production = spot_item.production
        route_description = spot_item.description


def closeDetail(id): #收缩细节窗口

    for item in expanders:
        if item.id == id:
            if not item.isPassedBy(mouse_posx-SCREEN_HEIGHT,mouse_posy):
                item.onClick()

    if id == 7:
        gol.set_value("detail_end",0)
        gol.set_value("detail_endx",980)
        gol.set_value("detail_endy",30)
        
    if id == 8:
        gol.set_value("detail_end",0)
        gol.set_value("detail_endx",980)
        gol.set_value("detail_endy",70)
        
    if id == 9:
        gol.set_value("detail_end",0)
        gol.set_value("detail_endx",980)
        gol.set_value("detail_endy",110)
    gol.set_value("detail_menu",0)
    detail_controls = gol.get_value("detail_controls")
    detail_controls.clear()
    gol.set_value("detail_controls",detail_controls)
    detail_id = 0

def buttonsHandler(id): #按钮响应
    global route_pos_start,route_pos_end,route_switch
    if (id > 20 and id < 100): #按钮id
        if id == 23: #goto按钮
            ldmk = current_map.landmarks_manager.getLandmarkById(detail_id)
            gol.set_value("end_offsetx",ldmk.posx)
            gol.set_value("end_offsetz",ldmk.posz)
            gol.set_value("map_jump_sw",1)

            closeDetail(7)
            closeDetail(8)
            closeDetail(9)
            findRoute(ldmk)
            route_switch = 1

def renderControls(): #控件绘制
    
    SWITCH_SCREEN.fill((0,0,0,0))
    for item in controls:
        item.render(SWITCH_SCREEN)

    for item in layers:
        item.render(SWITCH_SCREEN)

    for item in expanders:
        item.render(SWITCH_SCREEN)

    BASE_SCREEN.blit(SWITCH_SCREEN,(SCREEN_HEIGHT,0))
def detailLayerRender(): #细节窗口绘制

    global detail_controls
    scale = gol.get_value("detail_scale")
    position_x = gol.get_value("detail_posx")
    position_y = gol.get_value("detail_posy")
    position = (position_x,position_y)

    detail_controls = gol.get_value("detail_controls")

    new_size = (int((SCREEN_WIDTH - 100) * scale)  ,int((SCREEN_HEIGHT - 100) * scale))
    if (new_size[0] + new_size[1] > 20):
        DETAIL_SCREEN.fill((128,128,128,200))
        if id_detail == 7:
            for item in detail_controls:
                item.render(DETAIL_SCREEN,(0,0,0,255))

        A = pygame.transform.scale(DETAIL_SCREEN,new_size)
        BASE_SCREEN.blit(A,position)

def debugRender(): #debug信息绘制

    mouse_world_pos = current_map.screenXY2worldXZ(mouse_posx,mouse_posy)
    blockx = math.floor(mouse_world_pos[0] / 16)
    blockz = math.floor(mouse_world_pos[1] / 16)
    string = str("x: %d , z: %d" % (mouse_world_pos[0] , mouse_world_pos[1]))
    MAP_SCREEN.blit(gol.font_Basis.render(string, True, (0, 0, 0,128)), (20 , 10))
    string = str("bX: %d , bZ: %d" % (blockx , blockz))
    MAP_SCREEN.blit(gol.font_Basis.render(string, True, (0, 0, 0,128)), (250 , 10))

    pygame.draw.rect(MAP_SCREEN,(100,100,100,140),((450,20),(100,5)),1,border_radius=5)
    pygame.draw.rect(MAP_SCREEN,(100,100,100,140),((450,20),(50,5)),0,border_radius=5)

    unit50 = current_map.SCALE * 8 
    MAP_SCREEN.blit(gol.font_Basis_s.render(str("0"), True, (0, 0, 0,128)), (450 , 10))
    string = str("%d"%unit50)
    MAP_SCREEN.blit(gol.font_Basis_s.render(string, True, (0, 0, 0,128)), (495 , 10))
    string = str("%d m" % (unit50 * 2))
    MAP_SCREEN.blit(gol.font_Basis_s.render(string, True, (0, 0, 0,128)), (540 , 10))

def routeRender(): #导航信息绘制

    global route_pos_start,route_pos_end,route_switch,route_under_bed,route_photo,route_production,route_description
    if route_switch == 1:
        SCRIBE_SCREEN.fill((0,0,0,0))
        (startposx,startposy) = current_map.worldXZ2screenXY(route_pos_start[0],route_pos_start[1])
        (endposx,endposy)   = current_map.worldXZ2screenXY(route_pos_end[0],route_pos_end[1])
        
        for i in range(100,255,30):
            color_route_line = colorMerge( (i,i,255,255) , current_map.back_color ,  0.7 - (i - 100)/222 + 0.3 )
            pygame.draw.line(MAP_SCREEN,color_route_line,(startposx,startposy),(endposx + 5,endposy + 5),int(20 - i/15))
        for i in range(100,255,30):
            color_circle = colorMerge((255,100,255,255-i), current_map.back_color , 0.5)
            pygame.draw.circle(MAP_SCREEN,color_circle,(startposx,startposy),(25- i/7) ,0)
        
        SCRIBE_SCREEN.blit(gol.font_Scribe.render(route_title, True, (255, 255, 255,128)), (10 , 10))
        SCRIBE_SCREEN.blit(gol.font_Scribe.render(route_str1, True, (255, 255, 255,128)), (10 , 50))
        SCRIBE_SCREEN.blit(gol.font_Scribe.render(route_str2, True, (255, 255, 255,128)), (10 , 80))

        if route_under_bed == 1:
            SCRIBE_SCREEN.blit(gol.font_Scribe.render(str("地狱门位于基岩下方"), True, (255, 100, 100,128)), (10 , 110))

        SCRIBE_SCREEN.blit(route_photo, (50 , 140))
        SCRIBE_SCREEN.blit(gol.font_Scribe.render(route_production, True, (100, 255, 100,128)), (10 , 340))
        SCRIBE_SCREEN.blit(gol.font_Scribe.render(route_description, True, (255, 255, 255,128)), (10 , 370))
        

    pass



def render(): #绘制


    bk = gol.get_value("bk")

    app_mark.blit(bk,(0,0),None,BLEND_MULT)
    app_mark.blit(bk,(0,0),None,BLEND_MAX)

    BG_SCREEN.blit(bk,(0,0))
    BASE_SCREEN.blit(BG_SCREEN,(0,0))

    current_map.render()
    routeRender()
    current_map.renderLDMKS()
    current_map.renderCross()
    ali_mark = gol.get_value("map_mark")
    MAP_MARK.fill((0,0,0,ali_mark))
    

    MAP_MARK.blit(app_mark,(0,0))
    renderControls()
    debugRender()
    BASE_SCREEN.blit(SCRIBE_SCREEN,(SCREEN_HEIGHT,170 ))
    BASE_SCREEN.blit(MAP_SCREEN, (0,0))
    BASE_SCREEN.blit(MAP_MARK,(0,0))
    detailLayerRender()

    BASE_SCREEN.blit(gol.font_Scribe.render(str("WagLplanner v2.1.1 by Lantern"), True, (255, 255, 255,128)), (SCREEN_WIDTH - 200 , SCREEN_HEIGHT - 25))
    
    
    pass
def mouseMoveHandler(x,y,mouse_area): #鼠标移动事件处理
    global mouse_posx,mouse_posy,mosue_posx_old,mouse_posy_old,velocity_x,velocity_z,left_button_down
    mouse_posx_old = mouse_posx
    mouse_posy_old = mouse_posy
    mouse_posx = x
    mouse_posy = y
    if left_button_down == 1:
        dx = mouse_posx - mouse_posx_old
        dz = mouse_posy - mouse_posy_old
        current_map.OFFSET_X = current_map.OFFSET_X - (dx / 100 * 16 * current_map.SCALE)
        current_map.OFFSET_Z = current_map.OFFSET_Z - (dz / 100 * 16 * current_map.SCALE)
        velocity_x = dx * 5 * current_map.SCALE
        velocity_z = dz * 5 * current_map.SCALE
    if mouse_area == IN_SWITCH:

        
        for item in controls:
            item.onPassedBy(x - SCREEN_HEIGHT,y)

        for item in layers:
            item.onPassedBy(x - SCREEN_HEIGHT,y)

        for item in expanders:
            item.onPassedBy(x - SCREEN_HEIGHT,y)
    
    if mouse_area == IN_DETAIL:

        detail_controls = gol.get_value("detail_controls")
        for item in detail_controls:
            item.onPassedBy(x - 50,y - 50)
def expandHandler(id,selected): #展开事件处理
    global id_detail
    if selected == True:
        if id == 7:
            gol.set_value("detail_end",1)
            gol.set_value("detail_endx",50)
            gol.set_value("detail_endy",50)
            id_detail = 7
            gol.set_value("detail_menu",1)

            detail_controls = gol.get_value("detail_controls")
            oringinal_x = 20
            oringinal_y = 15
            for item in current_map.landmarks_manager.landmarks:

                string = str("%s (x: %d , z: %d)" % (item.name,item.posx ,item.posz))
                ldmk_button = control.DetailSwitch((400,30),(oringinal_x,oringinal_y),item.color,string,item.id)
                detail_controls.append(ldmk_button)

                oringinal_y = oringinal_y + 30
                if oringinal_y > SCREEN_HEIGHT - 125:
                    oringinal_x = oringinal_x + 410
                    oringinal_y = 15

            control_btn_next = control.Button((32,32),(890,30),(0,0,0,0),"操作按钮之下一页",21,"btn_next.png")
            control_btn_last = control.Button((32,32),(890,70),(0,0,0,0),"操作按钮之上一页",22,"btn_last.png")
            control_btn_goto = control.Button((32,32),(890,140),(0,0,0,0),"操作按钮之跳转",23,"btn_goto.png")
            detail_controls.append(control_btn_next)
            detail_controls.append(control_btn_last)
            detail_controls.append(control_btn_goto)
            gol.set_value("detail_controls",detail_controls)

        if id == 8:
            gol.set_value("detail_end",1)
            gol.set_value("detail_endx",50)
            gol.set_value("detail_endy",50)
            id_detail = 8
            gol.set_value("detail_menu",2)
        
        if id == 9:
            gol.set_value("detail_end",1)
            gol.set_value("detail_endx",50)
            gol.set_value("detail_endy",50)
            id_detail = 9
            gol.set_value("detail_menu",3)

    if selected == False:
        closeDetail(id)
        
def mouseClickHandler(x,y,button,mouse_area): #鼠标单击事件处理
    global mouse_posx,mouse_posy,mosue_posx_old,mouse_posy_old,velocity_x,velocity_z,left_button_down,current_map,id,detail_id,bk,app_mark,map_choice_id
    if button == 5: #上滚轮
        if mouse_area == IN_MAP:
            zoom_kinetic_energy = gol.get_value("zoom_kinetic_energy") + 1  #假设物体“缩放”的质量为1 ，每次滚动给予1焦耳动能
            gol.set_value("zoom_kinetic_energy",zoom_kinetic_energy)
    if event.button == 4: #下滚轮
        if mouse_area == IN_MAP:
            zoom_kinetic_energy = gol.get_value("zoom_kinetic_energy") - 1
            gol.set_value("zoom_kinetic_energy",zoom_kinetic_energy)
                    

    if event.button == 1: #左键
        if mouse_area == IN_MAP:   # 地图界面单击信息处理
            left_button_down = 1
            velocity_x = 0
            velocity_z = 0
            gol.set_value("drag_kinetic_energy_x",0) #按下键拖拽时立即消除滑动动能
            gol.set_value("drag_kinetic_energy_z",0)
        if mouse_area == IN_SWITCH: # 主界面单击信息处理
            old_id = id
            for item in controls:
                if item.isPassedBy(x-SCREEN_HEIGHT,y) == True:
                    id = item.onClick()

            for item in layers:
                if item.isPassedBy(x-SCREEN_HEIGHT,y) == True:
                    (temid,se) = item.onClick()
                    if temid == 4:
                        gol.set_value("layer_ldmk_sw",se)
                    if temid == 5:
                        gol.set_value("layer_ldmc_sw",se)
                    if temid == 6:
                        gol.set_value("layer_wlwl_sw",se)
            
            for item in expanders:
                if item.isPassedBy(x-SCREEN_HEIGHT,y) == True:
                    (temid,se) = item.onClick()
                    expandHandler(temid,se)
                    if se == False:
                        for item in expanders:
                            item.blocked = False
                    if se == True:
                        for item in expanders:
                            if item.id != temid:
                                item.blocked = True
            
            if old_id != id:
                for item in controls:
                    if item.id != id:
                        item.selected = False
                        item.frame_color = (255,255,255,2)
                
                if id == 1:
                    current_map = gol.map_main
                    gol.set_value("current_map",current_map)
                    gol.set_value("bk_alpha",0)
                    gol.set_value("bk_end",1)
                    map_choice_id = 1
                if id == 2:
                    current_map = gol.map_hell
                    gol.set_value("current_map",current_map)
                    gol.set_value("bk_alpha",0)
                    gol.set_value("bk_end",2)
                    map_choice_id = 2
                if id == 3:
                    current_map = gol.map_end
                    gol.set_value("current_map",current_map)
                    gol.set_value("bk_alpha",0)
                    gol.set_value("bk_end",3)
                    map_choice_id = 3
        
        if mouse_area == IN_DETAIL: # 弹出界面单击信息处理
            detail_controls = gol.get_value("detail_controls")
            old_detail_id = detail_id
            for item in detail_controls:
                if item.isPassedBy(x-50,y-50) == True:
                    (clickid,se) = item.onClick()
                    if(not (clickid > 20 and clickid < 100)):
                        detail_id = clickid
                    buttonsHandler(clickid)
                    
            
            if (old_detail_id != detail_id):
                for item in detail_controls:
                    if item.id != detail_id:
                        item.selected = False
                        item.frame_color = (128,128,128,255)
                    
            




while True:  # 死循环确保窗口一直显示

    tick = tick + 1
    for event in pygame.event.get():  # 遍历所有事件
        mouse_area = inWhichArea(mouse_posx,mouse_posy)
        if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
                mouseClickHandler(mouse_posx,mouse_posy,event.button,mouse_area)

        if event.type == pygame.MOUSEMOTION:
                mouseMoveHandler(event.pos[0],event.pos[1],mouse_area)
            

        if event.type == pygame.MOUSEBUTTONUP:
            if left_button_down == 1:
                gol.set_value("drag_kinetic_energy_x", 0.5 * velocity_x * velocity_x * sign(velocity_x) )
                gol.set_value("drag_kinetic_energy_z", 0.5 * velocity_z * velocity_z * sign(velocity_z) )
            left_button_down = 0
            tick = 0

        if event.type == pygame.KEYDOWN:  #目前没什么用，占个位
            if event.key == K_w:
                a_flag = 1            
            elif event.key == K_s:
                a_flag = -1
            elif event.key == K_a:
                cx_flag = 1
            elif event.key == K_d:
                cx_flag = -1
        if event.type == pygame.KEYUP:
            a_flag = 0
            cx_flag = 0
            pause_flag = 0
    
    pygame.display.update()
    pygame.time.wait(1)
    pygame.draw.rect(BASE_SCREEN,C_BLACK,((0,0) ,SCREEN_SIZE),0)
    animationUpdate()
    render()

pygame.quit()  # 退出pygame