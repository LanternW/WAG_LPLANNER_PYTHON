import pygame
import gol
import control

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1040, 600  # 设置窗口大小
BASE_SCREEN = pygame.display.set_mode(SCREEN_SIZE)  # 底层窗口
MAP_SCREEN = pygame.Surface((SCREEN_HEIGHT,SCREEN_HEIGHT), pygame.SRCALPHA)   # 地图窗口
MAP_MARK = pygame.Surface((SCREEN_HEIGHT,SCREEN_HEIGHT), pygame.SRCALPHA)   # 地图窗口上方特效遮罩

SWITCH_SCREEN = pygame.Surface((SCREEN_WIDTH - SCREEN_HEIGHT,150), pygame.SRCALPHA)   # 选择控件窗口

DETAIL_SCREEN = pygame.Surface((SCREEN_WIDTH - 100 ,SCREEN_HEIGHT - 100), pygame.SRCALPHA)   # 细节窗口

BG_SCREEN = pygame.Surface((SCREEN_WIDTH ,SCREEN_HEIGHT), pygame.SRCALPHA)   # 背景窗口

SCRIBE_SCREEN = pygame.Surface((SCREEN_WIDTH - SCREEN_HEIGHT ,450), pygame.SRCALPHA)   # 描述窗口



IN_MAP = 1
IN_SWITCH = 2
IN_DETAIL = 3



#颜色定义 R,G,B,A
C_WBLUE = 25,155,155,255
C_GREEN = 25, 255, 15,200
C_YELLOW = 255,255,15,200
C_GRAY = 100, 100 ,100,255
C_RED = 255,50,50,200
C_BLACK = 0,0,0,255
C_WHITE = 255,255,255,255



#控件定义

# 控件id划区说明：
# 1~20：主界面控件
# 20~100：弹出界面控制按钮
# 100~1000：弹出界面主世界地标
# 1000~2000：弹出界面下界地标
# 2000~3000：弹出界面末地地标

switch_main_world = control.Switch((150,30),(25,30),(25, 255, 15,100),"主世界",1)
switch_main_world.selected = True
switch_hell = control.Switch((150,30),(25,70),(255,50,50,100),"下界",2)
switch_end = control.Switch((150,30),(25,110),(255,255,15,100),"末地",3)

controls = [switch_main_world , switch_hell , switch_end]

switch_ldmks = control.SwitchMulti((150,30),(200,30),(25, 120, 255,100),"地标图层",4)
switch_loadareas = control.SwitchMulti((150,30),(200,70),(125, 120, 205,100),"加载区域图层",5)
switch_cszds = control.SwitchMulti((150,30),(200,110),(125, 120, 205,100),"物流网络图层",6)

switch_ldmks_ex = control.Expander((30,30),(380,30),(25, 120, 255,100),"地标图层",7)
switch_loadareas_ex = control.Expander((30,30),(380,70),(125, 120, 205,100),"加载区域图层",8)
switch_cszds_ex = control.Expander((30,30),(380,110),(125, 120, 205,100),"物流网络图层",9)

layers = [switch_ldmks,switch_loadareas,switch_cszds]

expanders = [switch_ldmks_ex,switch_loadareas_ex,switch_cszds_ex]

#图片加载
app_mark = pygame.image.load("imgs\\mark.png")
app_mark = pygame.transform.scale(app_mark,(SCREEN_HEIGHT,SCREEN_HEIGHT))

bk_main = pygame.image.load("imgs\\main.png")
bk_main = pygame.transform.scale(bk_main,(SCREEN_WIDTH,SCREEN_HEIGHT))

bk_hell = pygame.image.load("imgs\\hell.png")
bk_hell = pygame.transform.scale(bk_hell,(SCREEN_WIDTH,SCREEN_HEIGHT))

bk_end = pygame.image.load("imgs\\end.png")
bk_end = pygame.transform.scale(bk_end,(SCREEN_WIDTH,SCREEN_HEIGHT))


