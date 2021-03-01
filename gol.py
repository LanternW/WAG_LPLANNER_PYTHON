import mapand
import pygame
import record
global_dict = {}

#地图对象定义
map_main = mapand.Map((150,255,150,170))
map_hell = mapand.Map((255,180,180,170))
map_end  = mapand.Map((200,200,100,170))

#导游对象定义
guide = record.Guide()

#map_main.addLDMK((255,0,0,255),"主世界测试地标1",(20,20),101)
#map_main.addLDMK((200,0,200,255),"世界原点",(0,0),102)
#
#map_hell.addLDMK((0,255,0,255),"下界测试地标1",(50,-50),201)
#
#map_end.addLDMK((0,0,255,255),"末地测试地标1",(150,-50),202)

#字体定义
font_Basis = pygame.font.Font("font\\admin.ttf",16)
font_Basis_s = pygame.font.SysFont("SimHei",10)
font_Scribe = pygame.font.Font("font\\scribe.ttf",18)
#
def set_value(key, value):
    #定义一个全局变量
    global_dict[key] = value

def get_value(key):
    return global_dict[key]

def init(): # 初始化
    global global_dict


    bk = pygame.image.load("imgs\\main.png")
    bk = pygame.transform.scale(bk,(1040,600))
    set_value("current_map",map_main)

    #图层开关
    set_value("layer_ldmk_sw",0)
    set_value("layer_ldmc_sw",0)
    set_value("layer_wlwl_sw",0)

    #细节菜单相关
    set_value("detail_menu",0) #1,2,3分别为开启第一、二、三个细节界面
    set_value("detail_controls",[]) #细节菜单控件
    set_value("detail_selet_id" , 0) #细节菜单中选中的item的id

    #动画相关
    set_value("zoom_kinetic_energy",0)  #缩放动能
    set_value("zoom_f",10)   #缩放阻尼系数
    set_value("drag_kinetic_energy_x",0)  #水平方向拖拽动能
    set_value("drag_kinetic_energy_z",0)  #垂直方向拖拽动能
    set_value("drag_f",5)   #拖拽阻尼系数

    set_value("map_mark",0) #遮罩层不透明度

    set_value("detail_end",0) #细节窗口目标缩放
    set_value("detail_endx",0) #细节窗口目标位置
    set_value("detail_endy",0) 
    set_value("detail_scale",0) #细节窗口缩放
    set_value("detail_posx",0)  #细节窗口位置
    set_value("detail_posy",0)

    set_value("bk_alpha",100) #背景图片不透明度
    set_value("bk_end",1) #目标背景图片
    set_value("bk",bk) #背景

    set_value("end_offsetx",0) #地图目标offsetx
    set_value("end_offsetz",0) #地图目标offsetz
    set_value("map_jump_sw",0) #地图跳转开关



