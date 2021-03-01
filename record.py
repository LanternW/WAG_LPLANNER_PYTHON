import xlrd
import gol


class Spot(): #景点
    def __init__(self,id,photo,production,description):
        self.id = id
        self.photo = photo
        self.production = production
        self.description = description

class Guide(): #Guide取“导游”含义
    def __init__(self):
        self.spots = []

    def memorizeSpot(self,id,photo,production,description):
        new_spot = Spot(id,photo,production,description)
        self.spots.append(new_spot)
    
    def getSpotById(self,id):
        for item in self.spots:
            if item.id == id:
                return item
        return None

def loadSpot(sheet):
    nrows = sheet.nrows #行数
    for i in range(nrows):
        id          = int(sheet.cell(i,0).value) #获取地标id
        file_name   = sheet.cell(i,2).value      #获取照片文件名
        production  = sheet.cell(i,3).value      #获取产品信息
        description = sheet.cell(i,4).value      #获取描述
        file_name = str("record\photos\\" + file_name)
        gol.guide.memorizeSpot(id,file_name,production,description)

def loadLDMK(map,sheet):
    nrows = sheet.nrows #行数
    for i in range(nrows):
        id      = int(sheet.cell(i,0).value) #获取地标id
        name    = sheet.cell(i,1).value      #获取名称
        world_x = int(sheet.cell(i,2).value) #获取x坐标
        world_z = int(sheet.cell(i,3).value) #获取z坐标
        r       = int(sheet.cell(i,4).value) #获取r
        g       = int(sheet.cell(i,5).value) #获取g
        b       = int(sheet.cell(i,6).value) #获取b
        dor     = int(sheet.cell(i,7).value) #获取"该地标是否存在地狱门"参数
        map.addLDMK((r,g,b,255),name,(world_x,world_z),id,dor)  #添加地标




def load():

    landmark_book = xlrd.open_workbook("record\\landmarks.xls")
    sheet_main = landmark_book.sheet_by_name('main')
    sheet_hell = landmark_book.sheet_by_name('hell')
    sheet_end = landmark_book.sheet_by_name('end')

    gol.map_main.landmarks_manager.landmarks.clear()
    gol.map_hell.landmarks_manager.landmarks.clear()
    gol.map_end.landmarks_manager.landmarks.clear()

    #读取地标
    loadLDMK(gol.map_main , sheet_main)
    loadLDMK(gol.map_hell,  sheet_hell)
    loadLDMK(gol.map_end,  sheet_end)

    #读取导游信息
    sopts_book = xlrd.open_workbook("record\\photos.xls")
    sheet_main = sopts_book.sheet_by_name('main')
    loadSpot(sheet_main)
